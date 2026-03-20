# Part 3: Skills & Commands

---

## What Skills Are (~2 min)

CLAUDE.md and rules give Claude knowledge — what your project is, how it works, what conventions to follow. Skills give Claude capabilities — workflows it can execute.

A skill is a directory containing a `SKILL.md` file with YAML frontmatter and markdown instructions. When invoked, the instructions load into Claude's context and Claude executes them. A skill can be a set of conventions, a multi-step deployment pipeline, or anything in between.

**How loading works:** At startup, Claude reads only the `name` and `description` from each skill (~100 tokens each). The full body loads only when invoked. You can have dozens of skills installed without paying a context cost on unrelated tasks. There's a budget: skill descriptions can consume up to 2% of the context window. Run `/context` to check for warnings if you have many skills ([skills docs](https://code.claude.com/docs/en/skills)).

---

## Invocation (~3 min)

Two ways skills get triggered:

**Manual** — you type `/skill-name` as a slash command. Reliable, predictable. Arguments after the name get passed through and are available as `$ARGUMENTS` (all) or `$0`, `$1` (positional).

```
/fix-issue 1234
/deploy staging
```

**Auto-invocation** — Claude reads skill descriptions at startup and decides to invoke one when your request matches. Reliability depends on description quality. Practitioner reports range from 20-50% with basic descriptions to 90%+ with well-tuned ones ([source](https://medium.com/@reliabledataengineering/claude-skills-2-0-the-self-improving-ai-capabilities-that-actually-work-dc3525eb391b)). The description is the single biggest factor.

Manual invocation always works. Auto-invocation is a bonus. If something must happen every time, that's a hook, not a skill.

**Controlling invocation:**

| Frontmatter | You can invoke | Claude can invoke | Use for |
|---|---|---|---|
| (default) | Yes | Yes | Reference knowledge, conventions |
| `disable-model-invocation: true` | Yes | No | Side effects — deploy, commit, send |
| `user-invocable: false` | No | Yes | Background knowledge Claude should auto-apply |

Skills with `disable-model-invocation: true` don't even have their description loaded into context — Claude can't see them at all.

---

## Anatomy of a Skill (~3 min)

```
my-skill/
├── SKILL.md           # Required — instructions + frontmatter
├── templates/         # Optional — templates, scripts, examples
└── scripts/
```

The frontmatter fields that matter:

```yaml
---
name: fix-issue
description: Fix a GitHub issue by implementing changes and creating a PR
disable-model-invocation: true
argument-hint: [issue-number]
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
context: fork
model: sonnet
---
```

| Field | What it does |
|---|---|
| `name` | Slash command name. Defaults to directory name. |
| `description` | What the skill does. Claude uses this for auto-invocation. Write this well. |
| `disable-model-invocation` | `true` = manual only. Use for anything with side effects. |
| `allowed-tools` | Restrict tool access. `Read, Grep, Glob` for read-only skills. |
| `context` | `fork` = run in a subagent. Keeps main conversation clean. |
| `agent` | Which subagent type when forked (`Explore`, `Plan`, `general-purpose`, or custom). |
| `model` | Route to a specific model. `sonnet` for fast/cheap, `opus` for complex. |

Skills live in `.claude/skills/<name>/SKILL.md` (project, committed) or `~/.claude/skills/<name>/SKILL.md` (personal). In monorepos, Claude auto-discovers skills from nested `.claude/skills/` directories.

**Dynamic context** — skills can run shell commands at invocation time with `` !`command` `` syntax:

```markdown
## PR Context
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```

These execute before Claude sees the skill content. Claude receives the rendered output, not the commands. This is preprocessing, not something Claude runs.

---

## A Complete Example (~2 min)

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
2. Search the codebase for relevant files
3. Implement the fix
4. Write and run tests
5. Run linting and type checking: `pnpm lint && pnpm typecheck`
6. Create a commit referencing the issue
7. Push and create a PR with `gh pr create`
```

Usage: `/fix-issue 1234`. Manual-only because it creates commits and PRs.

The pattern is the same for every skill: frontmatter declares metadata, body declares the workflow. A conventions skill looks identical except the body is a list of rules instead of steps, and you leave auto-invocation on so Claude loads it when relevant.

---

## Built-in Skills (~2 min)

Five ship with Claude Code ([skills docs](https://code.claude.com/docs/en/skills)):

| Skill | What it does |
|---|---|
| `/simplify [focus]` | Reviews recently changed files via three parallel agents checking reuse, quality, and efficiency. |
| `/batch <instruction>` | Decomposes work into 5-30 units, spins up isolated git worktrees, executes in parallel, opens PRs. |
| `/loop [interval] <prompt>` | Runs a prompt repeatedly on an interval. Defaults to 10 minutes. |
| `/debug [description]` | Reads the session debug log to troubleshoot your current session. |
| `/claude-api` | Loads Claude API reference material. Also auto-activates when code imports `anthropic` or `@anthropic-ai/sdk`. |

Note: `/review` is deprecated. Install the `code-review` plugin instead: `claude plugin install code-review@claude-code-marketplace` ([commands docs](https://code.claude.com/docs/en/commands)).

---

## Commands vs Skills (~30 sec)

Older tutorials mention `.claude/commands/` as a separate system. They've been merged — a file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy`. Existing command files keep working. Use skills going forward: they support directories for supporting files, frontmatter control, and auto-invocation.

---

## Open Standard (~30 sec)

Skills follow the [Agent Skills specification](https://agentskills.io) — an open standard with 32+ adopters including Claude Code, OpenAI Codex, GitHub Copilot, Cursor, Gemini CLI, and JetBrains Junie. A skill you write for Claude Code works in Cursor without modification.
