# Part 3: Skills & Commands

---

## Opening — What Skills Are (~2 min)

### The concept

Pick up from Part 2's closing:

> "So far we've covered how to give Claude persistent context — CLAUDE.md and Rules. That's the *knowledge* layer. Now we're moving to the *capability* layer. Skills teach Claude how to *do* things."

**A skill is a directory containing a `SKILL.md` file.** That file has YAML frontmatter (metadata) and markdown instructions. When invoked, the instructions load into Claude's context and Claude executes them.

Think of it this way:
- **CLAUDE.md** = "Here's how our project works" (knowledge)
- **Rules** = "Here's what to do when working on specific files" (scoped knowledge)
- **Skills** = "Here's a workflow you can run" (capability)

A skill can be as simple as a set of conventions Claude should follow, or as complex as a multi-step deployment pipeline with argument handling and subagent delegation.

---

## How Skills Load — The Context-Efficient Model (~3 min)

### Why this matters

Skills don't bloat your context. This is a key design point worth explaining:

**Diagram: How Skills Load**

```
SESSION START
─────────────────────────────────────────────────
Claude reads ONLY the name + description from each skill
(~100 tokens each)

  fix-issue:      "Fix a GitHub issue"           ← indexed
  deploy:         "Deploy app to production"      ← indexed
  api-conventions: "REST API design patterns"     ← indexed
  explain-code:   "Explain code with diagrams"    ← indexed

Total cost: ~400 tokens (trivial)
Full skill content: NOT loaded yet

─────────────────────────────────────────────────

SKILL INVOKED (manual or auto)
─────────────────────────────────────────────────
You type: /fix-issue 1234
  OR
Claude decides fix-issue is relevant to your request

  → Full SKILL.md content loads into context
  → Claude executes the instructions
─────────────────────────────────────────────────
```

**The takeaway:** You can have dozens of skills installed without paying a context cost on unrelated tasks. Only the one that's invoked loads fully. This is the same progressive disclosure pattern we saw with path-scoped rules — load metadata cheaply, inject content on demand.

---

## Two Ways Skills Get Invoked (~3 min)

### Manual invocation — the reliable path

You type `/skill-name` as a slash command. Claude loads the full skill content and executes it. This is predictable, reliable, and how most people use skills day-to-day.

```
/fix-issue 1234
/deploy staging
/explain-code src/auth/login.ts
/simplify
```

Arguments after the skill name get passed through. The skill can reference them with `$ARGUMENTS` (all args) or `$ARGUMENTS[0]`, `$ARGUMENTS[1]` (by position), or the shorthand `$0`, `$1`.

### Auto-invocation — the probabilistic path

Claude can also trigger skills on its own. At startup, it reads all skill descriptions. During the session, if your request matches a skill's description closely enough, Claude loads and runs it automatically.

**Example:** You have a skill called `api-conventions` with description "REST API design patterns for this codebase." You ask Claude to "build a new endpoint for user profiles." Claude reads the description, decides it's relevant, and loads the skill before writing the endpoint.

### Be honest about the reliability

> "Auto-invocation is powerful when it fires, but it's not something to depend on. One practitioner measured about 50% auto-activation with basic setups. With careful description writing you can push that higher, but it's never guaranteed."
>
> "The practical rule: **manual invocation always works. Auto-invocation is a bonus.** If a behavior absolutely must happen, that's not a skill — that's a hook."

### Controlling who invokes what

Two frontmatter fields give you precise control:

**Show this table:**

| Setting | You can invoke | Claude can invoke | When to use |
|---------|---------------|-------------------|-------------|
| (default) | Yes | Yes | Most skills — conventions, explanations, analysis |
| `disable-model-invocation: true` | Yes | No | Side effects — deploy, commit, send messages |
| `user-invocable: false` | No | Yes | Background knowledge — legacy system context, domain rules |

**The key insight:** Use `disable-model-invocation: true` for anything with side effects. You don't want Claude deciding to deploy because your code looks ready. You don't want Claude sending a Slack message because it thinks someone should know. **You** decide when those things happen.

---

## Anatomy of a Skill (~3 min)

### The SKILL.md structure

Every skill is a directory with a `SKILL.md` file. The file has two parts: YAML frontmatter and markdown content.

```
my-skill/
├── SKILL.md           # Required — instructions + frontmatter
├── template.md        # Optional — templates Claude fills in
├── examples/
│   └── sample.md      # Optional — example outputs
└── scripts/
    └── validate.sh    # Optional — scripts Claude can execute
```

### Frontmatter fields

**Show the key fields (not all of them — focus on the ones people will actually use):**

```yaml
---
name: fix-issue                      # becomes /fix-issue
description: Fix a GitHub issue      # Claude uses this for auto-invocation
disable-model-invocation: true       # manual-only
allowed-tools: Read, Grep, Glob     # restrict what Claude can do
context: fork                        # run in a subagent (isolated context)
model: sonnet                        # use a specific model
---
```

| Field | What it does |
|-------|-------------|
| `name` | The slash command name. Defaults to directory name. Lowercase, hyphens, max 64 chars. |
| `description` | What the skill does. Claude uses this for auto-invocation decisions. **Write this well** — it's the most important field for auto-invocation. |
| `disable-model-invocation` | `true` = manual-only. Use for side effects (deploy, commit, send). |
| `user-invocable` | `false` = Claude-only. Use for background knowledge. |
| `allowed-tools` | Restrict tools. Great for read-only skills: `Read, Grep, Glob`. |
| `context` | `fork` = run in a separate subagent context. Keeps main conversation clean. |
| `agent` | Which agent runs the forked skill (`Explore`, `Plan`, `general-purpose`, or custom). |
| `model` | Route to a specific model. Use `sonnet` for fast/cheap tasks, `opus` for complex ones. |
| `argument-hint` | Shown during autocomplete: `[issue-number]`, `[filename] [format]`. |

### Where skills live

| Location | Path | Who can use it |
|----------|------|---------------|
| Personal | `~/.claude/skills/<name>/SKILL.md` | You, across all projects |
| Project | `.claude/skills/<name>/SKILL.md` | Anyone on the team (committed to git) |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where the plugin is enabled |
| Enterprise | Managed settings | Everyone in your org |

**Monorepo bonus:** Claude auto-discovers skills from nested `.claude/skills/` directories. If you're editing files in `packages/frontend/`, Claude also sees skills in `packages/frontend/.claude/skills/`.

---

## Practical Examples (~5 min)

### Example 1: A task skill — Fix a GitHub Issue

This is the "hello world" of useful skills. Manual-only, takes an issue number, follows a repeatable workflow.

```yaml
# .claude/skills/fix-issue/SKILL.md

---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
argument-hint: [issue-number]
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Use `gh issue view $ARGUMENTS` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking: `pnpm lint && pnpm typecheck`
7. Create a descriptive commit message referencing the issue
8. Push and create a PR with `gh pr create`
```

**Usage:** `/fix-issue 1234`

**Why `disable-model-invocation: true`?** This creates commits and PRs — side effects you want to control.

### Example 2: A reference skill — API Conventions

This one is auto-invocable. It's knowledge, not a task. Claude loads it whenever you're working on API code.

```yaml
# .claude/skills/api-conventions/SKILL.md

---
name: api-conventions
description: REST API design conventions for our services. Use when
  writing API endpoints, designing request/response schemas, or
  reviewing API code.
---

# API Conventions

- Use kebab-case for URL paths: `/user-profiles`, not `/userProfiles`
- Use camelCase for JSON properties
- Always include pagination for list endpoints (cursor-based, not offset)
- Version APIs in the URL path: `/v1/`, `/v2/`
- Error responses follow this shape:
  ```json
  {
    "error": { "code": "NOT_FOUND", "message": "User not found", "details": {} }
  }
  ```
- Validate all inputs with Zod schemas from `src/lib/schemas/`
- Include `X-Request-ID` header for correlation
```

**Why no `disable-model-invocation`?** This is reference knowledge. You *want* Claude to load it automatically when you're doing API work.

**Note the description:** It explicitly says "Use when writing API endpoints, designing request/response schemas, or reviewing API code." The more specific your description, the better Claude's auto-invocation decisions.

### Example 3: A forked skill — Deep Research

This skill runs in a subagent so the research doesn't clutter your main conversation.

```yaml
# .claude/skills/deep-research/SKILL.md

---
name: deep-research
description: Research a topic thoroughly in the codebase
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Use Glob to find all relevant files
2. Use Grep to search for related patterns and keywords
3. Read and analyze the key files
4. Summarize findings with specific file paths and line references
5. Note any inconsistencies or potential issues found
```

**Usage:** `/deep-research how authentication tokens are refreshed`

**Why `context: fork`?** Research reads lots of files. Without forking, all that file content fills your main context. With forking, the Explore agent does the heavy lifting in its own context and returns a clean summary.

### Example 4: A skill with dynamic context

Skills can run shell commands *before* Claude sees the content. The `!`command`` syntax executes at invocation time and injects the output.

```yaml
# .claude/skills/pr-summary/SKILL.md

---
name: pr-summary
description: Summarize the current pull request
context: fork
agent: Explore
---

## Pull Request Context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your Task
Summarize this pull request:
1. What changed and why
2. Key decisions made in the code
3. Potential risks or issues
4. Suggestions for reviewers to focus on
```

**What happens when you run `/pr-summary`:**
1. The `!`command`` blocks execute first (fetch PR data from GitHub)
2. The output replaces the placeholders
3. Claude receives the fully-rendered prompt with actual PR data
4. Claude analyzes and summarizes

This is **preprocessing**, not something Claude executes. Claude only sees the final result.

---

## Built-in Skills Worth Knowing (~3 min)

### The ones that ship with Claude Code

These are available in every session without any setup:

**`/simplify [focus]`** — The post-implementation cleanup tool.

After you've built something and it works, `/simplify` reviews your recently changed files and makes them better. It spawns **three parallel review agents**, each looking at the changes from a different angle:
- Code reuse opportunities
- Quality issues
- Efficiency improvements

It aggregates findings, fixes valid issues, and skips false positives. You get a mini code review without leaving the terminal.

```
/simplify
/simplify focus on memory efficiency
```

**`/batch <instruction>`** — The heavy hitter for large-scale changes.

Decomposes work into 5–30 independent units, spins up isolated git worktrees, and executes in parallel. Each agent implements its unit, runs tests, and opens a PR. Every `/batch` worker automatically runs `/simplify` before committing.

```
/batch migrate all React class components in src/ to functional components
/batch add input validation to all API endpoints in src/api/
```

**`/loop [interval] <prompt>`** — Run something repeatedly on a schedule.

Useful for polling deployments, babysitting PRs, or periodic checks.

```
/loop 5m check if the deploy finished
/loop 10m /simplify
```

**`/review`** — Code review without leaving the terminal. Complements `/simplify` — `/review` for correctness, `/simplify` for cleanliness.

**`/debug [description]`** — Troubleshoot your current session by reading the session debug log.

---

## Commands vs Skills — The Merger (~1 min)

### Quick historical note

> "If you've seen older tutorials or blog posts, they might mention `.claude/commands/` as a separate system. Historically, commands and skills were different things — commands were simpler markdown files, skills had directories and frontmatter."
>
> "They've been merged. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Your existing command files keep working."
>
> "**Going forward, use skills.** They support everything commands do, plus supporting files (templates, scripts alongside the skill), frontmatter control, and auto-invocation. There's no reason to create new commands."

---

## Skills Are an Open Standard (~1 min)

### The interoperability story

> "One more thing worth knowing: skills aren't locked to Claude Code. The Agent Skills specification is an open standard adopted by Claude Code, OpenAI Codex, Gemini CLI, Cursor, GitHub Copilot, Windsurf, and 20+ other tools."

**What this means practically:** A skill you write for Claude Code works in Cursor without modification. A skill someone published for Codex works in Claude Code. The SKILL.md format, the frontmatter metadata, the progressive disclosure pattern — all universal.

This isn't a walled garden. The ecosystem is standardizing around a shared format, which means:
- Skills you invest time writing are portable
- Community skills work across tools
- You're not locked into any one vendor

There are already community repositories with 500+ agent skills published and compatible across platforms.

---

## When to Use Skills vs Other Mechanisms (~2 min)

### The decision point

Wrap up Part 3 by placing skills in the bigger picture:

**Decision tree:**

```
"I want Claude to behave differently"
    │
    ├── "It should know something every session"
    │       → CLAUDE.md or unscoped Rule
    │
    ├── "It should know something for specific files"
    │       → Path-scoped Rule
    │
    ├── "It should be able to run a workflow"
    │   │
    │   ├── "I want to control when it runs"
    │   │       → Skill with disable-model-invocation: true
    │   │
    │   ├── "Claude should decide when it's relevant"
    │   │       → Skill with a good description (auto-invocable)
    │   │
    │   └── "It should run in isolation (heavy research, analysis)"
    │           → Skill with context: fork
    │
    └── "It MUST happen every single time, no exceptions"
            → Hook (covered next in Part 4)
```

### Bridge to Part 4

> "Everything we've covered — CLAUDE.md, Rules, Skills — is probabilistic. Claude sees the instructions, Claude usually follows them, but there's no hard guarantee. Sometimes Claude forgets. Sometimes context gets crowded and a rule gets lost."
>
> "Part 4 is where we cross the line from 'usually' to 'always.' Hooks are deterministic — they run every time, zero exceptions. If you've been thinking 'but what if Claude ignores my rule?' — hooks are the answer."
