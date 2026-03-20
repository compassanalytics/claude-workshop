# Part 5: Subagents & Agent Teams

---

## 5a: Subagents — Isolated Workers Within Your Session

### The Context Problem (~2 min)

#### Opening

> "Here's a scenario: you're two hours into a Claude Code session. You've been building a feature — planning, implementing, running tests, fixing bugs. Your context window is full of useful conversation history. Now you need to research how authentication works in another part of the codebase."
>
> "If Claude does that research in your main conversation, it reads 30 files, runs a bunch of grep searches, and all that output floods your context. Your earlier planning decisions, your implementation notes, your test results — they get pushed out or diluted. Claude starts losing track of what it was doing."
>
> "Subagents solve this. They do heavy lifting in a separate context window and return only the results."

### What Subagents Are (~2 min)

A subagent is a separate Claude instance that:
- Runs in its **own context window**
- Does a job (research, analysis, code review, implementation)
- Returns **only the final summary** to your main conversation
- Then stops

Everything that happened inside the subagent — every file read, every search, every intermediate thought — stays there. Your main conversation gets a clean result.

**The mental model:**

```
┌──────────────────────────────────────────────────┐
│  YOUR MAIN CONVERSATION                          │
│                                                  │
│  You: "Research how auth tokens work in our app" │
│                                                  │
│  Claude: "I'll delegate this to a subagent."     │
│          ┌────────────────────────────────┐      │
│          │  SUBAGENT (own context)        │      │
│          │                                │      │
│          │  Reads src/auth/token.ts       │      │
│          │  Reads src/auth/refresh.ts     │      │
│          │  Reads src/middleware/session.ts│      │
│          │  Greps for "jwt" across repo   │      │
│          │  Reads 12 more files...        │      │
│          │                                │      │
│          │  → Returns: "Auth uses JWT     │      │
│          │    stored in httpOnly cookies.  │      │
│          │    Refresh via /api/auth/       │      │
│          │    refresh with rotating        │      │
│          │    tokens. Session middleware   │      │
│          │    validates on every request." │      │
│          └────────────────────────────────┘      │
│                                                  │
│  Your context: clean. 15 file reads didn't       │
│  enter your conversation. Just the summary.      │
└──────────────────────────────────────────────────┘
```

### How Context Flows (~2 min)

This is important to understand — subagents are isolated by design.

**Parent → Subagent:**
- The only channel is the **prompt string** passed when spawning the subagent
- Whatever file paths, error messages, or decisions the subagent needs must be in that prompt
- The subagent does **NOT** inherit the parent's conversation history

**Subagent → Parent:**
- The subagent's **final message** returns verbatim as a tool result
- All intermediate work (files read, commands run, searches) stays inside the subagent
- The parent gets a summary, not the full trace

**What subagents DO inherit:**
- Project context (CLAUDE.md, rules, MCP servers)
- Permissions from the parent session
- Skills (only if explicitly listed in the subagent's `skills` field)

**Key limitation:** Subagents cannot spawn other subagents. No infinite nesting.

### Built-in Subagents (~2 min)

Claude uses these automatically — you don't need to configure them:

**Explore** — The fast scout.
- **Model:** Haiku (fast, cheap)
- **Tools:** Read-only (can't edit files)
- **Purpose:** File discovery, code search, codebase exploration
- Claude delegates here when it needs to search without making changes
- Three thoroughness levels: quick, medium, very thorough

> "When you ask Claude 'how does X work in our codebase?', it typically spawns an Explore subagent. The exploration happens in a separate context, and you get a clean summary. This is why codebase questions don't pollute your conversation."

**Plan** — The researcher for plan mode.
- **Model:** Same as main conversation
- **Tools:** Read-only
- **Purpose:** Gathering context before presenting a plan

**General-purpose** — The full capability worker.
- **Model:** Same as main conversation
- **Tools:** All tools (can edit, write, run commands)
- **Purpose:** Complex multi-step tasks

### Custom Subagents (~4 min)

#### Defining a subagent

Custom subagents are markdown files with YAML frontmatter in `.claude/agents/` (project) or `~/.claude/agents/` (personal):

```markdown
# .claude/agents/security-scanner.md

---
name: security-scanner
description: Scans code for security vulnerabilities and OWASP issues.
  Use proactively after code changes in auth or payment modules.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior security engineer. When invoked, analyze the
provided code for:

- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling
- Missing input validation

Provide specific file paths, line numbers, and suggested fixes.
Rate each finding: Critical, Warning, or Info.
```

#### Key frontmatter fields

| Field | What it does |
|-------|-------------|
| `name` | Unique identifier. Lowercase + hyphens. |
| `description` | When Claude should delegate to this subagent. **Write this well** — Claude uses it for auto-delegation decisions. |
| `tools` | Restrict what the subagent can do. `Read, Grep, Glob` for read-only. Omit to inherit all tools. |
| `disallowedTools` | Deny specific tools while keeping everything else. |
| `model` | `haiku` (fast/cheap), `sonnet` (balanced), `opus` (max capability), or `inherit`. |
| `permissionMode` | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`. |
| `maxTurns` | Cap the number of agentic turns before stopping. |
| `skills` | Preload specific skills into the subagent's context. |
| `memory` | `user`, `project`, or `local` — persistent memory across sessions. |
| `background` | `true` to always run in the background. |
| `isolation` | `worktree` to run in an isolated git worktree. |
| `hooks` | Lifecycle hooks scoped to this subagent. |

#### Two ways to invoke

**1. Natural language / @-mention:**
```
Use the security-scanner subagent to review the auth module
@security-scanner check src/payments/ for vulnerabilities
```

**2. Automatic delegation:**
Claude reads subagent descriptions and delegates when it thinks one fits. Same probabilistic matching as skills. Include "use proactively" in descriptions to encourage this.

#### Practical examples

**A cost-conscious researcher:**
```markdown
---
name: quick-lookup
description: Fast codebase lookups for simple questions
tools: Read, Grep, Glob
model: haiku
---

Answer the question concisely. Find the relevant file(s),
read them, and return a direct answer. No lengthy analysis.
```

Routes simple questions to Haiku — fast and cheap. Reserve Opus for complex work.

**A read-only database analyst:**
```markdown
---
name: db-analyst
description: Analyze database schemas and queries
tools: Bash, Read
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute
SELECT queries to answer questions about the data.
Never INSERT, UPDATE, DELETE, or modify schema.
```

Uses a hook to enforce read-only — even though the instructions say "never modify," the hook makes it physically impossible.

**A subagent with persistent memory:**
```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices.
  Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
memory: project
---

You are a code reviewer. Review changes for quality,
security, and maintainability.

Update your agent memory as you discover patterns,
conventions, and recurring issues. Check your memory
before starting each review for accumulated insights.
```

The `memory: project` field gives the subagent a persistent directory at `.claude/agent-memory/code-reviewer/`. Over time, it builds knowledge about your codebase that carries across sessions.

### When to Use Subagents vs Main Conversation (~1 min)

| Use main conversation when... | Use a subagent when... |
|------------------------------|----------------------|
| Frequent back-and-forth needed | Task produces verbose output you don't need |
| Multiple phases share context | Work is self-contained, returns a summary |
| Quick, targeted change | You want to enforce specific tool restrictions |
| Latency matters | Heavy research or exploration |

---

## 5b: Agent Teams — Multi-Session Coordination

### From Subagents to Teams (~2 min)

#### The step up

> "Subagents are isolated workers within one session. They report back to you and that's it. They can't talk to each other, share discoveries, or coordinate."
>
> "Agent teams are different. Multiple independent Claude Code sessions, each with their own context window, communicating directly with each other. One acts as the team lead. The rest are teammates working in parallel."

**Show the comparison:**

| | Subagents | Agent Teams |
|---|-----------|-------------|
| **Context** | Runs within parent session | Each has its own independent session |
| **Communication** | Reports back to parent only | Teammates message each other directly |
| **Coordination** | Parent manages everything | Shared task list, self-coordination |
| **Best for** | Focused tasks where only the result matters | Complex work requiring discussion and collaboration |
| **Token cost** | Lower (summarized results) | Higher (3-4x for a 3-person team) |
| **Status** | Stable, production-ready | **Experimental** (feature flag required) |

### How Teams Work (~3 min)

#### Architecture

```
┌──────────────────────────────────────────────┐
│                 TEAM LEAD                     │
│  (your main Claude Code session)             │
│                                              │
│  Creates team → Spawns teammates → Assigns   │
│  tasks → Synthesizes results                 │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Teammate A│←→│Teammate B│←→│Teammate C│  │
│  │          │  │          │  │          │  │
│  │ Frontend │  │ Backend  │  │  Tests   │  │
│  │ changes  │  │ changes  │  │          │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│       ↕              ↕             ↕         │
│  ┌──────────────────────────────────────┐   │
│  │         SHARED TASK LIST             │   │
│  │  □ Implement user profile page       │   │
│  │  ■ Create API endpoint (in progress) │   │
│  │  ✓ Write database migration (done)   │   │
│  └──────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
```

**Key components:**
- **Team lead:** Your main session. Creates the team, coordinates work, synthesizes results.
- **Teammates:** Separate Claude Code instances. Each has its own full context window. They load the same project context (CLAUDE.md, MCP, skills) but not the lead's conversation history.
- **Task list:** Shared file on disk. Tasks have states: pending, in progress, completed. Tasks can have dependencies.
- **Mailbox:** `SendMessage` tool for direct peer-to-peer communication. Teammates can message each other without going through the lead.

#### Communication model

This is the fundamental difference from subagents:

- **Subagents** can only report results back to the parent. To share a finding between two subagents, the parent has to relay it.
- **Teammates** message each other directly. "Hey, I changed the API response shape — here's the new type. Update your frontend components." No bottleneck.

### When Teams Help (~2 min)

**Strong use cases:**

- **Research and review:** Multiple teammates investigate different aspects simultaneously, then share and challenge findings
- **New modules/features:** Each teammate owns a separate piece without stepping on each other
- **Debugging with competing hypotheses:** Test different theories in parallel. The debate structure fights anchoring bias — one agent alone tends to find one plausible explanation and stop.
- **Cross-layer coordination:** Frontend, backend, and tests each owned by a different teammate

**When they're overkill:**

- Sequential tasks where each step depends on the previous
- Same-file edits (risk of merge conflicts)
- Simple tasks a single session handles fine
- Token budget is tight — each teammate has its own context window

### Starting a Team (~2 min)

#### Setup

Agent teams are experimental. Enable them:

```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

#### Launch in natural language

You describe the team, Claude creates it:

```
Create an agent team to refactor the authentication module.

Spawn three teammates:
- One to update the backend auth service
- One to update the frontend login flow
- One to write integration tests

Require plan approval before they make changes.
```

Claude spawns the teammates, creates a shared task list, and begins coordinating. You can interact with the lead to steer direction, or use **Shift+Down** to cycle through teammates and message them directly.

#### Display modes

- **In-process** (default): All teammates run in your terminal. Use Shift+Down to cycle. Works everywhere.
- **Split panes**: Each teammate gets its own pane. Requires tmux or iTerm2. Set `"teammateMode": "tmux"` in settings.

### Practical Examples (~3 min)

#### Example 1: Parallel code review

A single reviewer gravitates toward one type of issue. Split review criteria into independent domains:

```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

Each reviewer applies a different lens. The lead synthesizes across all three.

#### Example 2: Competing hypotheses debugging

When the root cause is unclear, make teammates adversarial:

```
Users report the app exits after one message instead of staying connected.
Spawn 5 teammates to investigate different hypotheses. Have them
talk to each other to try to disprove each other's theories, like
a scientific debate. Update findings with whatever consensus emerges.
```

> "The debate structure is the key mechanism. Sequential investigation suffers from anchoring — once one theory is explored, everything gets biased toward it. Multiple independent investigators actively trying to disprove each other produces more robust answers."

#### Example 3: Feature implementation with plan approval

```
Create a team to implement the invoice feature:
- Teammate 1: Database schema and migrations
- Teammate 2: API endpoints and business logic
- Teammate 3: React components and UI

Require plan approval. Each teammate should plan first,
and you (the lead) approve before implementation begins.
Have them coordinate on the data contract before coding.
```

The lead reviews each plan, ensures they align on shared interfaces, then approves implementation. Teammates communicate directly about the data contract.

### Best Practices (~2 min)

**Team size:** Start with 3-5 teammates. More isn't better — coordination overhead increases and returns diminish. 5-6 tasks per teammate keeps everyone productive.

**Avoid file conflicts:** Two teammates editing the same file leads to overwrites. Break work so each teammate owns different files.

**Give rich context in spawn prompts:** Teammates don't inherit the lead's history. Include everything they need in their task description.

**Monitor and steer:** Don't let a team run unattended too long. Check in, redirect approaches that aren't working, and synthesize as findings come in.

**The mindset shift:**

> "You're not configuring agents. You're being a tech lead. Define clear tasks, provide rich context, monitor progress, steer when things drift. The teams that produce the best output are the ones with the most thoughtful human direction."

### Current Limitations (~1 min)

Be upfront:

- **Experimental:** Behind a feature flag, requires Opus 4.6
- **No session resumption** for in-process teammates — if you resume a session, the lead may try to message teammates that no longer exist
- **Task status can lag** — teammates sometimes forget to mark tasks complete
- **One team per session** — clean up before starting a new team
- **No nested teams** — teammates can't spawn their own teams
- **Shutdown can be slow** — teammates finish their current work before stopping
- **Token costs scale linearly** — a 3-teammate team uses roughly 3-4x the tokens of a single session

> "These limitations are real, and they're the kind of thing that improves rapidly with updates. The feature is worth learning now because the architecture is sound — the rough edges will smooth out."

---

## Closing for Parts 2-5 (~1 min)

### The full picture so far

> "Let's step back and look at what we've covered — these are the four parts you need to go from 'person who uses Claude Code' to 'person who orchestrates Claude Code.'"

```
┌─────────────────────────────────────────────┐
│  Agent Teams (experimental, multi-session)   │
│  └─ Multiple Claude instances coordinating  │
├─────────────────────────────────────────────┤
│  Subagents (isolated workers, own context)   │
│  └─ Heavy lifting without polluting context │
├─────────────────────────────────────────────┤
│  Hooks (deterministic lifecycle control)     │
│  └─ Guarantees. Exit code 2 = hard stop.    │
├─────────────────────────────────────────────┤
│  Skills (probabilistic workflows)            │
│  └─ Capabilities Claude can run on demand   │
├─────────────────────────────────────────────┤
│  Rules (scoped guidance)                     │
│  └─ Load only when relevant files are open  │
├─────────────────────────────────────────────┤
│  CLAUDE.md (persistent project context)      │
│  └─ The foundation. Every session starts here│
└─────────────────────────────────────────────┘
```

> "Each layer builds on the one below. You don't need all of them on day one. Start with a good CLAUDE.md. Add hooks for things that must be deterministic. Grow from there."

**Hand off to the remaining sections** (MCP, Plugins, Permissions) which other presenters will cover.
