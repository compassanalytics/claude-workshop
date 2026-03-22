# Part 2a: CLAUDE.md — Your Onboarding Doc for the Agent

---

## Opening (~2 min)

### The hook

So we just saw how fast this has moved — autocomplete to full agent orchestration in under five years. What we want to do now is give everyone a level playing field. The goal for the rest of this session is to lay the foundations that take you from "I type prompts and hope for the best" to "I've built an environment where the agent consistently does good work."

And that starts with the simplest thing: Claude starts every session completely blank. No memory of yesterday. Doesn't know your test runner needs a special flag, doesn't know there's a legacy module nobody should touch.

**CLAUDE.md fixes that.** Markdown file Claude reads at the start of every session. Your conventions, your commands, your gotchas — all loaded before you type anything.

---

## The Hierarchy (~5 min)

### Where CLAUDE.md files live

There isn't just one CLAUDE.md — there's a hierarchy. Each level serves a different purpose.

**Diagram: The CLAUDE.md Hierarchy**

```
┌─────────────────────────────────────────────────────────┐
│  📁 ~/.claude/CLAUDE.md                                 │
│     Global. Applies to every project on your machine.   │
│     "I prefer TypeScript, use pnpm, never amend commits"│
│                                                         │
│  + ─────────────────────────────────────────────────────┤
│  📁 ./CLAUDE.md  or  ./.claude/CLAUDE.md                │
│     Project-level. Committed to git. Shared with team.  │
│     "We use ESM, run tests with vitest, deploy to AWS"  │
│                                                         │
│  + ─────────────────────────────────────────────────────┤
│  📁 ./subdir/CLAUDE.md                                  │
│     Directory-specific. Loaded when working in subdir.  │
│     "This module uses a different ORM"                  │
│                                                         │
│  + ─────────────────────────────────────────────────────┤
│  📁 ./CLAUDE.local.md                                   │
│     Personal, project-level. Gitignored.                │
│     "I like verbose test output"                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### How they combine

These **stack** — they don't replace each other. Claude sees all of them at once. Global sets your baseline, project adds team context on top, subdirectory layers on more when you're working in that folder, and local adds your personal preferences.

So what happens when two files contradict each other? Say your global CLAUDE.md says "use npm" but your project CLAUDE.md says "use pnpm." Claude sees both, and the **more specific scope wins**. Project beats global. Subdirectory beats project. Local beats everything — it's your personal override for this project, so it gets the final word.

### Talk through each level:

**Global (`~/.claude/CLAUDE.md`)** — Your personal defaults across every project. Things like:
- Your preferred package manager
- Your commit message style
- Your editor/terminal preferences that affect how Claude should behave

Keep this short. 10-20 lines max. If it's project-specific, it doesn't belong here.

**Project (`./CLAUDE.md`)** — The team file. This is the one that matters most. It gets committed to git, so everyone on the team benefits. It should contain:
- What the project is (one line)
- How to build, test, lint, deploy
- Coding conventions the team agreed on
- Architectural decisions Claude can't infer from code alone

**Directory-specific (`./subdir/CLAUDE.md`)** — For monorepos or projects with distinct modules. Claude loads these on demand when working in that directory. Example: your `frontend/CLAUDE.md` says "use React hooks, no class components" while your `api/CLAUDE.md` says "use Zod for validation, return consistent error shapes."

**Local (`./CLAUDE.local.md`)** — Your personal overrides for *this* project. Automatically gitignored. This is where you put things that are yours alone:
- "Run tests with `--verbose`"
- "I'm working on the auth module this sprint, prioritize context around `src/auth/`"
- "I prefer detailed explanations — don't be terse"

This is the file nobody talks about, but it's genuinely useful. It lets you customize your Claude experience without polluting the team's shared CLAUDE.md.

---

## Writing a Good CLAUDE.md (~8 min)

### The golden rule

> For each line, ask: **"Would removing this cause Claude to make mistakes?"** If the answer is no, delete it.

CLAUDE.md is loaded into Claude's context every session. Every line you add competes for attention with every other line. Anthropic's official guidance is to **target under 200 lines per CLAUDE.md file** — longer files consume more context and reduce adherence.

The IFScale benchmark (Jaroslawicz et al., July 2025 — [arXiv:2507.11538](https://arxiv.org/abs/2507.11538)) tested 20 frontier models and found that even the best ones start falling off hard after about 150 instructions. Claude Code's own system prompt already eats a big chunk of that budget — your CLAUDE.md is drawing from what's left.

### What to include

**This table is adapted from Anthropic's [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices) page:**

| ✅ Include | ❌ Exclude |
|-----------|-----------|
| Commands Claude can't guess (`pnpm test:unit --run`) | Anything Claude can figure out by reading code |
| Code style rules that differ from defaults | Standard conventions Claude already knows |
| Test instructions and preferred runners | Detailed API docs (link instead) |
| Branch naming, PR, commit conventions | Info that changes frequently |
| Architectural decisions specific to your project | Long explanations or tutorials |
| Dev environment quirks (required env vars, ports) | File-by-file codebase descriptions |
| Common gotchas and non-obvious behaviors | Self-evident things like "write clean code" |

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

## A Real Example (~3 min)

### Bad CLAUDE.md (show and critique)

```markdown
# My Project

This is a Next.js project with React and TypeScript. We use Tailwind for styling.
The project has a frontend and a backend. The frontend is in src/app and the backend
is in src/api. We use PostgreSQL for the database with Prisma as the ORM.

## Code Style
- Use TypeScript
- Use functional components
- Write clean, readable code
- Use meaningful variable names
- Add comments where necessary
- Follow DRY principles
- Use proper error handling
- Write tests for your code

## Don't Do This
- Don't use var
- Don't use class components
- Don't write inline styles
- Don't commit without tests
- Don't use any type
- Don't skip error handling
- Don't use console.log in production code
- Don't create duplicate files
- Don't modify the database schema without a migration

## Project Structure
- src/app — frontend pages and components
- src/api — backend API routes
- src/lib — shared utilities
- src/types — TypeScript type definitions
- prisma/ — database schema and migrations
- public/ — static assets
- tests/ — test files
```

**What's wrong with this:**
- **Claude already knows most of this.** "Use TypeScript," "meaningful variable names," "follow DRY" — Claude does these by default. Wasted context.
- **Negative instructions everywhere.** "Don't use var," "don't use class components" — positive framing would be stronger.
- **Describing the file structure.** Claude can read the directory. It doesn't need you to list what's in `src/`.
- **No actionable commands.** How does Claude run tests? Build? Lint? Deploy? Those are the things it can't figure out on its own.
- **Too vague to be useful.** "Write clean code" and "proper error handling" aren't instructions — they're platitudes.

### Good CLAUDE.md (show the rewrite)

```markdown
# Project
Next.js 14 e-commerce app with Prisma + PostgreSQL.

# Commands
- Build: `pnpm build`
- Dev: `pnpm dev` (port 3000)
- Test all: `pnpm test`
- Test single: `pnpm test -- --run path/to/test`
- Lint: `pnpm lint`
- Type check: `pnpm typecheck`
- DB migrate: `pnpm prisma migrate dev --name <name>`
- DB generate: `pnpm prisma generate`

# Code Style
- Use named exports exclusively
- Use `const` by default, `let` only when reassignment is needed
- Use CSS modules for component styling (not Tailwind utilities inline)
- Use the shared API client from `src/lib/api/client.ts` for all HTTP calls
- Collocate tests next to source files: `Button.tsx` → `Button.test.tsx`

# Architecture Decisions
- All API routes validate input with Zod schemas from `src/lib/schemas/`
- Auth uses next-auth with JWT strategy — session tokens in httpOnly cookies
- Database migrations are reviewed by the team — create the migration, don't apply it

# Gotchas
- The test database resets between runs — don't rely on seed data across tests
- IMPORTANT: `src/legacy/` is being deprecated. Read from it but write new code in `src/lib/`.
- Environment variables: copy `.env.example` to `.env.local` for local dev
```

**What's better:**
- **37 lines vs 35 lines** — similar length, vastly more useful content
- **Every line changes Claude's behavior.** Remove any line and Claude would make a mistake.
- **Actionable commands** Claude can copy-paste and run
- **Positive framing** — "use named exports" not "don't use default exports"
- **Real architectural context** Claude can't infer — the auth strategy, the Zod convention, the legacy module warning
- **Emphasis only where it matters** — one IMPORTANT tag on the rule that would cause the most damage if violated

---

## Getting Started (~2 min)

### `/init`

Run `/init` in Claude Code. It scans your project and generates a starter CLAUDE.md. Treat it as a first draft — it'll include stuff Claude can already figure out from your code (file structure descriptions, obvious conventions). Cut those.

### How it should evolve

A good CLAUDE.md grows from real friction, not upfront planning. Every time Claude makes a mistake, ask: "Would a one-line instruction have prevented this?" If yes, add it. Every time Claude keeps asking you something, that's a missing instruction. Commit it to git so the whole team benefits and iterates on it together.

The [HumanLayer blog (Nov 2025)](https://www.humanlayer.dev/blog/writing-a-good-claude-md) makes a good point here — their root CLAUDE.md is under sixty lines. You're not writing documentation. You're writing the minimum set of things Claude can't figure out on its own.
