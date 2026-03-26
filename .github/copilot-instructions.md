# Project Guidelines — ITC-OS-2026

## Overview

University Operating Systems course platform (SE-019, Institute of Technology of Cambodia). Serves 12 weeks of lecture materials, 3 labs, class activities, and an interactive retro-terminal web interface with real-time presence tracking.

Live site: https://rathpiseyalpha.github.io/ITC-OS-2026/

## Tech Stack

- **Frontend**: Vanilla JS (no frameworks), Marked.js (CDN), Firebase Realtime Database (optional), GitHub API for file tree
- **Backend**: Python 3.12 stdlib only — no external dependencies
- **Containerization**: Docker + docker-compose
- **Hosting**: GitHub Pages (frontend), Linux server (backend API)

## Build & Run

```bash
# Backend (from repo root)
python3 server/app.py                  # port 5000
python3 server/app.py --port 8080      # custom port

# Docker (from server/)
docker-compose up                      # port 5000, mounts utmp/wtmp

# Frontend: static files, no build step — open index.html or use GitHub Pages
```

API endpoints: `GET /api/users`, `GET /api/who`, `GET /api/last?n=20`, `GET /api/health`. See [server/README.md](../server/README.md) for systemd and nginx setup.

## Architecture

```
app/js/          # Frontend modules (no build step)
  app.js         # Boot sequence, matrix rain, file explorer, router
  config.js      # GitHub repo, Firebase, presence server, course metadata
  github.js      # GitHub API tree fetch with local caching
  presence.js    # Dual-mode: Firebase (web visitors) + REST API (Linux users)
app/css/         # Terminal theme (green/cyan palette, Fira Code, scanlines)
server/          # Python REST API — parses `who`/`last` for presence data
lectures/        # Weekly notes, PDF slides, class activities
labs/             # Hands-on experiments with submission templates
```

Frontend and backend are independent — the static site works standalone via GitHub Pages; the presence API is optional.

## Conventions

### File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Lecture note | `week##-topic-slug.md` | `week01-introduction-to-os.md` |
| Lab folder | `lab#/` | `lab1/` |
| Lab instruction | `lab#-instruction.md` | `lab1-instruction.md` |
| Class activity | `class-activity#.md` | `class-activity1.md` |

### Markdown Content Patterns

- **Lecture notes** are fillable templates with 10 standard sections: Overview → Key Concepts table → Detailed Notes → Diagrams → Comparisons → Examples/Code → Review Questions → Connections → Reflection → Summary. See [lectures/notes/README.md](../lectures/notes/README.md) for the full template.
- **Lab instructions** start with a metadata table (Course, Title, Chapter, Duration), numbered objectives, then task-by-task sections with code blocks.
- **Class activities** have a navigation table, prerequisites, background theory, tasks, grading criteria, and submission template.
- Code blocks always specify language (```bash, ```c, ```python). Bash examples use `$` prefix.
- Emoji for visual hierarchy: 🎣 Hook, ❓ Question, 📝 Note, ✅ OK, ⚠️ Warning.
- Tables for definitions, schedules, and metadata comparisons.

### Code Style

- **JS**: Vanilla ES5/ES6, no framework, no build tools. Modules organized by concern (`app.js`, `config.js`, `github.js`, `presence.js`).
- **Python**: Stdlib only. No external packages. CORS headers set manually.
- **CSS**: Terminal/hacker theme — use existing color variables (green `#00ff41`, cyan `#00d4ff`). Fira Code font.

## Key Documentation

| Doc | What it covers |
|-----|----------------|
| [README.md](../README.md) | Project overview, repo structure, weekly topics |
| [course-outline.md](../course-outline.md) | Full 12-week syllabus and learning objectives |
| [server/README.md](../server/README.md) | API reference, Docker, systemd, nginx setup |
| [lectures/notes/README.md](../lectures/notes/README.md) | Note template structure and weekly file index |
| [lectures/class-activity/README.md](../lectures/class-activity/README.md) | Activity index, submission rules |

## Pitfalls

- GitHub API rate limit: 60 req/hr unauthenticated. Use a token in `config.js` for development (5000/hr). Never commit tokens.
- `presence.js` has dual mode (Firebase + REST). Firebase config in `config.js` is optional — the site works without it.
- Backend relies on Linux `who`/`last` commands — will not produce useful output on Windows/macOS.
