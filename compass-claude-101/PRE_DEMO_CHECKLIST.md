# Pre-Demo Checklist

Things that actually need verification before workshop day. Stagecraft (IDE layout, fonts, dry-run) is implicit — not on this list.

---

## 1. Spin up a fresh demo copy

```bash
cd ~/Desktop  # or anywhere you want
bash /path/to/claude-workshop/setup-demo.sh ~/Desktop/demo-workshop
```

- [ ] Script completes without errors
- [ ] Output ends with `✓ All tests passed`
- [ ] `cd ~/Desktop/demo-workshop` shows `.claude/`, `src/`, `web/`, `tests/`, `.venv/`

## 2. MCP demo prerequisites (Part 4)

- [ ] Jira/Confluence env vars set in your shell — open a fresh terminal, run `echo $JIRA_API_TOKEN`, should print a value
- [ ] `uvx mcp-atlassian --help` works (proves the package is reachable)
- [ ] After launching `claude` in the demo dir, `claude mcp list` shows `atlassian` as connected (not `failed to start` or `not connected`)

## 3. Per-section demo triggers

Open `claude` in your demo copy, run each prompt, confirm the expected behaviour.

### Part 2a — CLAUDE.md
- [ ] Trigger: *"Add an endpoint to delete an event by id."*
- [ ] Output uses `snake_case`, Pydantic v2 `Annotated`, `Depends(get_current_user)`, the `problem()` helper

### Part 2b — Rules
- [ ] Trigger: *"I want to switch our `/api/events` list endpoint to cursor-based pagination — write the new route signature."*
- [ ] Claude reads `src/api/ingest/routes.py` (visible Read tool call)
- [ ] Claude PUSHES BACK and refuses cursor approach, citing the canonical limit/offset pattern
- [ ] Trigger: *"Without reading any existing files in `src/api/`, create a new file `src/api/health/routes.py` with a single endpoint that returns the current server time."*
- [ ] Output is generic (no `problem()` helper, no `Depends(get_current_user)` — proves the rule didn't fire)

### Part 3 — Skills
- [ ] Trigger: `/scaffold-endpoint POST /api/events/search`
- [ ] Slash command resolves; argument-hint shows in the TUI as you type
- [ ] Generated files: route handler, request model, response model, test stub
- [ ] All follow project conventions
- [ ] Trigger: `/pr-prep`
- [ ] The `Pre-flight context` block (the `!`cmd`` lines) renders git status / log / diff at the top of context

### Part 5 — Hooks (HIGHEST RISK)
- [ ] Pre-stage: `cp .env.example .env && git add -f .env` (the `-f` is required because `.env` is gitignored)
- [ ] Trigger: *"Commit my staged changes."*
- [ ] **Trigger A — `block-secrets`**: hook fires, audience can SEE the `BLOCKED: ...` message in the TUI
- [ ] **Trigger D — agent hook**: a fresh subagent reads the staged diff and emits `APPROVE: ...` or `BLOCK: ...` — **output must be visible in the TUI**, not silently logged. If you can't see it, drop Trigger D from the demo and only show command hooks.

### Part 6 — Subagents
- [ ] Trigger: *"Run security-scanner, pattern-explorer, and test-generator in parallel against `src/api/auth/login.py`. Merge their findings into one report."*
- [ ] Three concurrent Task tool invocations visible
- [ ] `security-scanner` finds the FIXME items (SQL injection, plaintext password, missing rate limit)
- [ ] Final output is a merged report, not three separate dumps

### Part 7 — Plugins
- [ ] `github.com/compassanalytics/claude-compass-superpowers` opens in your browser (research's external fetch returned 404 — verify from your machine)
- [ ] You can navigate into one plugin folder and read its `plugin.json` and `skills/`
- [ ] You know which plugins are currently in the marketplace (catalog matches your slide)

### Part 8 — Permissions
- [ ] Trigger: *"Push my branch to main."* → blocked with deny-rule reason visible
- [ ] Trigger: *"Run pytest."* → no permission prompt, runs immediately
- [ ] Trigger: a command outside both lists (e.g., `du -sh .`) → Claude pauses for your approval

---

## Risk items I cannot test for you

| Item | Why it's a risk | What to do |
|---|---|---|
| **Agent hook output surfacing** (Part 5 Trigger D) | Schema verified, runtime display in the TUI is unverified. | Run the trigger ONCE. If output doesn't visibly land, drop Trigger D, demo only command hooks. |
| **MCP server connection** (Part 4) | Depends on your real Jira/Confluence tokens being valid and `mcp-atlassian` working in your shell. | Run `claude mcp list` after launching; verify `atlassian` shows connected. |
| **`compass-superpowers` repo reachability** (Part 7) | Research's external fetch returned 404 — possibly private or moved. | Open the URL in a browser. If it 404s, find the correct path or skip the live tour. |
| **Live subagent timing** (Part 6) | Three concurrent agents can take 30–90s to all return. | Narrate while waiting ("each one is reading files independently in its own context"). |
