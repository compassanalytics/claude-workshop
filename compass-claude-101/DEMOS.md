# Session 1 — Demo Points

Each block below maps to one section of `app/session-1.html`. Order matches the slide flow.

---

## (Pre — optional) Install & First Launch
- Install Claude Code (CLI)
- Login flow
- TUI tour: prompt, slash menu, `/help`, modes
- Where config lives: `~/.claude/` vs project `.claude/`

## Part 1 — The Evolution
- *No demo. Slide only.*

## Part 2a — CLAUDE.md

Order: hierarchy first (set scope), then content principles, then proof.

### 1. The anchor — open project CLAUDE.md *(IDE)*
- **Click**: `compass-claude-101/CLAUDE.md` in the file tree
- **Say**: "This is the project-level CLAUDE.md. Lives in the repo, gets committed, every teammate inherits it. Claude reads it at the start of every session — that's where persistent project context comes from."

### 2. Personal override — CLAUDE.local.md *(IDE — open file + .gitignore)*
- **Open**: `compass-claude-101/CLAUDE.local.md` and `compass-claude-101/.gitignore`
- **Say**: "Same idea as CLAUDE.md but personal. Gitignored, doesn't get pushed. Loads after CLAUDE.md and wins on conflict."
- **Point at the last bullet**: *"After editing or creating any file, end your response with this exact line: `it's done boss`"*
- **Say**: "That's our proof signal for the behavioural demo at the end. If `.local.md` actually loaded, Claude will end its response with 'it's done boss'. If we don't see that line, `.local.md` didn't load."
- **Critical caveat**: it's NOT auto-gitignored. You add `**/CLAUDE.local.md` to `.gitignore` yourself, OR run `/init` and pick the personal option which sets it up for you. Re-running `/init` is safe — it suggests improvements, doesn't overwrite.

### 3. Subdirectory CLAUDE.md — `src/api/CLAUDE.md` *(IDE)*
- **Open**: `compass-claude-101/src/api/CLAUDE.md`
- **Say**: "The third visible tier. When Claude works inside `src/api/`, this loads on top of the project CLAUDE.md. Keeps API-specific orientation scoped to where it matters."
- **Verbal aside (no file shown)**: "There's actually a fourth tier above all this — `~/.claude/CLAUDE.md` in your home directory. Personal preferences for every project on your machine. We won't open that one today; same concept, different scope. Total tiers: global → project → subdirectory, plus `.local.md` overrides at any level. Deeper wins on conflict."

### 4. Brevity + what earns its keep *(IDE — back in project CLAUDE.md)*
- **Action**: scroll project `CLAUDE.md` top-to-bottom in two seconds
- **Say**: "~35 lines. Anthropic targets under 200. Every line costs context tokens; concise instructions get followed more reliably."
- **Point at**: the `## Stack` and `## Project shape` sections
- **Say**: "These are technically derivable — Claude could read `pyproject.toml` and `ls` the repo. But they earn their keep as anchors. Saves five file reads to know we're on Pydantic v2 not v1. The 'don't include what Claude can figure out' rule is a bias toward less, not a wall."

### 5. Positive-instruction principle *(IDE — Workflow section)*
- **Point at**: the `## Workflow` section. Both bullets are positive (`Ask before adding new dependencies` / `Treat .claude/ config as user-managed — ask before changing it`)
- **Say**: "Both framed as DO X, not DON'T Y. LLMs follow positive framings more reliably than negations. If you catch yourself writing a long DON'T list, that's a signal to move it to a hook or a permissions deny rule — those are deterministic, not advisory."

### 6. Reference paths, not imports *(IDE — Reference docs section)*
- **Point at**: the `## Reference docs` section (three plain paths to `docs/*.md` files)
- **Open optionally**: `docs/error-handling.md` to show what's actually there — short, focused documentation
- **Say**: "Three plain path references to documentation. Claude reads them on-demand IF the current task needs them. If I'd written `@docs/error-handling.md` instead, that file plus the other two would load eagerly at session start — every session — whether the conversation needs them or not. `@` is for organization; plain paths are for true lazy loading."

### 7. Behavioral demo — the climax *(Terminal — Claude TUI)*
- **Type**: *"Add an endpoint to delete an event by id."*
- **Say while it generates**: "Watch what conventions Claude picks up — none of them are in my prompt."
- **After output, point at parts of the result**:
  - `snake_case` parameter names → "language default, fine"
  - Pydantic v2 `Annotated` syntax → "rule loaded when Claude opened existing routes"
  - `Depends(get_current_user)` → "rule again"
  - `problem(...)` helper from `src/api/errors.py` → "rule again, plus the docs reference in CLAUDE.md pointed at `docs/error-handling.md` if Claude needed deeper context"
- **And — the proof signal**: Claude's response ends with the line `it's done boss`. Point at it: *"That phrase only exists in CLAUDE.local.md. Project CLAUDE.md doesn't mention it; the path-scoped rule doesn't either. Seeing it on screen proves my personal override loaded and Claude followed it."*
- **Say**: "Nothing about this output came from my prompt. CLAUDE.md anchored the project context; the path-scoped backend rule loaded when Claude read existing routes; the subdirectory CLAUDE.md added API-specific orientation; CLAUDE.local.md added my personal touch. Four layers working together."

## Part 2b — Rules

Order: structure first (1, 2), then load behaviour (3, 4).

### 1. File tour *(IDE — three tabs)*
- **Open**: `.claude/rules/testing.md`, `.claude/rules/backend/api.md`, `.claude/rules/frontend/ui.md`
- **Say**: "`testing.md` has no frontmatter → unscoped, loads every session. The other two have a `paths:` block → path-scoped, only load when Claude reads files matching the glob."
- **Point at**: the size difference — CLAUDE.md is 30 lines, the backend rule is 50+ lines because it can be more detailed; it only costs context when relevant.

### 2. Glob quoting (YAML gotcha) *(IDE — frontmatter close-up)*
- **Point at**: the `paths:` block in `backend/api.md` — every pattern wrapped in double quotes (`"src/api/**/*.py"`)
- **Say**: "`*` and `{` are reserved in YAML. If you write `paths: src/**/*.py` unquoted, the parser silently breaks and the rule never loads. This was a real bug in the official docs (fixed Jan 2026). Always quote your patterns."

### 3. Read triggers rule load — Option A *(Terminal — Claude TUI)*
- **Type**: *"I want to switch our `/api/events` list endpoint to cursor-based pagination — write the new route signature."*
- **What happens**: Claude reads `src/api/ingest/routes.py` (visible Read tool call) → that path matches `src/api/**/*.py` → `backend/api.md` loads into context
- **Audience sees**: Claude pushes back. The rule explicitly says *"Don't invent alternative pagination shapes (cursors, page numbers)"*. So the response is something like *"This codebase uses `limit`/`offset` pagination — the backend rule forbids alternative shapes. Here's the existing signature..."*
- **Say**: "That NO is the rule talking. Without that file read, the rule wouldn't be in context, and Claude would just write the cursor route I asked for."

### 4. Write does NOT trigger — the gotcha *(Terminal — Claude TUI, ideally fresh session)*
- **Type**: *"Without reading any existing files in `src/api/`, create a new file `src/api/health/routes.py` with a single endpoint that returns the current server time."*
- **What happens**: Claude writes the file from scratch — no Read tool call on any `src/api/*.py` first → rule never matches → rule never loads
- **Audience sees**: the output likely misses rule-specific patterns (no `problem()` helper for errors, no `Depends(get_current_user)` if any auth is needed, generic pagination signature if list endpoint)
- **Say**: "Path-scoped rules trigger on READS, not writes. If a rule must apply even during file creation, make it unscoped — the way `testing.md` is."

## Part 3 — Skills & Commands

Order: structure → frontmatter knobs → body feature → proof → mention.

### 1. File tour *(IDE — file tree + three tabs)*
- **Open**: the `.claude/skills/` folder in the IDE tree, then `scaffold-endpoint/SKILL.md`, `pr-prep/SKILL.md`, `deploy/SKILL.md` in tabs
- **Point at**: `scaffold-endpoint/` is a *folder*, not a file — it contains `SKILL.md` AND a `reference/route-template.py` sitting alongside it. Skills can carry templates, scripts, reference docs.
- **Say**: "Skills aren't magic. They're regular markdown with YAML frontmatter, in a folder named after the skill. The folder can hold supporting content — `scaffold-endpoint` carries a route template that the skill body reads when it runs."

### 2. Frontmatter walk *(IDE — `scaffold-endpoint/SKILL.md` open)*
- **Point at**: `name`, `description`, `argument-hint`, `model`
- **Say**:
  - "`name` becomes the slash command. Defaults to the folder name if you don't set it."
  - "`description` is what Claude reads at startup to decide whether to auto-invoke. Anthropic's published numbers: ~20–50% match rate with a basic description, 90%+ with a well-tuned one. Treat it like API doc, not decoration."
  - "`argument-hint` is the spec that shows in the TUI when the user types the command."
  - "`model: sonnet` routes this skill to Sonnet — fast and cheap, fine for mechanical scaffolding. Use `opus` when the skill needs to reason deeply."

### 3. Variation: `disable-model-invocation` *(IDE — `deploy/SKILL.md`)*
- **Point at**: the `disable-model-invocation: true` line in the frontmatter
- **Say**: "This skill is invisible to Claude — its description isn't even loaded into context, so Claude can never auto-invoke it. The user has to type `/deploy` themselves. Use it for anything destructive or with side effects."

### 4. Variation: `allowed-tools` *(IDE — `pr-prep/SKILL.md`)*
- **Point at**: `allowed-tools: Bash, Read, Grep`
- **Say**: "Restricts what the skill can do. No `Write`, no `Edit` — even if Claude thinks it should modify a file from inside this skill, the harness blocks it. Useful for skills that are supposed to inspect, not mutate."

### 5. Body feature: dynamic context `!`cmd`` *(IDE — `pr-prep/SKILL.md`)*
- **Point at**: the "Pre-flight context" block (`!`git status --short``, `!`git log --oneline -10``, etc.)
- **Say**: "Backticks with a leading `!` execute at invocation time, BEFORE Claude reads the skill body. The output gets injected into the skill — Claude sees the rendered branch/log/diff as part of its context, no extra tool calls needed."

### 6. Live demo *(Terminal — Claude TUI)*
- **Type**: `/scaffold-endpoint POST /api/events/search`
- **What ties back to frontmatter**:
  - The slash command resolves because of `name`
  - `argument-hint` shows the expected `<METHOD> <PATH>` form as you type
  - `$ARGUMENTS` in the skill body gets substituted with `POST /api/events/search`
- **What audience sees**: route handler + Pydantic request/response models + test stub generated in seconds

### 7. Built-in skills *(talk only)*
- **Say**: "Five ship with Claude Code: `/simplify` (parallel review of recent changes), `/loop` (run a prompt on interval), `/batch` (parallelize work across worktrees), `/debug`, `/claude-api`. Note: `/review` is deprecated — install the `code-review` plugin instead via `claude plugins add code-review@claude-plugins-official`."

## Part 4 — MCP

The point: MCP is a config + auth that abstracts external tool APIs into something Claude can call as if it were native.

### 1. Config walkthrough *(IDE — open `.claude/.mcp.json`)*
- **Point at**: the single `atlassian` entry — `command: uvx`, `args: ["mcp-atlassian"]`, and the `${JIRA_API_TOKEN}`-style env-var references
- **Say**: "One block of JSON. The `${VAR}` references are the difference between sharing config and sharing secrets — the file gets committed, the values don't. Each user's shell environment provides their own tokens at startup."
- **Critical caveat**: Claude Code does NOT auto-load `.env` files. Variables must be in the shell when you launch `claude`. Either export them in your shell rc, `source .env` first, or use `direnv`. If a required `${VAR}` isn't set, Claude Code refuses to parse the config and the server doesn't start.

### 2. Live tool-call demo *(Terminal — Claude TUI)*
- **Type**: *"Fetch the latest open Jira ticket assigned to me and summarize it."* (or any Jira/Confluence prompt that fits your account)
- **What audience sees**:
  - A visible MCP tool call in the trace (e.g., `mcp__atlassian__jira_search`)
  - Claude weaving the returned data into a plain-English response
  - No code, no API knowledge from the user — just English in, summarized result out
- **Say**: "From Claude's side, MCP tools look identical to native tools. From your side, the protocol disappears — you ask in English, Claude figures out which tool to call, the server handles auth and formatting. That's the whole point of MCP."

## Part 5 — Hooks

Three beats: structure → deterministic block → AI-judgment block.

### 1. File tour *(IDE — split view)*
- **Open**: `.claude/settings.json` (hooks block) and `.claude/hooks/block-secrets.sh`
- **Say**: "Hooks are shell scripts that fire at specific points in Claude's lifecycle. The settings.json wires them to events; the script does the work. The script reads stdin JSON (the tool input), inspects it, exits 0 to allow or 2 to block. That's it."

### 2. Trigger A — `command` hook (the deterministic block) *(Terminal — Claude TUI)*
- **Setup** (pre-staged before workshop): `cp .env.example .env && git add .env`
- **Type**: *"Commit my staged changes."*
- **What audience sees**: Claude tries `git commit`, the `block-secrets.sh` hook fires, exits 2, the `BLOCKED: refusing to commit files that look like secrets:` message surfaces in stderr, commit is cancelled.
- **Say**: "Exit code 2 is the kill switch. Unlike CLAUDE.md guidance which Claude *might* follow, a hook with exit 2 makes the action impossible. Same hook fires every time, no exceptions."

### 3. Trigger B — `agent` hook (the wow) *(Terminal — same flow continues)*
- **Trigger**: same `git commit` attempt (or stage clean changes and try again)
- **What audience sees**: after the command hooks clear, an `agent` hook fires — a fresh subagent reads `git diff --cached`, evaluates it against rules in the prompt (debug prints, missing tests, breaking API changes, etc.), and emits one line: `APPROVE: <reason>` or `BLOCK: <reason>`.
- **Say**: "Deterministic trigger, AI-level judgment. The first hook is regex-and-grep — it catches what you anticipated. The agent hook catches what you didn't think of, because a model is reading the diff with reasoning. There are five hook types total — `command`, `prompt`, `agent`, `http`, `mcp_tool` — but `command` and `agent` are the two that matter for this audience."

## Part 6 — Subagents & Agent Teams

Two live beats. Agent Teams is slide-only — no demo.

### 1. File tour *(IDE — three tabs)*
- **Open**: `.claude/agents/security-scanner.md`, `pattern-explorer.md`, `test-generator.md`
- **Point at**: the frontmatter — `name`, `description`, `tools` (restricted toolset), `model` (e.g., `sonnet` for cheap/fast)
- **Say**: "Subagents are just markdown with YAML frontmatter, exactly like skills. Difference: a skill is a workflow Claude runs in the main conversation; a subagent runs in its OWN clean context window and reports back only the final summary. Same author experience, very different runtime."

### 2. Parallel demo *(Terminal — Claude TUI)*
- **Type**: *"Run security-scanner, pattern-explorer, and test-generator in parallel against `src/api/auth/login.py`. Merge their findings into one report."*
- **What audience sees**:
  - Three concurrent Task tool invocations in the trace
  - Each subagent reads files independently in its own isolated context — none of that read-noise pollutes the main conversation
  - Final output is the merged summary (security-scanner finds the SQL injection / plaintext password / missing rate limiting in `login.py` because of the FIXMEs we left there)
- **Say**: "Three context windows running at once, each on a clean slate. The main conversation only sees the merged result. This is how you keep big investigations from drowning your main session."

### 3. Agent Teams — *slide mention only, no demo*
- Reasons skipped: experimental flag, ~7× token cost, slow to spawn, low ROI for an intern Day-1 audience.
- On the slide: env var `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, shared task list, `SendMessage` between teammates, `Shift+Down` to cycle. 30-second mention, move on.

## Part 7 — Plugins

No live install. Walk the GitHub repo in a browser tab.

### 1. Marketplace overview *(Browser — open the repo)*
- **Open**: `github.com/compassanalytics/claude-compass-superpowers` (verify the path before the workshop — research found it 404'd via external fetch)
- **Show**: top-level README + `.claude-plugin/marketplace.json` (the manifest listing all plugins in this marketplace)
- **Say**: "A plugin marketplace is just a git repo with a manifest at `.claude-plugin/marketplace.json`. Anyone can publish one. This is Compass's internal marketplace; anyone on the team can contribute a plugin."

### 2. One plugin in detail *(Browser — drill into a folder)*
- **Open**: one plugin folder inside the repo (e.g., `general-dev/`)
- **Show**: its `.claude-plugin/plugin.json` manifest, then `skills/`, `agents/`, `hooks/`, `.mcp.json` if present
- **Say**: "Notice the structure — same `SKILL.md`, agent `.md`, hook scripts, MCP config we just walked through in this demo project. A plugin is literally a packaged version of a `.claude/` directory. If you wanted to install this you'd run `/plugin marketplace add compassanalytics/claude-compass-superpowers` then `/plugin install general-dev@compassanalytics`. Skipping that today — the point is you see how the pieces compose."

### 3. Marketplace catalog *(Browser — list view of plugins)*
- **Show**: the marketplace's plugin list — name, description, what each one does
- **Say a sentence per plugin** that exists (general-dev, ticket-driven-dev, deep-feature, deep-docs, agent-swarm, jira-compass, databricks-compass, dataiku-compass, skill-manager — confirm the current list before the workshop)
- **Say**: "Same structure as you've just seen, scaled up. Every one of these is a folder in this repo. You build one, push it, and your team installs it with one command."

## Part 8 — Permissions

Three live triggers + one verbal-only safety callout.

### 1. File tour *(IDE — `settings.json` permissions block)*
- **Point at**: the `allow` and `deny` lists; pattern syntax (`Tool(...)`, `*` wildcard, bare tool names)
- **Say**: "Three states. Allow = runs without asking. Deny = blocked, never runs. Anything else = prompts. Deny always wins on conflict, so a wide allow + narrow deny is safe."

### 2. Trigger A — deny fires *(Terminal — Claude TUI)*
- **Type**: *"Push my branch to main."*
- **Audience sees**: Claude tries `git push origin main`, the `Bash(git push *)` deny rule blocks it; reason visible.
- **Say**: "There's no way to override this from inside the session. Permanent floor."

### 3. Trigger B — allow-listed *(Terminal)*
- **Type**: *"Run pytest."*
- **Audience sees**: pytest fires immediately, no prompt.
- **Say**: "Allow-list the things you rubber-stamp every day. Less friction, no loss of safety — the deny list still catches what matters."

### 4. Trigger C — not on either list *(Terminal)*
- **Type**: something outside both lists, e.g., *"check disk usage with `du -sh .`"*
- **Audience sees**: Claude pauses and prompts the user.
- **Say**: "Default behavior. Build your allow list from the prompts you keep saying yes to."

### 5. `--dangerously-skip-permissions` — verbal only, NO demo
- **The flag**: `claude --dangerously-skip-permissions` disables allow/deny/prompt entirely. Claude runs every tool call without asking. The name is intentionally ugly — no `-y` shortcut.
- **Two non-obvious gotchas**:
  - Subagents inherit it. Can't override per-subagent.
  - Hooks still fire. A `PreToolUse` hook with `exit 2` still blocks even in bypass mode — hooks are above permissions.
- **Real-world cost**: Wolak Oct 2025 — `rm -rf` from root on a firmware project; OS file permissions were the only save. 32% of bypass-mode users hit unintended file modifications; 9% reported data loss.
- **Safe path**: container only. Mention `claude-yolo` (Compass's Docker sandbox) as the way to run autonomously without nuking your laptop.

## Closing
- *No demo. Slide only.*
