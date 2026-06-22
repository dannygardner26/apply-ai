import http.server
import json
import os
import threading

PORT = 8300
DIR = os.path.dirname(os.path.abspath(__file__))

_locks = {}
_locks_guard = threading.Lock()

def _lock_for(path):
    with _locks_guard:
        lock = _locks.get(path)
        if lock is None:
            lock = threading.Lock()
            _locks[path] = lock
        return lock


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_PUT(self):
        try:
            if self.path.startswith('/data/') and self.path.endswith('.json'):
                filepath = os.path.join(DIR, self.path.lstrip('/'))
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)
                try:
                    json.loads(body)
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error":"invalid json"}')
                    return
                with _lock_for(filepath):
                    tmp = filepath + '.tmp'
                    with open(tmp, 'wb') as f:
                        f.write(body)
                        f.flush()
                        os.fsync(f.fileno())
                    os.replace(tmp, filepath)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            else:
                self.send_response(403)
                self.end_headers()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass
        except Exception as e:
            try:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            except Exception:
                pass

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    print(f"Apply AI dashboard running at http://localhost:{PORT}")
    while True:
        try:
            Server(('', PORT), Handler).serve_forever()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("server error, restarting:", e)
