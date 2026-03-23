# Part 2a: CLAUDE.md — Your Onboarding Doc for the Agent

---

## Opening (~2 min)

### The hook

So we just saw how fast this has moved. The goal for the rest of this session is to lay the foundations and go over some of the basics that take you from just prompting, to creating an environment where your agent consistently does good work. The end goal is for you to spend less time prompting, and your agent less tokens correcting its own mistakes.

And so we're going to start with the simplest thing: Claude.md. Claude starts every session completely blank. No memory of yesterday. And you might want to persist some basic guidance and instructions that are relevant to your own and/or your project conventions, and that would apply to each and every session.

**CLAUDE.md fixes that.** Markdown file Claude reads at the start of every session all loaded before you type anything.

---

## The Hierarchy (~5 min)

### Where CLAUDE.md files live and how they combine

Now as you may know, CLAUDE.md is not a single file that lives on your computer. It can be defined at multiple levels. So how are they combined?

**Diagram:** See `gemini-svg.svg` in this directory for the visual version.

First of all, these are all layers that stack on top of one another. Anytime you start a new session, the global CLAUDE.md (`~/.claude/CLAUDE.md`) always loads no matter what project you're working on, and where you are on your computer.

Now if you're working on a project with a CLAUDE.md defined in the project root (`./CLAUDE.md`), then a new session loads both global and project CLAUDE.md.

And say you're also working on the backend of your application — a new session is going to stack that subdirectory CLAUDE.md (`./subdir/CLAUDE.md`) on top of the one in the project root, and on top of global.

If you have conflicting instructions at different levels, the more specific directory takes priority.

Now these files — anything at project level and below — are typically committed to git so they can be shared with your team. But say you'd like to add your personal touch and you don't want to share some instructions with the team. Then you would define a `CLAUDE.local.md` file, which is automatically gitignored. This is seen as a personal override, and these instructions will take priority over the shared ones at the same directory level.

---

## Writing a Good CLAUDE.md (~8 min)

### The golden rule

> For each line, ask: **"Would removing this cause Claude to make mistakes?"** If the answer is no, delete it.

CLAUDE.md is loaded into Claude's context every session. Every line you add competes for attention with every other line. Anthropic's official guidance is to **target under 200 lines per CLAUDE.md file** — longer files consume more context and reduce adherence.

The IFScale benchmark (Jaroslawicz et al., July 2025 — [arXiv:2507.11538](https://arxiv.org/abs/2507.11538)) tested 20 frontier models and found that even the best ones start falling off hard after about 150 instructions. Claude Code's own system prompt already eats a big chunk of that budget — your CLAUDE.md is drawing from what's left.

### What to include

So what actually goes into a good CLAUDE.md? Anthropic has a table on their [best practices page](https://code.claude.com/docs/en/best-practices) that lays this out, and the underlying logic is simple.

On the include side, it all comes down to one question: **can Claude figure this out on its own?** If the answer is no, it belongs in CLAUDE.md. Your build commands, your test runner flags, architectural decisions that aren't obvious from the code, environment quirks — Claude has no way to know these unless you tell it.

On the exclude side, it's the inverse. If Claude can read your code and figure it out — your file structure, standard language conventions, things like "write clean code" — don't waste context on it. And don't paste in long docs or tutorials. Link to them instead.

The golden rule: for each line in your CLAUDE.md, ask yourself — **would removing this cause Claude to make mistakes?** If the answer is no, delete it.

**Table from Anthropic's [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices) page:**

| ✅ Include | ❌ Exclude |
|-----------|-----------|
| Bash commands Claude can't guess | Anything Claude can figure out by reading code |
| Code style rules that differ from defaults | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners | Detailed API documentation (link to docs instead) |
| Repository etiquette (branch naming, PR conventions) | Information that changes frequently |
| Architectural decisions specific to your project | Long explanations or tutorials |
| Developer environment quirks (required env vars) | File-by-file descriptions of the codebase |
| Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

### The positive instruction principle

LLMs are measurably worse at following negated instructions. Research out of KAIST (Jang et al., NeurIPS 2022 — [arXiv:2209.12711](https://arxiv.org/abs/2209.12711)) found an inverse scaling law: larger models actually performed *worse* on negated prompts. Anthropic's own docs say it plainly: **"Tell Claude what to do instead of what not to do."** ([Claude Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices))

Frame instructions as what you want, not what you don't:

| ❌ Negative | ✅ Positive |
|------------|------------|
| Don't create new files if one exists | Make all changes in existing files |
| Don't push directly to main | Create a feature branch for all changes |
| Never hardcode secrets | Load secrets from environment variables |
| Avoid long functions | Keep functions under 40 lines, extract helpers |
| Don't leave TODO comments | Resolve TODOs before committing or file an issue |

**When negative instructions still make sense:** Hard safety boundaries. "NEVER commit .env files" or "NEVER expose API keys in client code." These are guardrails, not style preferences — and even then, a hook is more reliable than a CLAUDE.md instruction. We'll get to hooks later.

### Emphasis when it matters

If a rule is critical, you can add emphasis. Claude responds to signal words:

```markdown
IMPORTANT: Always run the type checker before committing.
YOU MUST use the shared API client from src/lib/api — do not create new HTTP clients.
```

Use this sparingly. If everything is "IMPORTANT," nothing is. Save emphasis for the 2-3 rules that really matter.

### The import syntax

CLAUDE.md files can reference other files using `@` syntax:

```markdown
See @README.md for project overview.
See @docs/api-conventions.md for API design rules.
```

This keeps your CLAUDE.md lean while still giving Claude access to detailed reference material. Claude reads the referenced file when it needs the content — it's not loaded upfront.

**Pro tip (from the [HumanLayer blog, Nov 2025](https://www.humanlayer.dev/blog/writing-a-good-claude-md)):** Prefer pointers over copies. Don't paste code snippets into CLAUDE.md — they go stale fast. Instead, point to the file: `"See @src/lib/api/client.ts for the canonical API client pattern."` Claude reads the current version.

---

## Getting Started (~2 min)

### `/init`

Run `/init` in Claude Code. It scans your project and generates a starter CLAUDE.md. Treat it as a first draft — it'll include stuff Claude can already figure out from your code (file structure descriptions, obvious conventions). Cut those.

### How it should evolve

A good CLAUDE.md grows from real friction, not upfront planning. Every time Claude makes a mistake, ask: "Would a one-line instruction have prevented this?" If yes, add it. Every time Claude keeps asking you something, that's a missing instruction. Commit it to git so the whole team benefits and iterates on it together.

The [HumanLayer blog (Nov 2025)](https://www.humanlayer.dev/blog/writing-a-good-claude-md) makes a good point here — their root CLAUDE.md is under sixty lines. You're not writing documentation. You're writing the minimum set of things Claude can't figure out on its own.
