# Claude Code Workshop

Internal workshop materials for leveling up Claude Code usage at Compass Analytics.

**Live site:** [compassanalytics.github.io/claude-workshop](https://compassanalytics.github.io/claude-workshop) (redirects to Session 2)

---

## Sessions

| Session | Topic | What you'll learn |
|---|---|---|
| **Session 1** | [From Basics to Power User](app/session-1.html) | CLAUDE.md, rules, skills, hooks, MCP, subagents, agent teams, plugins, permissions. Demo project: [`compass-claude-101/`](compass-claude-101/README.md). |
| **Session 2** | [Agentic SDLC Workflows](app/session-2.html) | Spec-driven development, structured lifecycles, persistence, orchestration, and building your own SDLC plugin |

---

## Quick Start: Install the Workshop Skills

Session 2 includes hands-on skill building. Install the workshop skills with one command:

```bash
curl -sL https://raw.githubusercontent.com/compassanalytics/claude-workshop/main/install.sh | bash
```

This copies the following skills into `~/.claude/skills/` so they're available in every Claude Code session:

- **`/sdlc`** — lightweight spec-driven development toolkit
- **`/sdlc-coach`** — interactive guide for designing your own SDLC plugin

Verify the install:

```bash
/sdlc-coach
```

Prefer manual? Clone the repo and copy the skills yourself:

```bash
git clone https://github.com/compassanalytics/claude-workshop.git
cp -r claude-workshop/workshop-session-2/skills/* ~/.claude/skills/
```

---

## Bring Claude to the Workshop

Want Claude to participate with you as you follow the session? Paste this into any Claude Code session:

```
Follow the Claude Code Workshop Session 2 companion guide and help me participate actively:
https://raw.githubusercontent.com/compassanalytics/claude-workshop/main/workshop-session-2/COMPANION.md
```

Claude will read the companion guide and act as your workshop co-pilot — surfacing key concepts, answering questions, and guiding you through the hands-on exercises in real time.

---

## Repo Structure

```
.
├── app/                          # GitHub Pages site (the workshop slides — single source of truth)
│   ├── index.html                # Redirects to session-2.html
│   ├── session-1.html            # Session 1 content
│   ├── session-2.html            # Session 2 content
│   ├── session-2-notes.html      # Presenter notes version
│   ├── images/, assets/          # Diagrams and screenshots
│   └── render-diagrams.py        # Mermaid diagram renderer
├── compass-claude-101/           # Session 1 hands-on demo project (FastAPI + React + .claude/)
│   ├── CLAUDE.md, .claude/, src/, web/, tests/
│   └── README.md                 # Host setup + demo segment → files map
├── workshop-session-2/           # Session 2 plugin: sdlc + sdlc-coach skills + companion
│   ├── .claude-plugin/plugin.json
│   ├── skills/sdlc/, skills/sdlc-coach/
│   └── COMPANION.md              # Copy-paste guide for the Claude Code companion
├── install.sh                    # One-line installer for session-2 skills
├── .github/workflows/pages.yml   # GitHub Pages deployment
└── README.md
```

---

## Regenerating Diagrams

Session 2 uses Mermaid diagrams. To regenerate them after editing:

```bash
cd app
python3 render-diagrams.py
```

Requires `npx` and Node.js (installs `@mermaid-js/mermaid-cli` automatically).

---

## Contributing

This is a living workshop. If you update `session-2.html`, consider whether `session-2-notes.html` needs corresponding changes.

Push to `main` and GitHub Pages redeploys automatically.
