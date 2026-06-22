# Apply AI

An AI-powered application prep skill for Claude Code that helps you mass-apply to internships, jobs, and programs with confidence.

## What It Does

1. **Onboarding** — Your Claude agent asks you questions about yourself (skills, goals, experience, preferences) and builds a profile
2. **Resume Upload** — Upload your resume(s) and the agent parses them into structured data
3. **Dashboard** — Auto-generates a personal application tracking dashboard (HTML, runs locally)
4. **Question Bank** — As you answer application questions, the agent caches your answers for reuse
5. **Auto-Fill** — Deterministic fields (name, email, GPA, etc.) are filled automatically from your profile
6. **Long-Form Drafts** — For essay/short-answer questions, the agent drafts in YOUR voice based on your profile
7. **Submit** — Uses Playwright MCP to fill out and submit applications in your browser

## How to Use

### As a Claude Code Skill
```bash
# Clone into your skills directory
git clone https://github.com/dannygardner26/apply-ai.git ~/.claude/skills/apply-ai/

# Or reference it in your CLAUDE.md
```

Then just tell your Claude agent: "I want to apply to jobs" or invoke `/apply-ai`

### Standalone
```bash
git clone https://github.com/dannygardner26/apply-ai.git
cd apply-ai
# Open the dashboard
python -m http.server 8000
# Visit http://localhost:8000/dashboard.html
```

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. ONBOARDING                                              │
│  Agent interviews you → builds profile.json                 │
│  "What's your major?" "Target roles?" "Top 3 projects?"    │
├─────────────────────────────────────────────────────────────┤
│  2. RESUME PARSING                                          │
│  Upload PDF → agent extracts structured data                │
│  Skills, experience, education → auto-fill fields           │
├─────────────────────────────────────────────────────────────┤
│  3. PROGRAM DISCOVERY                                       │
│  "What kind of roles?" → agent finds matching programs      │
│  Deadlines, requirements, application links                 │
├─────────────────────────────────────────────────────────────┤
│  4. ANSWER CACHING                                          │
│  Short answers (name, GPA, grad year) → auto-filled         │
│  Long answers (essays, "why us?") → you write once, reuse   │
├─────────────────────────────────────────────────────────────┤
│  5. APPLICATION SUBMISSION                                  │
│  Agent opens form in Playwright → fills fields → you review │
│  One-click submit after your approval                       │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack

- **Skill Definition**: Claude Code skill (SKILL.md)
- **Dashboard**: Self-contained HTML (Warm Vanilla design system)
- **Data**: Local JSON files (profile.json, answers.json, applications.json)
- **Server**: Python SimpleHTTPServer for local dashboard + PUT persistence
- **Browser Automation**: Playwright MCP for form filling

## File Structure

```
apply-ai/
├── .claude/skills/apply-ai/SKILL.md   — The skill definition
├── dashboard.html                      — Application tracking dashboard
├── server.py                           — Local persistence server
├── data/
│   ├── profile-schema.json             — Profile data schema
│   ├── answers-schema.json             — Cached answer schema
│   └── applications-schema.json        — Application tracking schema
└── README.md
```

## Privacy

- All data stays local. Nothing is sent to any server.
- Your profile, answers, and applications are stored as JSON in the project directory.
- The skill never pushes, uploads, or transmits your personal information.

## License

MIT
