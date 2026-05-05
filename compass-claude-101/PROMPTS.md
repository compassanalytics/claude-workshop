# Demo Prompts — copy-paste

Every prompt and command you'll type during the workshop, in slide order.
Open this file on a second monitor or split-pane next to the Claude TUI.

---

## Part 2a — CLAUDE.md

**Beat 7 — Behavioral demo (the climax):**

```
Add an endpoint to delete an event by id.
```

*(Backup if you want a more pure-CLAUDE.md exercise:)*

```
Add bcrypt for password hashing in login.py.
```

---

## Part 2b — Rules

**Beat 3 — Read triggers rule load:**

```
I want to switch our /api/events list endpoint to cursor-based pagination — write the new route signature.
```

**Beat 4 — Write does NOT trigger (the gotcha):**

```
Without reading any existing files in src/api/, create a new file src/api/health/routes.py with a single endpoint that returns the current server time.
```

---

## Part 3 — Skills

**Beat 6 — `/scaffold-endpoint` live:**

```
/scaffold-endpoint POST /api/events/search
```

**Bonus — `/pr-prep` to show dynamic `!`cmd`` context:**

```
/pr-prep
```

---

## Part 4 — MCP

**Beat 2 — live tool invocation:**

```
Fetch the latest open Jira ticket assigned to me and summarize it.
```

*(Or any Jira/Confluence prompt that fits your account — what matters is that the audience sees an MCP tool call in the trace.)*

---

## Part 5 — Hooks

**Pre-stage in a terminal BEFORE the trigger:**

```bash
cp .env.example .env
git add -f .env
```

**⚠ Gotcha**: `.env` is in the project's `.gitignore`. You MUST use `-f` to force-add it; plain `git add .env` refuses. Without it staged, `block-secrets.sh` sees nothing in `git diff --cached` and the hook silently passes.

**Beat 2 — block-secrets command hook fires:**

```
Commit my staged changes.
```

**Beat 3 — agent hook reviews diff:**
After block-secrets blocks the bait commit, unstage `.env` and stage something clean:

```bash
git restore --staged .env
git add docs/testing.md
```

Then in the Claude TUI:

```
Commit my staged changes.
```

The agent hook should fire on this clean commit, emit `APPROVE: ...` or `BLOCK: ...`.

---

## Part 6 — Subagents

**Beat 2 — three subagents in parallel:**

```
Run security-scanner, pattern-explorer, and test-generator in parallel against src/api/auth/login.py. Merge their findings into one report.
```

---

## Part 7 — Plugins

**Live install commands (in the Claude TUI, not the terminal):**

```
/plugin marketplace add compassanalytics/claude-compass-superpowers
```

```
/plugin install general-dev@compassanalytics
```

*(Verify the marketplace path is reachable from your machine BEFORE the workshop — research's external fetch returned 404.)*

---

## Part 8 — Permissions

**Trigger A — denied (deny rule fires):**

```
Push my branch to main.
```

**Trigger B — allow-listed (no prompt):**

```
Run pytest.
```

**Trigger C — not on either list (Claude prompts):**

```
Check disk usage with `du -sh .`.
```

---

## Setup commands you may need

**Spin up a fresh demo copy anywhere:**

```bash
bash /Users/Richard.El-Chaar/Documents/claude-workshop/setup-demo.sh ~/Desktop/demo-test
```

**Activate venv + open Claude in the test dir:**

```bash
cd ~/Documents/compass-claude-101-test
source .venv/bin/activate
claude
```

**Re-pull the latest workshop materials before the workshop:**

```bash
cd /Users/Richard.El-Chaar/Documents/claude-workshop
git pull
```

---

## Reset between dry-runs

Demos accumulate cruft (modified routes from Part 2a, new files from Part 2b, staged `.env` from Part 5). Use the reset script to get back to a known good state:

```bash
cd ~/Documents/compass-claude-101-test
bash reset-demo.sh             # plain reset — restores working tree, removes demo artifacts
bash reset-demo.sh --bait      # reset + pre-stage .env for the hooks demo
```

The script:
- Restores all unstaged + staged changes
- Removes `src/api/health/` (Part 2b artifact) and `.env`
- With `--bait`: re-creates `.env` from `.env.example` and force-stages it

It does NOT touch `.venv`, `.git`, `.claude/`, or `CLAUDE.local.md`.

---

## Live-demo gotchas (things that bit me, things to watch)

| Gotcha | Why it bites | Fix |
|---|---|---|
| `git add .env` refuses with "paths are ignored" | `.env` is gitignored. The hook needs it staged though. | Use `git add -f .env` (force) |
| zsh chokes on commands with `# inline comments` when pasted | zsh's default doesn't treat `#` as a comment in interactive mode | Drop the comments, paste only the actual command |
| Path-scoped backend rule didn't fire on a "create new file" prompt | Path-scoped rules trigger on **reads**, not writes | Working as designed — that IS the Part 2b gotcha demo. If you wanted the rule to fire, the prompt has to make Claude read an existing `src/api/*.py` first. |
| Subdirectory `src/api/CLAUDE.md` doesn't load when I open Claude from project root | Subdir CLAUDE.mds load lazily — only when Claude reads a file in that dir | Working as designed. It activates during the behavioral demo (when Claude opens existing routes). To eager-load it, `cd src/api && claude` instead. |
| `it's done boss` doesn't appear at the end of Claude's response | `CLAUDE.local.md` didn't load | Verify the file exists and is non-empty in the demo project root. Restart Claude. |
| Agent hook (`commit-reviewer`) output isn't visible in the TUI | Schema verified, runtime display is the one thing I couldn't pre-test | If you can't see the APPROVE/BLOCK line, drop Trigger D from the demo and demo only command hooks. |
