# Compass Claude 101 — Workshop Demo Project

A small FastAPI + React project used to teach Claude Code in a 90-minute intern workshop.
Each section of the slides has a corresponding artifact in this repo. Open the file, then trigger the behavior.

---

## Host setup (do this BEFORE the workshop)

Run through this once on the laptop you'll present from. It takes ~10 minutes.

### 1. Install dependencies (so `pytest` and `ruff` actually work in the demos)

```bash
cd compass-claude-101

# Python deps
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Frontend deps (optional — only if you want to demo `cd web && npm run lint`)
cd web && npm install && cd ..
```

Verify: `pytest -q` should report **5 passing** (3 auth + 2 ingest tests).

### 2. Initialize git

The `block-secrets` hook needs a real git repo to inspect staged files.

```bash
git init && git add -A && git commit -m "chore: initial scaffold"
```

### 3. Set up the hierarchy demo

Drop a personal CLAUDE.md at the user level so you have three tiers to show:

```bash
cp examples/global-CLAUDE.md.example ~/.claude/CLAUDE.md
```

(Edit it however you like — that file is yours.)

### 4. Pre-record an agent-teams clip

Agent teams are slow to spawn and occasionally flaky. Record a 90-second clean run as a fallback:

```
Spawn a 3-teammate team to refactor src/api/auth/ to add bcrypt password hashing
and rate limiting. Assign one teammate to the backend (login.py + tokens.py),
one to tests (test_auth.py), and one to the frontend login form (LoginForm.tsx).
Require plan approval before edits.
```

Save it. If the live demo stalls, play the recording instead.

### 5. Pre-stage one secret-block scenario

So the hooks demo is one keystroke away:

```bash
cp .env.example .env
git add .env
# Don't commit yet — the demo IS the commit attempt.
```

### 6. Open the right things on screen

- IDE on one half (project tree visible)
- Terminal with `claude` running on the other half
- Slides on a second monitor or a separate window

---

## Demo segment → what to show / what to trigger

For each row: open the files, narrate the structure for ~30 seconds, then run the trigger prompt.

### CLAUDE.md
- **Open**: `CLAUDE.md` (project), `~/.claude/CLAUDE.md` (global). Show three tiers stack.
- **Trigger**: *"Add an endpoint to delete an event by id."*
- **What to point out**: Watch Claude follow conventions without being told — snake_case, Pydantic v2 `Annotated`, `Depends(get_current_user)`, the `problem()` helper. None of that is in CLAUDE.md directly — it's in the path-scoped backend rule, which loads because Claude reads existing routes first.

### Rules — read triggers
- **Open**: `.claude/rules/testing.md` (unscoped), `.claude/rules/backend/api.md` (scoped to `src/api/**/*.py`), `.claude/rules/frontend/ui.md` (scoped to `web/src/**`).
- **Trigger A** (read → rule loads): *"Explain how login works in this codebase."* Claude reads `src/api/auth/login.py` → backend rule loads → answer references `Depends(get_current_user)` and `problem()`.
- **Trigger B** (write only → rule does NOT load): *"Without reading any existing files, create `src/api/health/routes.py` with a single endpoint that returns the current server time."* Claude writes a new file from scratch with no reads → backend rule never loads → output may skip `problem()`, may use a different error pattern, may forget the pagination/auth boilerplate. **That gap is the gotcha.**
- **What to point out**: Path-scoped rules trigger on **reads**, not writes. If a rule must apply during file creation, make it unscoped.

### Skills
- **Open**: `.claude/skills/scaffold-endpoint/SKILL.md`, `.claude/skills/pr-prep/SKILL.md`, `.claude/skills/deploy/SKILL.md`. Walk through frontmatter on one of them.
- **Trigger A**: `/scaffold-endpoint POST /api/events/search` — watches Claude generate handler + Pydantic models + test stub from one argument.
- **Trigger B**: `/pr-prep` — point at the **`Pre-flight context`** block at the top of `pr-prep/SKILL.md`. The `!`git status --short`` and `!`git log --oneline -10`` lines run *before* Claude reads the body; Claude receives the rendered output as context, not the commands. That's the dynamic-context feature.
- **What to point out**:
  - `argument-hint` shows the audience how `$ARGUMENTS` flows in.
  - `disable-model-invocation: true` on `/deploy` — Claude can't auto-fire it. Side effects only happen on explicit user invocation. *Bonus*: the description isn't even loaded into context for skills with this flag — they're invisible to auto-invocation.
  - `allowed-tools` on `/pr-prep` restricts what the skill can do (Bash + Read + Grep, no Write).
  - `!`cmd`` dynamic context in `/pr-prep` — repo state is pre-rendered into the prompt without Claude having to make tool calls first.

### Hooks
- **Open**: `.claude/settings.json` (the `hooks` block) and `.claude/hooks/*.sh`. Walk through one script. Show how stdin JSON gets parsed with `jq`.
- **Trigger A** (command hook — block-secrets fires): *"Commit my staged changes."* Claude tries `git commit` → `block-secrets.sh` exits 2 → audience sees the BLOCKED stderr message.
- **Trigger B** (command hook — auto-format fires invisibly): *"Add a docstring to the `health` function in `src/api/main.py`."* Claude edits the file → `auto-format.sh` runs `ruff format` → file is reformatted automatically.
- **Trigger C** (command hook — notify fires): End the conversation. Desktop notification pops.
- **Trigger D** (`agent` hook — subagent reviews the commit): the same `git commit` from Trigger A also fires the agent hook on the `PreToolUse Bash` matcher. After block-secrets clears, a fresh subagent reads the staged diff and emits `APPROVE: <reason>` or `BLOCK: <reason>`. The audience sees an LLM judging the commit in real time. **This is the highlight** — deterministic trigger, AI-level judgment.
- **Trigger E** (`prompt` hook — auto-summary on session end): when the conversation ends, a `Stop` prompt hook fires a single Claude inference that summarizes what was accomplished. Lighter than agent hooks, useful for lifecycle annotations.
- **What to point out**:
  - Hooks are **deterministic at the trigger** — every `Bash` call fires every entry in this matcher. Exit 2 unconditionally blocks.
  - There are **five hook types**: `command`, `prompt`, `agent`, plus `http` and `mcp_tool` (not demoed today).
  - Caveat: the agent hook fires on every Bash call, then the prompt itself filters to commits. In production you'd use the `if:` field for cheaper gating.
  - Caveat: agent hooks are still marked experimental as of May 2026.

### Subagents (parallel)
- **Open**: `.claude/agents/security-scanner.md`, `pattern-explorer.md`, `test-generator.md`. Walk the frontmatter.
- **Trigger**: *"Run security-scanner, pattern-explorer, and test-generator in parallel against `src/api/auth/login.py`. Merge their findings into one report."*
- **What to point out**: Three concurrent `Task` invocations in the UI. Each subagent has its own clean context — they're not seeing each other's work or the parent conversation. `login.py` has intentional FIXMEs for SQL injection, plaintext password compare, and missing rate limiting; security-scanner finds all three at concrete line numbers.

### Agent Teams
- **Open**: `.claude/settings.json` — point at `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- **Trigger** (live or pre-recorded): the prompt from "Host setup" step 4.
- **What to point out**: Each teammate has its own session. Shared task list on disk. `SendMessage` lets teammates coordinate directly without going through the lead. `Shift+Down` cycles between sessions. Caveat — experimental, ~7× token cost, treat as advanced.

### Permissions
- **Open**: `.claude/settings.json` — `permissions` block. Three deny rules, ~12 allow rules.
- **Trigger A** (denied): *"Push my current branch to main."* → `Bash(git push *)` denies → blocked.
- **Trigger B** (allow-listed): *"Run pytest."* → `Bash(pytest *)` allowed → runs without prompting.
- **Trigger C** (prompt): *"Run `npx some-cli`."* → not in allow OR deny → user gets prompted.
- **What to point out**: Deny beats allow. Build the allow list from things you keep rubber-stamping. For yolo mode, use a container — the `claude-yolo` Docker setup is the safe path.

### Plugins + Compass tour
- **Open**: nothing pre-installed.
- **Trigger**:
  ```
  /plugin marketplace add compassanalytics/claude-compass-superpowers
  /plugin install general-dev@compassanalytics
  ```
- **Walk through**: what got added — new skills, agents, possibly hooks/MCPs. Then list the 9 plugins in the marketplace and what each one does.
- **What to point out**: Plugins are the packaging layer. One repo → `.claude/`. Multiple projects or team → plugin. The Compass marketplace exists, anyone can contribute.

---

## Intentional teaching artifacts inside the code

These are NOT bugs to fix. They exist so the demos have something concrete to find:

- `src/api/auth/login.py` — `FIXME[security]` markers for **SQL injection** (string-interpolated `text()` query), **plaintext password compare** (`row.password != payload.password`), and **no rate limiting**. The `security-scanner` subagent finds all three.
- `src/api/models/user.py` — stores `password` as plaintext `String`. Same teaching purpose.
- `src/api/auth/login.py` and `src/api/ingest/routes.py` — both demonstrate the canonical patterns the path-scoped backend rule documents (`Depends(get_current_user)`, `problem()`, response_model, pagination signature).

---

## What this project is NOT

- It is **not production code**. The auth flow has deliberate vulnerabilities for the security-scanner demo.
- It is **not the spec-driven workflow demo** — that's Session 2 with `/sdlc-coach`.
- It is **not** meant to be deployed. The `/deploy` skill exists only to demonstrate `disable-model-invocation`.
