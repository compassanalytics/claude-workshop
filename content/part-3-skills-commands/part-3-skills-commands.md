# Part 3: Skills & Commands

---

## What Skills Are (~1 min)

CLAUDE.md and rules give Claude knowledge — what your project is, how it works, and what conventions to follow. Skills on the other hand give Claude capabilities to execute certain workflows. 

For example: You could have a skill that explores your codebase in a specific way and generates documentation that should follow a specific format, and include key points you want it to look for. A skill here would prevent you from having to rewrite the prompt each time, and it also helps ensure your agent is consistent with the way it approaches this task.

Now concretely, a skill is a directory with a `SKILL.md` file inside it. That's the only required file. The directory can also contain supporting files — templates, scripts, reference docs — anything Claude might need when executing the skill.

Skills live in `.claude/skills/<name>/SKILL.md`.

**Diagram:** See `skills-directory.svg` in this directory for the full layout.

---

## A Complete Example (~2 min)

Before we get into the details, here's what a skill actually looks like:

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

The top part between the `---` is frontmatter — metadata that controls how the skill behaves. The bottom part is the instructions Claude follows when the skill runs. You invoke it by typing `/fix-issue 1234`. We'll break down every piece in a moment.

---

## Invocation (~3 min)

Typically, when you start a new session, Claude reads only the `name` and `description` from each skill (~100 tokens each). The full body loads only when invoked. You can have dozens of skills installed without paying a context cost on unrelated tasks.

Two ways skills get triggered:

**Manual** — you type `/skill-name` as a slash command. Reliable, predictable.

```
/fix-issue 1234
/deploy staging
```

**Auto-invocation** — Claude decides on its own whether now is a good time to invoke a skill based on the current context and the skills description.

Reliability depends on description quality. Practitioner reports range from 20-50% with basic descriptions to 90%+ with well-tuned ones ([source](https://medium.com/@reliabledataengineering/claude-skills-2-0-the-self-improving-ai-capabilities-that-actually-work-dc3525eb391b)). The description is the single biggest factor.

The way you should see it is auto-invocation is an added bonus. If you want your skill to run, then you may as well specify it manually.


**Controlling invocation:**

| Frontmatter | You can invoke | Claude can invoke | Use for |
|---|---|---|---|
| (default) | Yes | Yes | Reference knowledge, conventions |
| `disable-model-invocation: true` | Yes | No | Side effects — deploy, commit, send |
| `user-invocable: false` | No | Yes | Background knowledge Claude should auto-apply |

Skills with `disable-model-invocation: true` don't even have their description loaded into context — Claude can't see them at all.

---

## Anatomy — Frontmatter Fields (~3 min)

Now that you know how skills are invoked, here's what each frontmatter field does:

| Field | What it does |
|---|---|
| `name` | Slash command name. Defaults to directory name. |
| `description` | What the skill does. This is what Claude reads at startup to decide whether to auto-invoke. Write this well. |
| `argument-hint` | Tells the user what arguments the skill expects (e.g. `[issue-number]`). In the body, `$ARGUMENTS` gives you everything after the slash command, `$0`, `$1` give positional args. |
| `disable-model-invocation` | `true` = manual only. Use for anything with side effects (deploy, commit, send). |
| `allowed-tools` | Restrict what the skill can do. `Read, Grep, Glob` for read-only skills. |
| `context` | `fork` = run in a subagent. Keeps main conversation clean. |
| `model` | Route to a specific model. `sonnet` for fast/cheap, `opus` for complex. |

**Dynamic context** — skills can run shell commands at invocation time with `` !`command` `` syntax:

```markdown
## PR Context
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```

These execute before Claude sees the skill content. Claude receives the rendered output, not the commands.

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
