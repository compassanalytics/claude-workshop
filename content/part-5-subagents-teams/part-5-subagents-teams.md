# Part 5: Subagents & Agent Teams

---

## 5a: Subagents

### The Problem They Solve (~1 min)

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

---

### A Custom Subagent (~2 min)

Here's what a subagent definition looks like:

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

Same structure as a skill — frontmatter on top, instructions below. Lives in `.claude/agents/` (project) or `~/.claude/agents/` (personal).

Invoke with natural language ("use the security-scanner to review src/auth/") or `@security-scanner`. Claude also auto-delegates based on descriptions — same probabilistic matching as skills.

---

### How Context Flows (~2 min)

- **Parent → subagent:** Only the prompt string. The subagent does not inherit conversation history.
- **Subagent → parent:** Only the final message. All intermediate work stays inside.
- **Inherited:** Project context (CLAUDE.md, rules, MCP servers), permissions.
- **Not inherited:** Skills. You must explicitly list them in the `skills` frontmatter field to pass them into a subagent.
- **Limitation:** Subagents cannot spawn other subagents.

### Built-in Subagents

Claude uses these automatically — you don't need to define them:

| Agent | Model | Tools | Purpose |
|---|---|---|---|
| **Explore** | Haiku | Read-only | File discovery, code search. Three thoroughness levels. |
| **Plan** | Inherits | Read-only | Context gathering for plan mode |
| **General-purpose** | Inherits | All | Complex multi-step tasks |

When you ask "how does X work in our codebase?", Claude typically spawns an Explore subagent. The research happens in a separate context; you get a clean answer.

---

### Frontmatter Fields (~1 min)

| Field | What it does |
|---|---|
| `name` | How you reference the subagent. |
| `description` | Drives auto-delegation — same as skills. Write this well. |
| `tools` | Restrict what the subagent can do. `Read, Grep, Glob` for read-only. |
| `model` | Route to a specific model. `sonnet` for fast/cheap tasks. |
| `skills` | List of skills to inject into the subagent's context. Full content is loaded at startup. Subagents don't inherit skills — you must list them explicitly. |
| `isolation` | `worktree` = run in an isolated git worktree. |

Run `/agents` to view, create, edit, and delete subagents.

---

## 5b: Agent Teams

### From Subagents to Teams (~1 min)

Subagents are isolated workers within one session. They report back to you and can't talk to each other. Agent teams are different: multiple independent Claude Code sessions, each with their own context window, communicating directly with each other.

| | Subagents | Agent Teams |
|---|---|---|
| **Context** | Within parent session | Each has its own session |
| **Communication** | Reports to parent only | Teammates message each other directly |
| **Coordination** | Parent manages everything | Shared task list, self-coordination |
| **Token cost** | Lower (summarized results) | ~7x a standard session |
| **Status** | Stable | **Experimental** (feature flag) |

---

### How They Work (~2 min)

One session is the team lead. It spawns teammates — separate Claude Code instances. Each teammate has its own context window. They load the same project context (CLAUDE.md, rules, MCP servers) but not the lead's conversation history.

**Key components:**
- **Task list** — shared file on disk. Tasks have states (pending, in progress, completed) and can have dependencies.
- **Mailbox** — `SendMessage` for direct peer-to-peer communication. Teammates coordinate without going through the lead. "I changed the API response shape — here's the new type. Update your frontend components."

---

### Launching a Team (~2 min)

Agent teams are experimental. Enable in settings:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Then launch in natural language:

```
Create a team to refactor the auth module.
Spawn three teammates:
- One for the backend auth service
- One for the frontend login flow
- One for integration tests
Require plan approval before they make changes.
```

Claude spawns the teammates, creates a shared task list, and begins coordinating. Use **Shift+Down** to cycle through teammates.

---

### When Teams Help

- **Research and review:** Multiple investigators apply different lenses simultaneously
- **New features:** Each teammate owns a separate layer without stepping on each other
- **Competing hypotheses:** Test different theories in parallel

**When they're overkill:** sequential tasks, same-file edits (merge conflicts), simple tasks, tight token budgets.

---

### Practical Guidance

- **Team size:** 3-5 teammates. More isn't better — coordination overhead grows.
- **Model choice:** Sonnet for teammates, Opus for the lead.
- **Avoid file conflicts:** Break work so each teammate owns different files.
- **Give rich context in spawn prompts:** Teammates don't inherit the lead's history. Include everything they need.
- **Known rough edges:** experimental feature flag required, no session resumption for teammates, task status can lag, shutdown can be slow as teammates finish current work.

---
