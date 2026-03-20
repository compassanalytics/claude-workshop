# Part 5: Subagents & Agent Teams

---

## 5a: Subagents (~8 min)

### The Problem They Solve

Two hours into a session, you need Claude to research how authentication works elsewhere in the codebase. If Claude does that in your main conversation, it reads 30 files, runs a bunch of greps, and all that output floods your context. Your earlier planning and implementation notes get diluted.

Subagents solve this. A subagent is a separate Claude instance with its own context window. It does a job — research, analysis, code review — and returns only the final summary. Everything intermediate stays inside the subagent.

```
YOUR MAIN CONVERSATION
│
│  "Research how auth tokens work in our app"
│
│  → Subagent spawns (own context)
│    → Reads 15 files, greps for patterns
│    → Returns: "Auth uses JWT in httpOnly cookies.
│       Refresh via /api/auth/refresh with rotating
│       tokens. Session middleware validates every request."
│
│  Your context: clean. Just the summary.
```

### Context Rules

- **Parent → subagent:** Only the prompt string. The subagent does not inherit conversation history.
- **Subagent → parent:** Only the final message. All intermediate work stays inside.
- **Inherited:** Project context (CLAUDE.md, rules, MCP servers), permissions. Skills only if explicitly listed in the `skills` field.
- **Limitation:** Subagents cannot spawn other subagents.

### Built-in Subagents

| Agent | Model | Tools | Purpose |
|---|---|---|---|
| **Explore** | Haiku | Read-only | File discovery, code search. Three thoroughness levels. |
| **Plan** | Inherits | Read-only | Context gathering for plan mode |
| **General-purpose** | Inherits | All | Complex multi-step tasks |

When you ask "how does X work in our codebase?", Claude typically spawns an Explore subagent. The research happens in a separate context; you get a clean answer.

### Custom Subagents

Markdown files with YAML frontmatter in `.claude/agents/` (project) or `~/.claude/agents/` (personal):

```markdown
# .claude/agents/security-scanner.md

---
name: security-scanner
description: Scans code for security vulnerabilities and OWASP issues.
  Use proactively after code changes in auth or payment modules.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior security engineer. Analyze the provided code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Auth and authorization flaws
- Secrets or credentials in code
- Missing input validation

Provide file paths, line numbers, and suggested fixes.
Rate each finding: Critical, Warning, or Info.
```

Key frontmatter fields: `name`, `description` (drives auto-delegation — same as skills), `tools` (restrict capabilities), `model` (route to cheaper models for simple tasks), `memory` (`user`/`project`/`local` for persistent cross-session learning), `isolation` (`worktree` for isolated git worktree), `hooks` (lifecycle hooks scoped to this subagent).

Invoke with natural language ("use the security-scanner to review src/auth/") or `@security-scanner`. Claude also auto-delegates based on descriptions — same probabilistic matching as skills.

Run `/agents` to view, create, edit, and delete subagents.

### When to Use Subagents

Use the main conversation when you need back-and-forth or quick targeted changes. Use a subagent when the task produces verbose output you don't need in context — research, exploration, analysis — or when you want to enforce tool restrictions.

---

## 5b: Agent Teams (~8 min)

### From Subagents to Teams

Subagents are isolated workers within one session. They report back to you and can't talk to each other. Agent teams are different: multiple independent Claude Code sessions, each with their own context window, communicating directly with each other.

| | Subagents | Agent Teams |
|---|---|---|
| **Context** | Within parent session | Each has its own session |
| **Communication** | Reports to parent only | Teammates message each other directly |
| **Coordination** | Parent manages everything | Shared task list, self-coordination |
| **Token cost** | Lower (summarized results) | ~7x a standard session ([costs docs](https://code.claude.com/docs/en/costs)) |
| **Status** | Stable | **Experimental** (feature flag) |

### How They Work

One session is the team lead. It spawns teammates — separate Claude Code instances. Each teammate has its own context window. They load the same project context (CLAUDE.md, rules, MCP servers) but not the lead's conversation history.

**Key components:**
- **Task list** — shared file on disk. Tasks have states (pending, in progress, completed) and can have dependencies.
- **Mailbox** — `SendMessage` for direct peer-to-peer communication. Teammates coordinate without going through the lead. "I changed the API response shape — here's the new type. Update your frontend components."

### When Teams Help

- **Research and review:** Multiple investigators apply different lenses simultaneously
- **New features:** Each teammate owns a separate layer without stepping on each other
- **Competing hypotheses:** Test different theories in parallel. The debate structure fights anchoring bias.

When they're overkill: sequential tasks, same-file edits (merge conflicts), simple tasks, tight token budgets.

### Setup

Agent teams are experimental. Enable:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Launch in natural language:

```
Create a team to refactor the auth module.
Spawn three teammates:
- One for the backend auth service
- One for the frontend login flow
- One for integration tests
Require plan approval before they make changes.
```

Claude spawns the teammates, creates a shared task list, and begins coordinating. Use **Shift+Down** to cycle through teammates. Split pane mode (`"teammateMode": "tmux"` in settings) gives each teammate its own pane if you're in tmux or iTerm2.

### Practical Guidance

**Team size:** 3-5 teammates. More isn't better — coordination overhead grows. 5-6 tasks per teammate.

**Model choice:** Use Sonnet for teammates. The docs recommend it for balancing capability and cost. The lead can use Opus for coordination.

**Avoid file conflicts:** Break work so each teammate owns different files.

**Give rich context in spawn prompts:** Teammates don't inherit the lead's history. Include everything they need.

### Current Limitations ([teams docs](https://code.claude.com/docs/en/agent-teams))

- Behind a feature flag, experimental
- No session resumption for in-process teammates
- Task status can lag — teammates sometimes forget to mark tasks complete
- One team per session
- No nested teams
- Shutdown can be slow — teammates finish current work before stopping
- Token costs scale linearly with team size (~7x for a full team in plan mode)

The architecture is sound. The rough edges will smooth out with updates.

---

## The Full Stack (~1 min)

```
┌─────────────────────────────────────────────┐
│  Agent Teams (experimental, multi-session)   │
├─────────────────────────────────────────────┤
│  Subagents (isolated workers, own context)   │
├─────────────────────────────────────────────┤
│  Hooks (deterministic lifecycle control)     │
├─────────────────────────────────────────────┤
│  Skills (probabilistic workflows)            │
├─────────────────────────────────────────────┤
│  Rules (scoped guidance)                     │
├─────────────────────────────────────────────┤
│  CLAUDE.md (persistent project context)      │
└─────────────────────────────────────────────┘
```

Each layer builds on the one below. Start with a good CLAUDE.md. Add hooks for things that must be deterministic. Grow from there.
