---
name: auto-apply
description: Automated application assistant for jobs/internships AND scholarships — finds opportunities, tailors materials, drafts essays/cover letters, and submits via Playwright
version: 2.0.0
author: Danny Gardner (@dannygardnercode)
---

# Auto-Apply Skill

A Claude Code skill that automates the tedious parts of applying to tech internships, jobs, AND scholarships. It finds relevant opportunities, tailors your materials to each one, writes essays/cover letters, and can even submit applications through browser automation.

## First Question: Jobs or Scholarships?

When you invoke this skill, it asks:

> **What are we applying to today?**
> 1. Jobs / Internships
> 2. Scholarships
> 3. Both

This determines which sources to search, what materials to generate, and how to track progress.

## What It Does

### Jobs/Internships Mode
1. **Discovers openings** — Searches job boards (LinkedIn, Handshake, company career pages) for roles matching your criteria
2. **Tailors your resume** — Rewrites bullet points to match each job description's keywords (ATS optimization)
3. **Drafts cover letters** — Generates personalized cover letters using your projects and experience
4. **Auto-fills applications** — Uses Playwright to navigate career portals and fill in your information
5. **Tracks everything** — Maintains a tracker of what you applied to, when, and current status

### Scholarship Mode
1. **Discovers scholarships** — Searches scholarship databases (Fastweb, Scholarships.com, Going Merry, school-specific) for matches
2. **Checks eligibility** — Filters by your grade level, GPA, demographic, field of study, location
3. **Drafts essays** — Generates scholarship essays from your profile. Most prompts reuse the same 3-4 themes (leadership, community impact, overcoming adversity, career goals) — write great answers once, adapt them.
4. **Fills applications** — Auto-fills personal info, uploads transcripts/recommendations, pastes essays
5. **Tracks deadlines** — Color-coded by urgency (red = <1 week, yellow = <1 month, green = 1+ month out)

## Setup

### Prerequisites
- Node.js 18+
- Playwright (`npm install playwright`)
- Your base resume (PDF or markdown)
- A `profile.md` with your info (name, email, school, GPA, skills, projects)

### Configuration

Create a `~/.claude/skills/auto-apply/config.json`:

```json
{
  "profile": {
    "name": "Your Name",
    "email": "you@example.com",
    "school": "University Name",
    "graduation": "2028",
    "gpa": "3.8",
    "major": "Computer Science",
    "grade_level": "junior",
    "linkedin": "linkedin.com/in/you",
    "github": "github.com/you",
    "phone": "555-123-4567",
    "state": "Illinois",
    "extracurriculars": ["Robotics Club President", "Varsity Track", "Volunteer Tutor"],
    "financial_need": false,
    "demographics": {}
  },
  "jobs": {
    "roles": ["Software Engineering Intern", "SWE Intern", "Backend Intern", "Full Stack Intern"],
    "locations": ["Remote", "New York", "San Francisco", "Chicago"],
    "min_pay": 0,
    "freshman_friendly": true,
    "exclude_companies": []
  },
  "scholarships": {
    "min_amount": 1000,
    "include_local": true,
    "include_national": true,
    "essay_bank_path": "~/applications/essay-bank.md",
    "categories": ["STEM", "leadership", "community service", "general merit"]
  },
  "resume_path": "~/resumes/base-resume.md",
  "tracker_path": "~/applications/tracker.md",
  "max_daily_applications": 10
}
```

## Usage

### Jobs Mode

```bash
claude "Use the auto-apply skill to find and apply to 5 SWE internships today"
claude "Use auto-apply to tailor my resume for this job: [paste URL or description]"
claude "Run an auto-apply session — find 10 freshman-friendly internships and apply to all of them"
```

### Scholarship Mode

```bash
claude "Use auto-apply in scholarship mode — find scholarships I'm eligible for"
claude "Use auto-apply to write my Coca-Cola Scholars essay"
claude "Run a scholarship session — find 10 local scholarships with upcoming deadlines"
claude "Use auto-apply to adapt my leadership essay for the Gates Scholarship (500 words)"
```

### Both

```bash
claude "Use auto-apply — find both internships and scholarships I should apply to this week"
```

## How It Works

### Step 0: Mode Selection

The skill asks upfront:
```
What are we applying to today?
> 1. Jobs / Internships
> 2. Scholarships
> 3. Both
```

This determines which discovery sources, material generation, and tracking format to use.

### Step 1: Discovery

**Jobs mode** searches:
- **LinkedIn Jobs** — filtered by entry-level, internship, your location preferences
- **Handshake** — your school's job board (if connected)
- **Company career pages** — directly hits known freshman-friendly programs (Microsoft Explore, NVIDIA Ignite, etc.)
- **GitHub Jobs, AngelList** — startup internships

**Scholarship mode** searches:
- **Fastweb / Scholarships.com** — national database filtered by your profile
- **Going Merry / Bold.org** — aggregators with one-profile-many-applications
- **Your school's financial aid page** — often has local/departmental scholarships nobody applies to
- **Community foundations** — your state/county's community foundation (often 5-20 scholarships with <50 applicants each)
- **Rotary, Lions Club, Elks, VFW** — local service orgs that give $1k-$5k with minimal competition
- **Employer programs** — parent's employer often has dependent scholarships
- **Known prestigious ones** — Coca-Cola Scholars, Gates, QuestBridge, Jack Kent Cooke, Ron Brown, Cameron Impact, Dell, Horatio Alger

### Step 2: Filtering

**Jobs** are scored:
- Does it match your role keywords? (+10)
- Is it explicitly freshman/sophomore friendly? (+20)
- Is it in your preferred location? (+5)
- Does the company have a known good intern program? (+10)
- Is the deadline still open? (required)

**Scholarships** are scored:
- Are you eligible? (grade level, GPA, demographics) — required
- Award amount vs. effort to apply (+1 per $1k/hour of work)
- Number of applicants — fewer = better odds (+20 if <100 applicants)
- Is it local? (+15 — local scholarships have way less competition)
- Do you already have a matching essay? (+10)
- Is the deadline soon? (+5 if <2 weeks — urgency, but still doable)

### Step 3: Resume Tailoring

For each application, the skill:
1. Extracts keywords from the job description (frameworks, languages, soft skills)
2. Rewrites your bullet points to naturally include those keywords
3. Reorders projects to put the most relevant ones first
4. Adjusts the "Skills" section to front-load what they're looking for
5. Generates a PDF using your LaTeX template (or markdown → PDF)

### Step 4: Cover Letter (Jobs) / Essay (Scholarships)

**Jobs — Cover Letter** (3 paragraphs):
- **Paragraph 1**: Why this company specifically (researches their product/mission)
- **Paragraph 2**: Your most relevant project/experience mapped to their needs
- **Paragraph 3**: What you'd bring to the team + enthusiasm

**Scholarships — Essay Bank** approach:

Most scholarship essays reuse the same 3-4 prompts. The skill maintains an essay bank:

| Prompt Theme | Example Questions |
|---|---|
| Leadership | "Describe a time you led others" / "Tell us about your leadership style" |
| Community Impact | "How have you made a difference?" / "Describe your volunteer work" |
| Overcoming Adversity | "Tell us about a challenge you've faced" / "What obstacle shaped you?" |
| Career Goals | "Where do you see yourself in 10 years?" / "Why this field?" |

The skill:
1. Identifies which theme(s) the scholarship prompt matches
2. Pulls your best essay for that theme from the bank
3. Adapts it to the specific word count, organization, and any unique angle they're asking for
4. Personalizes with details about the scholarship's mission ("As a Gates Scholar, I would...")
5. Stores the new version back in the bank for future reuse

### Step 5: Application Submission (Playwright)

For supported portals, the skill can auto-fill:
- Workday, Greenhouse, Lever, Ashby (most common ATS platforms)
- LinkedIn Easy Apply
- Handshake one-click apply

It fills in:
- Personal info (name, email, phone, school)
- Uploads tailored resume PDF
- Pastes cover letter
- Answers common screening questions ("Are you authorized to work in the US?", "Expected graduation date", etc.)
- **Stops before final submit** — shows you a preview and asks for confirmation

### Step 6: Tracking

After each application, logs to your tracker:
```markdown
| Date | Company | Role | Platform | Status | Link | Notes |
|------|---------|------|----------|--------|------|-------|
| 2026-06-23 | Microsoft | Explore Intern | Careers | Applied | [link] | Freshman program |
```

## Safety & Ethics

- **Never lies** on applications — only rewords your real experience
- **Stops before submit** by default — you confirm each one
- **Rate limited** — max 10/day to avoid looking like a bot
- **Respects robots.txt** — won't scrape sites that block automation
- **Your data stays local** — nothing is sent to external services except the application itself

## Anti-Patterns (Don't Do This)

- Don't apply to 100 jobs/day — quality > quantity, and companies notice
- Don't use generic cover letters — the whole point is personalization
- Don't skip reading the job description — the skill helps you prep, but YOU should understand the role
- Don't apply to roles you're wildly unqualified for — freshman applying to Staff Engineer wastes everyone's time

## Customization

### Add a new job board source

Edit `~/.claude/skills/auto-apply/sources.json`:
```json
[
  {
    "name": "Custom Board",
    "type": "scrape",
    "url": "https://jobs.example.com",
    "selectors": {
      "listing": ".job-card",
      "title": ".job-title",
      "company": ".company-name",
      "link": "a.apply-link"
    }
  }
]
```

### Add screening question answers

Pre-fill common questions in `config.json`:
```json
{
  "screening_answers": {
    "Are you authorized to work in the US?": "Yes",
    "Do you require visa sponsorship?": "No",
    "Expected graduation date": "May 2028",
    "Are you 18 or older?": "Yes",
    "How did you hear about us?": "University career fair"
  }
}
```

## Example Output

### Jobs session:

```
✓ Applied to 5 internships today:

1. Microsoft Explore — Redmond, WA (Freshman program)
   Resume tailored: emphasized React project + team leadership
   Cover letter: connected portfolio site to their developer tools mission

2. NVIDIA Ignite — Santa Clara, CA
   Resume tailored: highlighted CUDA coursework + ML project
   Cover letter: referenced their new GPU architecture announcement

3. Palantir Path — NYC
   Resume tailored: led with data pipeline project
   Cover letter: connected NHS project to their healthcare vertical

4. Ramp — NYC (Startup)
   Resume tailored: emphasized full-stack + fast shipping
   Cover letter: mentioned their expense management UX

5. Citadel Discover — Chicago
   Resume tailored: led with USACO Gold + competitive programming
   Cover letter: connected algorithmic thinking to trading systems

Tracker updated: ~/applications/tracker.md
```

### Scholarship session:

```
✓ Found 8 scholarships you're eligible for. Applied to 5:

1. Coca-Cola Scholars ($20,000) — National, 150 winners
   Essay: adapted "community impact" essay (was 600w → trimmed to 500w)
   Due: Oct 31 ✓ submitted

2. Champaign County Community Foundation ($2,500) — LOCAL, ~30 applicants
   Essay: reused "career goals" essay + added local angle
   Due: Nov 15 ✓ submitted

3. Elks Most Valuable Student ($4,000-$50,000) — 500 winners
   Essay: new draft combining "leadership" + "community" themes
   Due: Nov 5 ✓ submitted

4. Dell Scholars ($20,000 + laptop + mentoring)
   Essay: adapted "overcoming adversity" + "career goals"
   Due: Dec 1 ✓ submitted

5. Rotary Club of [Your Town] ($1,500) — LOCAL, ~15 applicants
   Essay: short 250w "why you deserve this" — adapted from bank
   Due: Nov 20 ✓ submitted

Skipped (ineligible): Ron Brown (not matching criteria), Cameron Impact (missed deadline)
Essay bank updated: 2 new versions saved
Tracker updated: ~/applications/tracker.md
```

## Getting Started

1. Clone this skill: `git clone https://github.com/dannygardner26/apply-ai`
2. Copy `config.example.json` to `config.json` and fill in your info
3. Add your base resume to the path specified in config
4. Run: `claude "Use auto-apply"` — it'll ask if you want jobs, scholarships, or both
5. Review the tailored materials
6. Confirm submissions or adjust and retry

---

*Built by [@dannygardnercode](https://instagram.com/dannygardnercode) — because applying to 50+ internships and scholarships manually is insane when Claude can do the boring parts.*
