# Part 2a: CLAUDE.md — Your Onboarding Doc for the Agent

---

## Opening (~2 min)

### The hook

Start with this question to the room:

> "How many of you have started a Claude Code session and spent the first 5 minutes re-explaining your project? What framework you use, how to run tests, what naming conventions to follow?"

That's the problem. Every session starts from zero. Claude doesn't remember your last conversation. It doesn't know your team's conventions. It doesn't know that your test runner needs a special flag, or that you use barrel exports, or that there's a legacy module nobody should touch.

**CLAUDE.md fixes this.** It's a markdown file that Claude reads at the start of every single session — before you type anything. It's persistent context. Think of it as writing an onboarding doc, except the new hire is an AI agent that joins your team fresh every morning.

Without one, you're managing an amnesiac. With a good one, Claude shows up already knowing how your project works.

---

## The Hierarchy (~5 min)

### Where CLAUDE.md files live

There isn't just one CLAUDE.md — there's a hierarchy. Each level serves a different purpose.

**Diagram: The CLAUDE.md Hierarchy**

```
┌─────────────────────────────────────────────────────────┐
│  MOST SPECIFIC (wins on conflict)                       │
│                                                         │
│  📁 ./CLAUDE.local.md                                   │
│     Personal, project-level. Gitignored.                │
│     "I like verbose test output"                        │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  📁 ./CLAUDE.md  or  ./.claude/CLAUDE.md                │
│     Project-level. Committed to git. Shared with team.  │
│     "We use ESM, run tests with vitest, deploy to AWS"  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  📁 ./subdir/CLAUDE.md                                  │
│     Directory-specific. Loaded on demand.               │
│     "This module uses a different ORM"                  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  📁 ~/.claude/CLAUDE.md                                 │
│     Global. Applies to every project on your machine.   │
│     "I prefer TypeScript, use pnpm, never amend commits"│
│                                                         │
│  MOST GENERAL                                           │
└─────────────────────────────────────────────────────────┘
```

### How they combine

All levels **combine** — they don't replace each other. Claude sees all of them. When there's a conflict, the more specific file wins.

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

CLAUDE.md is loaded into Claude's context every session. Every line you add competes for attention with every other line. Research shows frontier LLMs can follow roughly **150–200 instructions** with reasonable consistency — and Claude Code's own system prompt already uses about 50 of those. Your CLAUDE.md is drawing from what's left.

### What to include

**Show this table — it's the fastest way to communicate the boundaries:**

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

This is a practical insight worth landing clearly.

**The problem:** When you write "Do NOT use default exports," Claude has to process the negation and infer what you *do* want. This is how LLMs work — negations require an extra reasoning step that sometimes fails.

**The fix:** Frame instructions as what you want, not what you don't.

**Before and After examples:**

| ❌ Negative (weaker) | ✅ Positive (stronger) |
|---------------------|----------------------|
| Do NOT use default exports | Use named exports exclusively |
| Don't use `var` | Use `const` by default, `let` when reassignment is needed |
| Never create duplicate files | Make all updates in existing files |
| Don't use mocks in integration tests | Integration tests must hit the real database |
| Avoid inline styles | Use CSS modules for all component styling |

**The data behind this:** Practitioners who flipped 10 negative rules to positive equivalents measured roughly **half the violation rate**. Anthropic's own documentation says: "Tell Claude what to do instead of what not to do."

There's a psychological parallel here — **Ironic Process Theory** (the "don't think of a pink elephant" effect). Telling someone *not* to do something makes the unwanted behavior more salient, not less. LLMs, trained on human language patterns, exhibit the same tendency.

**When negative instructions still make sense:** Hard safety boundaries. "NEVER commit .env files" or "NEVER expose API keys in client code." These are guardrails, not style preferences — and even then, a hook is more reliable than a CLAUDE.md instruction.

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

**Pro tip from HumanLayer:** Prefer pointers over copies. Don't paste code snippets into CLAUDE.md — they go stale fast. Instead, point to the file: `"See @src/lib/api/client.ts for the canonical API client pattern."` Claude reads the current version.

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

## Getting Started & Maintenance (~2 min)

### The `/init` command

For anyone starting from scratch:

> Run `/init` in Claude Code. It scans your project — reads package files, configs, code structure — and generates a starter CLAUDE.md.

It's a solid starting point. But treat it as a draft, not a finished product. `/init` will include things Claude can already infer (file structure descriptions, obvious conventions). **Ruthlessly prune** what it generates.

### The feedback loop

The best CLAUDE.md files aren't written in one sitting. They evolve:

1. **Start with `/init`**, prune aggressively
2. **When Claude makes a mistake** — ask yourself: "Would a one-line instruction in CLAUDE.md have prevented this?" If yes, add it.
3. **When Claude asks a question** that CLAUDE.md already answers — the phrasing might be ambiguous. Rewrite the instruction.
4. **When Claude correctly does something** without a corresponding instruction — delete the instruction if there is one. It's unnecessary weight.

> **Treat CLAUDE.md like code.** Review it when things go wrong. Prune it regularly. Commit it to git so your team iterates on it together. It compounds in value over time.

### Bridge to 2b

That covers what goes into a single CLAUDE.md file. But as your project grows, stuffing everything into one file becomes the same problem as having no file at all — important rules get lost in the noise.

That's where **Rules** come in — splitting your instructions into focused, scoped files that load only when relevant. Let's look at that next.
