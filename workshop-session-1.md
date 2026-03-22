# Session 1: Claude Code — From Basics to Power User

**Format:** Presentation + discussion (not hands-on — that's Session 2)
**Duration:** ~90-100 min (adjust per section)
**Audience:** Developers who have used Claude Code in a basic capacity

---

## Part 1: The Evolution — From Autocomplete to Agent Orchestration (~20 min)

### The journey (substantiated, not hand-wavy)

Tell the story of how we actually got here, because the speed of this shift is genuinely remarkable.

**Phase 1: Autocomplete (2021-2022) — "IntelliSense on steroids"**
GitHub Copilot launches mid-2021, built on OpenAI's Codex. For the first time, AI is predicting entire lines and blocks of code from context. Impressive, but fundamentally passive — you type, it suggests, you accept or reject. Every decision is still yours. The developer drives every keystroke.

**Phase 2: Conversational coding (2023-early 2024) — "Ask it, don't just type"**
ChatGPT (late 2022) and GPT-4 (March 2023) change the interface. Copilot Chat arrives. AI stops being just inline suggestions and becomes a second interface for coding — you can ask for patterns, debug explanations, scaffolding, alternative implementations. Cursor launches (March 2023) as a VS Code fork with AI baked in. At this stage it's still chat + autocomplete — powerful, but the developer drives everything. Quality control is entirely human.

**Phase 3: Agentic coding emerges (late 2024-2025) — "Delegate, don't dictate"**
This is where the paradigm actually shifts. Cursor ships Agent Mode (November 2024) — the AI can now read terminal output, run commands, make multi-file changes, and iterate on errors inside the IDE. Claude Code launches (February 2025) as terminal-native: no IDE at all, just an agent that reads your codebase, plans, executes, and loops. Copilot adds agent mode (May 2025). Codex, Windsurf, and others follow. The AI isn't suggesting code anymore — it's *executing tasks*. You describe intent; the agent handles execution. By late 2025, Cursor reports a dramatic flip: where they once had 2.5× more tab-completion users than agent users, they now have 2× more agent users than tab users.

**The key distinction here:** agentic isn't one tool — it's a mode of working that all the major players converged on roughly simultaneously. Cursor does it inside the IDE. Claude Code does it in the terminal. Copilot does it across GitHub. Different interfaces, same fundamental shift from "you type, AI suggests" to "you describe, AI executes."

**Phase 4: Multi-agent orchestration (early 2026 — where we are now)**
Agent teams, parallel execution, peer-to-peer communication between agents. One lead coordinates, teammates work independently with their own context windows. We've gone from "AI autocomplete" to "managing a team of AI engineers" in under 5 years.

### Where we actually are right now — the numbers

Ground this in real data, not vibes. Pull from Anthropic's 2026 Agentic Coding Trends Report, the Sonar State of Code survey, Stack Overflow, and independent studies:

- **84%+ of developers** are now using or planning to use AI coding tools (Stack Overflow 2025). 51% of professional developers use AI daily.
- **64% of developers** have started using agentic AI tools specifically — 25% regularly, another 39% experimenting (Sonar State of Code 2026).
- **41% of all code** is now estimated to be AI-generated (global estimates, early 2026).
- **Developers save ~3.6 hours/week** on average; daily users save more. 75% say AI reduces "toil work" (DX Q4 2025 report, 135k+ developers).
- **But only 0-20% of tasks** are fully delegated to AI — most work is still collaborative, not autonomous (Anthropic's own report).
- **22% of merged code** is AI-authored based on actual repo telemetry (DX analysis).
- GitHub study of 129K+ projects found **15-22% agent adoption** — remarkable for technology only months old.

**Enterprise case studies that landed:**
- Rakuten: Claude Code completed activation vector extraction across a 12.5M-line codebase in 7 autonomous hours, achieving 99.9% numerical accuracy
- TELUS: 13,000+ custom AI solutions, engineering code shipped 30% faster, 500,000 total hours saved
- Zapier: 89-97% AI adoption across their *entire* organization, not just engineering
- Stripe: Cursor adoption went from single digits to over 80% of developers
- Salesforce: 90% of 20,000 developers using AI coding tools

### Where it's all headed

This section gives people a reason to invest in learning the tooling properly.

**The near-term (2026):** Agents are progressing from short tasks to work that continues for hours or days. Multi-agent coordination is becoming standard — not just parallelism, but agents that share findings, challenge each other, and coordinate independently. Non-engineers (security, ops, design, data, legal, marketing) are starting to build their own tools using agents.

**The convergence:** Compare Claude Code, Codex, Copilot CLI, Gemini CLI, Cursor, Windsurf — they're all converging on the same architecture under the hood. Config files (CLAUDE.md / AGENTS.md), tool use, multi-step planning, agent delegation. The open standard (MCP for tools, Agent Skills spec for skills) means skills work across Claude Code, Codex CLI, Gemini CLI, and Cursor without modification. This isn't a walled garden; the ecosystem is standardizing.

**The role shift:** Anthropic's report frames it bluntly — engineering is shifting from writing code to *orchestrating agents that write code*. The developer becomes a conductor, not a composer. The gap between "person who prompts a chatbot" and "person who orchestrates an AI workforce" is widening fast. That's what this workshop is about — making sure everyone in the room is on the right side of that gap.

**Be honest about the current limitations too:**
- Developers still fully delegate only 0-20% of tasks — this isn't "AI replaces you," it's "AI amplifies you"
- CodeRabbit's analysis found ~1.7× more issues in AI-coauthored PRs — verification matters
- Long sessions suffer from context rot; assumptions compound
- 75% of devs still manually review every AI snippet before merging
- The tools are powerful but need proper setup to be reliable — which is exactly what the rest of this session covers

---

## Part 2: The Configuration & Context Layer (~20-25 min)

This is where "I type prompts and hope" becomes "I've built an environment where the agent consistently does good work."

### 2a. CLAUDE.md — Your onboarding doc for the agent

**What it is:** A markdown file Claude reads at the start of every session. It's your persistent context — coding conventions, how to run tests, what not to touch, architectural decisions.

**The hierarchy (this matters):**
| File | Scope | Shared? |
|------|-------|---------|
| `~/.claude/CLAUDE.md` | Global, all projects | Personal |
| `./CLAUDE.md` or `./.claude/CLAUDE.md` | Project-level | Committed to git |
| `CLAUDE.local.md` | Project-level personal | Gitignored |

All levels combine — they don't replace each other. When there's a conflict, the more specific file wins. Anthropic's official guidance: **target under 200 lines per CLAUDE.md file.**

**Key insight:** Good CLAUDE.md files are boring on purpose. Short, specific, positive instructions. "Use named exports exclusively" beats "Do NOT use default exports" — LLMs are measurably worse at following negated instructions (KAIST, NeurIPS 2022 Workshop; Zhang et al., ACL 2023). Anthropic's own docs say: "Tell Claude what to do instead of what not to do."

**Common mistakes:**
- Over-specifying: 200+ lines where half get ignored because important rules get lost in the noise
- Mixing global preferences with project-specific context — the file becomes sludge
- Describing things Claude can already infer from the code

**Pro tip:** Run `/init` to generate a starter CLAUDE.md from your project structure, then ruthlessly prune. If Claude already does something correctly without the instruction, delete it.

### 2b. Rules — Scoped instructions for specific contexts

**What it is:** The `.claude/rules/` directory lets you split instructions into focused rule files instead of one massive CLAUDE.md.

**Why it matters:** When everything is high priority, nothing is. Instead of one 200-line CLAUDE.md where important rules get buried, you split instructions into focused files where each one covers one topic.

**How loading actually works (two-phase system — explain this clearly):**

1. **At startup:** Claude scans all `.md` files in `.claude/rules/` recursively. Rules **without** a `paths` field are loaded immediately and unconditionally — they behave like extra CLAUDE.md content, always in context.

2. **During the session:** Rules **with** a `paths` field are only *indexed* at startup (Claude reads the filename and frontmatter, not the full content). The actual rule body gets injected into context only when Claude reads or edits a file matching the glob pattern. So your API rules aren't consuming context tokens when you're working on React components.

**Path-scoping uses YAML frontmatter** — a small metadata block at the top of the markdown file:

```markdown
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All endpoints must validate input with Zod
- Return consistent error shapes
- Log all requests with correlation IDs
```

This rule only activates when Claude touches files matching `src/api/**/*.ts`. You can use glob patterns, brace expansion (`{ts,tsx}`), and multiple paths.

**Honest caveat for the workshop:** Path-scoped rules are still maturing. There have been real bugs — rules only triggering on file reads but not writes/creates, issues with user-level (`~/.claude/rules/`) path matching, and even the YAML examples in the official docs having invalid syntax at one point. Worth checking GitHub issues if something isn't working as expected. The `/memory` command lets you verify which rules are actually loaded.

```
.claude/rules/
├── code-style.md          # No paths → loads always
├── testing.md             # No paths → loads always
├── security.md            # No paths → loads always
├── frontend/
│   ├── components.md      # paths: ["src/**/*.tsx"] → loads on match
│   └── styling.md         # paths: ["**/*.css"] → loads on match
└── backend/
    ├── api.md             # paths: ["src/api/**/*.ts"] → loads on match
    └── database.md        # paths: ["**/migrations/**"] → loads on match
```

**When to use rules vs CLAUDE.md:** If it applies everywhere, every session — CLAUDE.md or an unscoped rule file. If it only matters for a subset of files — path-scoped rule. If it MUST happen deterministically every time — that's not a rule at all, that's a hook (covered later).

---

## Part 3: Skills & Commands (~10-15 min)

**What they are:** Directories containing a `SKILL.md` file with YAML frontmatter and markdown instructions. When invoked, the instructions load into Claude's context and Claude executes them. Skills can spawn subagents, accept arguments, and orchestrate multi-step workflows.

**Two ways skills get invoked:**

1. **Manual invocation (the primary way most people use them):** You type `/skill-name` as a slash command and Claude loads and runs it. This is reliable, predictable, and how built-in skills like `/simplify`, `/review`, `/batch` work. If you've written a custom skill, you invoke it the same way. This is the entry point for most people.

2. **Auto-invocation (probabilistic):** Claude can also trigger skills autonomously based on context — it scans skill names and descriptions at startup (~100 tokens each) and decides whether a skill is relevant to the current task. This is powerful in theory but inconsistent in practice. One practitioner measured ~50% auto-activation with basic setups. With forced evaluation hooks you can push it to ~80-84%, but it's never guaranteed.

**The key takeaway for the audience:** You can always invoke skills manually and they work reliably. Auto-invocation is a bonus when it fires, not something to depend on. If a behaviour absolutely must happen, use a hook — not a skill.

**How they load (context-efficient):** At startup, Claude reads only the name + description from each installed skill. The full instructions only load when the skill is actually invoked (manually or auto). So you can have dozens of skills installed without bloating your context on unrelated tasks.

**Commands vs Skills:** Historically these were separate systems (`.claude/commands/*.md` vs `.claude/skills/*/SKILL.md`). They've been merged — files in either location create the same `/slash-command` interface. Skills are the recommended approach going forward because they support features commands don't: supporting files (templates, scripts alongside the skill), frontmatter control, and auto-invocation.

**Built-in skills worth knowing:**
- `/simplify` — spawns 3 parallel review agents to check recently changed files for reuse, quality, efficiency
- `/review` — code review without leaving the terminal
- `/batch` — decomposes work into 5-30 independent units, spins up isolated git worktrees, executes in parallel, creates PRs
- `/loop` — iterative task execution
- `/debug` — systematic debugging

**Skills are an open standard.** The Agent Skills specification is adopted by Claude Code, Codex CLI, Gemini CLI, Cursor, and GitHub Copilot. A skill you write works across all of them without modification.

---

## Part 4: MCP — Connecting Claude to Everything (~10-15 min)

### What MCP actually is

**Model Context Protocol** — an open standard (developed by Anthropic, now adopted widely) that defines how AI assistants connect to external tools via a JSON-RPC-style protocol over stdio or HTTP.

**The mental model:** Without MCP, Claude Code can read files, run shell commands, and call the Anthropic API — nothing else. MCP servers are bridges that give Claude access to your tools, databases, and APIs. Each server exposes tools (callable functions) and optionally resources (readable data).

**Three primitives:** Resources (raw data like database records), Tools (actions like creating a GitHub PR), Prompts (reusable templates for workflows).

**Practical examples — what becomes possible:**
- "Implement the feature described in JIRA issue ENG-4521 and create a PR on GitHub"
- "Check Sentry and Statsig to check usage of this feature"
- "Find emails of 10 users who used feature X, based on our PostgreSQL database"
- "Update our email template based on the new Figma designs posted in Slack"

**Configuration scopes:**
- Local (default): stored in `~/.claude.json` under project path, private to you
- Project: `.claude/.mcp.json`, committed, shared with team
- User: `~/.claude.json`, available across all projects

**Adding servers:**
```bash
# HTTP (recommended for remote)
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Stdio (for local tools)
claude mcp add postgres --command "npx" --args "-y @modelcontextprotocol/server-postgres"
```

**Key ecosystem servers:** GitHub, Atlassian (Jira/Confluence), Notion, Figma, Supabase, Playwright (browser automation), PostgreSQL, filesystem, Context7 (live library docs), Slack, Google Workspace.

**When NOT to overdo it:** MCP servers add to context. The new MCP Tool Search feature enables lazy loading (reduces context usage by up to 95%), but don't connect 50 servers "just in case." Connect what you actually use.

---

## Part 5: Hooks — Deterministic Control (~10-15 min)

### The critical distinction

This is the single most important concept to land in this section:

> **Skills are probabilistic** — Claude uses judgment about whether to invoke them.
> **Hooks are deterministic** — they run every single time, zero exceptions.

Hooks are shell commands that execute at specific points in Claude Code's lifecycle. They don't ask Claude to do something — they *do* it. Every time.

### Anatomy of a hook

Three parts: an **event** (when does it fire?), a **matcher** (which tools trigger it?), and a **command** (what shell script runs?).

**Key events:** `PreToolUse` (before a tool runs — can block with exit code 2), `PostToolUse` (after completion), `Notification` (when Claude needs your attention), `Stop` (agent finishes), `SessionStart`, `UserPromptSubmit`, `ConfigChange`.

### Practical examples worth showing

**Desktop notification when Claude needs input** (the "go get coffee" hook):
```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
      }]
    }]
  }
}
```

**Block commits with sensitive files** (security guardrail):
A PreToolUse hook with exit code 2 that prevents committing `.env`, `.key`, `.pem` files. Exit code 2 is the kill switch — it gives you a hard stop Claude respects every time.

**Auto-format after edits:** PostToolUse hook on file writes that runs your formatter.

### When to use hooks vs. skills vs. CLAUDE.md

| Mechanism | Deterministic? | Use when... |
|-----------|---------------|-------------|
| CLAUDE.md | No (guidance) | General conventions, context Claude needs every session |
| Rules (`.claude/rules/`) | No (guidance) | File-type or path-specific conventions |
| Skills | No (probabilistic) | Complex workflows where Claude's judgment is acceptable |
| Hooks | **Yes** | Rules that MUST be followed 100% of the time — safety, formatting, notifications |

**The decision framework:** If it's a safety or compliance rule, use a hook. If it's a convention where Claude's judgment is acceptable, use a skill or CLAUDE.md. If you catch yourself thinking "Claude keeps ignoring this rule," promote it to a hook.

### Advanced: Prompt-based and agent-based hooks

Hooks aren't limited to shell scripts. You can use prompt-based hooks (an LLM evaluates a condition) or agent-based hooks (a Claude model decides) for decisions that require judgment but still need to happen deterministically at the right lifecycle point.

---

## Part 6: Subagents & Agent Teams (~15 min)

### 6a. Subagents — Isolated workers within your session

**What they are:** A subagent is a separate Claude instance that runs in its own context window, does a job, and returns only the results to your main conversation. Think of it like calling a specialist: you hand off a task, they work independently, and you get back a clean summary — not every file they read along the way.

**Why they exist (the context problem):** In a long session, your main context fills up with noise — every file Claude reads, every search result, every tool output. After an hour, Claude starts losing track of earlier decisions. Subagents solve this by doing heavy lifting in a separate context, keeping your main conversation clean and focused.

**How context flows:**
- **Parent → Subagent:** The only channel is the prompt string passed via the Agent tool. Whatever file paths, error messages, or decisions the subagent needs must be included in that prompt. The subagent does NOT inherit the parent's conversation history.
- **Subagent → Parent:** The subagent's final message returns verbatim as the tool result. All intermediate work (files read, commands run, search results) stays inside the subagent. The parent gets a summary, not the full trace.
- **Subagent inherits:** Project context (CLAUDE.md, skills, MCP servers), permissions from the parent session. But NOT the conversation history.
- **Key limitation:** Subagents cannot spawn other subagents — no infinite nesting.

**Built-in subagents (Claude uses these automatically):**
- **Explore** — read-only codebase search and analysis. Runs on Haiku for speed. Claude delegates here when it needs to search without making changes.
- **Plan** — gathers context before presenting a plan in plan mode.
- **General-purpose** — handles tasks needing both exploration and modification.

**Custom subagents** are defined as markdown files with YAML frontmatter in `.claude/agents/` (project-level) or `~/.claude/agents/` (user-level):

```markdown
---
name: security-scanner
description: Scans code for security vulnerabilities and OWASP issues
tools: Read, Grep, Glob
model: sonnet
---
You are a security specialist. Analyze the provided code for...
```

Key frontmatter fields: `name`, `description` (used for auto-invocation — same as skills), `tools` (restricts what the subagent can do), `model` (route to cheaper/faster models for simple tasks), `skills` (preload specific skills into the subagent's context).

**Two ways to invoke them:**
1. **Explicitly:** "Use the security-scanner subagent to review the auth module" or reference with `@security-scanner`
2. **Automatically:** Claude reads subagent descriptions and delegates when it thinks one fits — same probabilistic matching as skills

**When to use subagents vs. skills:**
- Use a **skill** when the work should happen in your main conversation and you want to see the process
- Use a **subagent** when the work would generate noise you don't need (codebase exploration, research, analysis) — keeps your main context clean
- A skill can also *fork into* a subagent using `context: fork` in its frontmatter — same logic, but running in isolation

### 6b. Agent Teams — Multi-session coordination

**What they are:** Agent teams take it a level further. Instead of subagents working within one session, agent teams coordinate *multiple independent Claude Code instances*. One session acts as the team lead, teammates work in their own sessions with their own context windows, and they communicate via a peer-to-peer mailbox system.

**The key difference from subagents:**

| | Subagents | Agent Teams |
|---|-----------|-------------|
| Context | Runs within parent session | Each has its own independent session |
| Communication | Reports back to parent only | Teammates message each other directly |
| Coordination | Parent relays everything | Peer-to-peer, no bottleneck |
| Setup | Automatic or explicit invocation | You describe the team, Claude spawns it |
| Status | Stable, production-ready | Experimental (feature flag required) |

**When teams genuinely help:**
- **Research and review:** Multiple teammates investigate different aspects simultaneously, then share and challenge findings
- **New modules/features:** Each teammate owns a separate piece without stepping on each other
- **Debugging with competing hypotheses:** Test different theories in parallel, converge faster
- **Cross-layer coordination:** Frontend, backend, and tests each owned by a different teammate

**When they're overkill:**
- Sequential tasks where each step depends on the previous
- Same-file edits (risk of conflicts)
- Simple tasks a single session handles fine
- Token budget matters: each teammate has its own context window, usage scales with team size (4-7× more tokens than single-agent sessions)

**Current state (experimental):**
- Behind a feature flag: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` in settings.json
- Requires Opus 4.6
- Display modes: in-process (default), split panes (tmux/iTerm2), auto-detect
- You describe the team in natural language — no config files, no agent schemas. Claude spawns and coordinates.
- Known limitations around session resumption, task coordination, and shutdown behavior

**The mindset shift:** You're not configuring agents — you're being a tech lead. Define clear tasks, provide rich context, monitor progress, steer when things drift. The teams that produce the best output are the ones with the most thoughtful human direction.

---

## Part 7: Plugins — Bundling It All Together (~5-10 min)

### What plugins solve

By this point in the workshop, the audience has seen skills, hooks, MCP servers, and subagents as individual concepts. **Plugins are the packaging layer** — they bundle any combination of these into a single installable unit that can be shared across projects and teams.

**What a plugin can contain:**
- Skills (slash commands, workflows)
- Subagents (custom agent definitions)
- Hooks (lifecycle automation)
- MCP servers (tool connections)
- All defined in a `plugin.json` manifest

```
my-team-plugin/
├── .claude-plugin/
│   └── plugin.json       # Manifest: name, description, version
├── .mcp.json              # MCP server config (optional)
├── commands/              # Slash commands (optional)
├── agents/                # Subagent definitions (optional)
├── skills/                # Skill definitions (optional)
└── README.md
```

**When to use a plugin vs. individual files:** If it's just for one repo, keep things in `.claude/`. If you need the same workflow across multiple projects or across your team, bundle it into a plugin.

**The plugin ecosystem (as of March 2026):**
- Official Anthropic marketplace (`claude-plugins-official`) — automatically available
- Community marketplaces — 43+ marketplaces, 834+ plugins catalogued
- Install via `/plugin marketplace add <owner/repo>`, then `/plugin install <name>`
- Scopes: user (personal, all projects), project (committed, team-shared), local (personal, this repo only), managed (admin-deployed)

**Worth mentioning briefly:** The official marketplace includes LSP plugins (language server protocol) that give Claude real code intelligence — jump to definition, find references, see type errors immediately after edits. These are configured per-language and require the language server binary installed on your system.

---

## Part 8: Permissions & `--dangerously-skip-permissions` (~10 min)

### The permission system

Claude Code asks for permission before executing potentially dangerous operations — bash commands, file modifications, network operations, dependency installation. This is correct from a security standpoint, but creates real workflow friction.

**The permission fatigue problem:** In practice, Claude asks ~100 permissions/hour. It becomes impossible to evaluate whether each one is dangerous — you end up rubber-stamping without reading. One LessWrong commenter pointed out this creates a false sense of security that may be *worse* than no permissions at all.

### The 5 permission modes

1. **Default** — prompts for everything potentially dangerous
2. **Auto-accept (Shift+Tab)** — proceeds without pausing, but remains interactive (you can still see and intervene)
3. **AllowedTools whitelist** — configure specific tools/commands in `settings.json` that don't need approval
4. **Deny rules** — explicitly block specific tools/commands (takes precedence over allow)
5. **`--dangerously-skip-permissions` (Bypass/YOLO mode)** — disables ALL permission checks

### The flag everyone's curious about

`--dangerously-skip-permissions` does exactly what it says. No confirmation dialogs, no pauses. It's technically equivalent to `--permission-mode bypassPermissions`.

**Critical details most people miss:**
- Subagent inheritance: ALL subagents inherit full autonomous access. You can't override this.
- The name is deliberately scary — there's no short alias, no `-y` shortcut. You type the full thing every time.
- Hooks still fire even in bypass mode — a PreToolUse hook can block a tool call regardless of permission mode.

**The real risks (not theoretical):**
- The Wolak incident (Oct 2025): Claude Code executed `rm -rf` from root on a firmware project. Error logs showed thousands of "Permission denied" messages for system paths. The command tried to delete everything.
- A study found 32% of developers using the flag encountered unintended file modifications; 9% reported data loss.

**When it's actually appropriate:**
- Inside a Docker container or VM with no access to your real machine (Anthropic's own recommendation)
- With `--network none` to prevent external connections
- With git checkpoints before every session
- For well-scoped tasks with clear specifications and test-driven verification
- Anthropic's own engineers use it — but their blog post about building a C compiler with parallel Claudes includes the parenthetical: "(Run this in a container, not your actual machine.)"

**The better alternative for most people:** Configure granular `AllowedTools` in `settings.json`. Allow common dev commands, deny dangerous ones. You get 90% of the speed without the risk:
```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Bash(git commit *)", "Bash(* --version)"],
    "deny": ["Bash(git push *)", "Bash(rm -rf *)"]
  }
}
```

---

## Closing: Tying it all together (~5 min)

### The layered architecture

Show this as the takeaway mental model:

```
┌─────────────────────────────────────────────────┐
│  Agent Teams (experimental, multi-session)       │
├─────────────────────────────────────────────────┤
│  Subagents (isolated workers, own context)       │
├─────────────────────────────────────────────────┤
│  Plugins (bundled shareable packages)            │
├─────────────────────────────────────────────────┤
│  MCP Servers (external tool connections)         │
├─────────────────────────────────────────────────┤
│  Hooks (deterministic lifecycle control)         │
├─────────────────────────────────────────────────┤
│  Skills (probabilistic prompt-based)             │
├─────────────────────────────────────────────────┤
│  Rules (.claude/rules/ - scoped guidance)        │
├─────────────────────────────────────────────────┤
│  CLAUDE.md (persistent project context)          │
├─────────────────────────────────────────────────┤
│  Permissions (safety & access control)           │
└─────────────────────────────────────────────────┘
```

Each layer builds on the one below. You don't need all of them on day one — start with a good CLAUDE.md, add hooks for things that must be deterministic, connect MCP servers for your actual tools, and build up from there.

### The deterministic vs. probabilistic mental model

This is the single most important thing to take away:

| Layer | Type | Guarantee |
|-------|------|-----------|
| CLAUDE.md / Rules | Guidance | Claude sees it, usually follows it |
| Skills | Probabilistic | Claude may auto-invoke, or you invoke manually |
| Subagents | Probabilistic | Claude may delegate, or you request it explicitly |
| Hooks | **Deterministic** | Runs every time, no exceptions |
| Permissions | **Deterministic** | Allow/deny enforced regardless of Claude's intent |

If something must happen 100% of the time → hook or permission rule.
If something should happen when relevant → skill, subagent, or CLAUDE.md.

### Bridge to Session 2

Session 2 will be hands-on: setting up a real project with CLAUDE.md, configuring hooks, connecting MCP servers, writing a custom skill, building a subagent, and (if time allows) spinning up an agent team. Encourage everyone to come with a real project or codebase they want to work with.