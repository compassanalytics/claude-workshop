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
git add .env
```

**Beat 2 — block-secrets command hook fires:**

```
Commit my staged changes.
```

**Beat 3 — agent hook reviews diff:**
The same `git commit` flow continues. After block-secrets clears (e.g. unstage `.env` and stage some clean change), trigger another commit attempt:

```
Stage src/api/main.py and commit "chore: trivial change".
```

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
