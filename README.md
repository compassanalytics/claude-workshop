# Claude Code Workshop

Internal workshop materials for leveling up Claude Code usage at Compass Analytics.

**Live site:** [compassanalytics.github.io/claude-workshop](https://compassanalytics.github.io/claude-workshop) (redirects to Session 2)

---

## Sessions

| Session | Topic | What you'll learn |
|---|---|---|
| **Session 1** | [From Basics to Power User](app/session-1.html) | CLAUDE.md, rules, skills, hooks, MCP, subagents, agent teams, plugins, permissions |
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

## Repo Structure

```
.
├── app/                          # GitHub Pages site
│   ├── index.html                # Redirects to session-2.html
│   ├── session-1.html            # Session 1 content
│   ├── session-2.html            # Session 2 content
│   ├── session-2-notes.html      # Presenter notes version
│   ├── images/                   # Diagrams and screenshots
│   └── render-diagrams.py        # Mermaid diagram renderer
├── content/                      # Raw content sources
├── install.sh                    # One-line skill installer
├── workshop-session-1.md         # Session 1 source material
├── workshop-session-2/           # Session 2 implementation artifacts
│   └── skills/                   # sdlc + sdlc-coach skills
└── .github/workflows/            # GitHub Pages deployment
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
