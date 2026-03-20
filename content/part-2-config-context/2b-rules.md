# Part 2b: Rules — Scoped Instructions for Specific Contexts

---

## The Problem Rules Solve (~2 min)

### Opening

Pick up directly from the 2a bridge:

> "So now you have a good CLAUDE.md. It's lean, it's useful, Claude follows it. But your project keeps growing. You add API conventions, then React patterns, then testing standards, then database migration rules, then security guidelines. Suddenly your CLAUDE.md is 300 lines — and Claude starts ignoring half of it."

This is **priority saturation**. When everything is high priority, nothing is. Claude treats CLAUDE.md as authoritative — every line competes for the same attention. A 300-line file means your critical rules about database migrations are fighting for context with your preference for arrow functions.

And here's the waste: when Claude is editing a React component, it's loading your API validation rules, your migration safety rules, your deployment conventions — none of which matter for the task at hand.

**Rules solve both problems.** Instead of one massive file, you split instructions into focused files. Each one covers one topic. And with path-scoping, you can make rules load *only* when Claude is working on matching files.

---

## What Rules Are (~2 min)

### The basics

The `.claude/rules/` directory contains markdown files. Each file is a rule. Every `.md` file in this directory (including subdirectories) automatically becomes part of your project context — no configuration needed.

**Two modes:**

1. **Unscoped rules** — no frontmatter, load every session, apply universally. Behave exactly like extra CLAUDE.md content.

2. **Path-scoped rules** — have a `paths` field in YAML frontmatter. Only load when Claude is working on files that match the pattern.

**Show the distinction side by side:**

```markdown
# .claude/rules/code-style.md
# (No frontmatter — loads every session)

- Use named exports exclusively
- Prefer const, use let only for reassignment
- Collocate tests next to source files
```

```markdown
# .claude/rules/backend/api.md

---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules
- Validate all inputs with Zod schemas from src/lib/schemas/
- Return consistent error shapes: { error: string, code: number, details?: object }
- Log all requests with correlation IDs
- Use parameterized queries — never interpolate user input into SQL
```

The first file loads every time — it's universal code style. The second file only activates when Claude reads or edits files matching `src/api/**/*.ts`. When Claude is working on a React component, the API rules aren't consuming context.

---

## The Two-Phase Loading System (~3 min)

### How it actually works under the hood

This is worth explaining clearly because it's the key to understanding why path-scoped rules are context-efficient.

**Diagram: Two-Phase Loading**

```
SESSION START
─────────────────────────────────────────────────
Phase 1: Scan .claude/rules/ recursively

  code-style.md      → No paths → LOAD FULL CONTENT NOW
  testing.md          → No paths → LOAD FULL CONTENT NOW
  security.md         → No paths → LOAD FULL CONTENT NOW
  frontend/react.md   → paths: ["src/**/*.tsx"] → INDEX ONLY (name + frontmatter)
  frontend/styling.md → paths: ["**/*.css"] → INDEX ONLY
  backend/api.md      → paths: ["src/api/**/*.ts"] → INDEX ONLY
  backend/database.md → paths: ["**/migrations/**"] → INDEX ONLY

─────────────────────────────────────────────────

DURING SESSION
─────────────────────────────────────────────────
Claude reads src/api/users.ts
  → Matches "src/api/**/*.ts"
  → backend/api.md FULL CONTENT INJECTED into context

Claude reads src/components/Button.tsx
  → Matches "src/**/*.tsx"
  → frontend/react.md FULL CONTENT INJECTED into context
  → backend/api.md stays dormant — no match

─────────────────────────────────────────────────
```

**The key insight:** At startup, path-scoped rules cost almost nothing — Claude reads only the filename and frontmatter (a few tokens each). The full rule body only enters context when it's relevant. You can have dozens of scoped rules without bloating context on unrelated tasks.

---

## Frontmatter Syntax (~2 min)

### The format

Path-scoping uses YAML frontmatter at the top of the markdown file:

```yaml
---
paths:
  - "src/api/**/*.ts"
---
```

**Supported patterns:**

```yaml
# Single pattern
---
paths: "src/api/**/*.ts"
---

# Multiple patterns
---
paths:
  - "src/components/**/*.tsx"
  - "src/hooks/**/*.ts"
---

# Brace expansion
---
paths: "src/**/*.{ts,tsx}"
---
```

**Pattern cheat sheet:**

| Pattern | Matches |
|---------|---------|
| `src/api/**/*.ts` | All .ts files in src/api/ and subdirectories |
| `**/*.test.ts` | Test files anywhere in the project |
| `**/*.css` | CSS files anywhere |
| `src/**/*.{ts,tsx}` | TypeScript and TSX files under src/ |
| `prisma/migrations/**/*` | Everything in migrations |

**Important:** Always quote your glob patterns in the frontmatter. Patterns starting with `*` or `{` are reserved characters in YAML — unquoted, they'll cause parse errors. This was actually a bug in the official docs at one point.

---

## A Realistic Directory Structure (~2 min)

### Show the full picture

```
.claude/rules/
├── code-style.md              # No paths → always loaded
├── testing.md                 # No paths → always loaded
├── git-workflow.md            # No paths → always loaded
├── frontend/
│   ├── react.md              # paths: ["src/components/**/*.tsx",
│   │                         #         "src/hooks/**/*.ts"]
│   └── styling.md            # paths: ["**/*.css", "**/*.module.css"]
├── backend/
│   ├── api.md                # paths: ["src/api/**/*.ts"]
│   └── database.md           # paths: ["prisma/migrations/**/*"]
└── security/
    └── auth.md               # paths: ["src/auth/**/*",
                              #         "src/payments/**/*"]
```

**Walk through the logic:**

- **Claude opens a fresh session.** It loads `code-style.md`, `testing.md`, and `git-workflow.md` in full. The rest are indexed — Claude knows they exist and what file patterns they match, but their content isn't in context yet.

- **You ask Claude to build a new API endpoint.** Claude starts editing `src/api/orders.ts`. The path matches `src/api/**/*.ts` — `api.md` content loads. Claude now knows to validate with Zod, return consistent error shapes, and use parameterized queries.

- **Claude also needs to write a test.** It creates `src/api/orders.test.ts`. The `.test.ts` pattern means `testing.md` was already loaded (it's unscoped). If you had a scoped test rule with `paths: ["**/*.test.*"]`, it would load now too.

- **Claude never touches the React components.** `react.md` and `styling.md` stay dormant the entire session — zero context cost.

---

## Real Rule File Examples (~3 min)

### Show 3-4 complete examples people can model from

**Example 1: React component rules**

```markdown
# .claude/rules/frontend/react.md

---
paths:
  - "src/components/**/*.tsx"
  - "src/app/**/*.tsx"
---

# React Component Rules

- Use functional components with hooks — no class components
- Props interfaces go in the same file, named {ComponentName}Props
- Extract hooks into src/hooks/ when reused across 2+ components
- Use React.memo() only when profiling shows a measurable render cost
- Event handlers: handleClick, handleSubmit, handleChange (not onClick, onSubmit)
- Prefer controlled components for forms
```

**Example 2: Database migration safety**

```markdown
# .claude/rules/backend/database.md

---
paths:
  - "prisma/migrations/**/*"
  - "prisma/schema.prisma"
---

# Migration Safety Rules

- IMPORTANT: Create the migration file but do NOT run `prisma migrate deploy`
- Every migration needs a rollback strategy documented in a comment
- Never drop a column in the same migration that removes the code using it — split into two migrations
- Add new required columns as optional first, backfill, then make required
- Index any column used in WHERE clauses or JOINs
```

**Example 3: Security-critical paths**

```markdown
# .claude/rules/security/auth.md

---
paths:
  - "src/auth/**/*"
  - "src/payments/**/*"
  - "src/middleware/session.*"
---

# Security-Critical Code Rules

- Never log tokens, passwords, API keys, or PII
- Validate all inputs at the boundary — assume everything external is malicious
- Use parameterized queries exclusively — zero string interpolation in SQL
- Auth tokens: httpOnly cookies only, never localStorage
- Rate-limit all authentication endpoints
- Payment amounts: validate server-side, never trust client-submitted totals
```

**Example 4: An unscoped testing standard**

```markdown
# .claude/rules/testing.md
# (No frontmatter — loads every session)

# Testing Standards

- Run single tests during development: `pnpm test -- --run path/to/file`
- Full suite before committing: `pnpm test`
- Test names: "should [action] when [condition]"
- One logical assertion per test
- Mock external services (APIs, email, payments) — never call real services in tests
- Integration tests hit the real database — no DB mocks
```

---

## The Honest Caveats (~1 min)

### Be upfront about maturity

Path-scoped rules are powerful but still maturing. Worth flagging these known issues so people don't get frustrated and give up:

- **Write/create gap:** Path-scoped rules have been reported to only trigger on file *reads*, not when Claude *writes* or *creates* a matching file. So if Claude is creating a brand new API file, the API rules might not activate. Workaround: also include the rule as guidance in CLAUDE.md, or make the rule unscoped if it's critical enough.

- **User-level path scoping:** The `paths` frontmatter works reliably in project-level rules (`.claude/rules/`), but has had issues in user-level rules (`~/.claude/rules/`). Keep path-scoped rules at the project level for now.

- **YAML quoting:** Always quote glob patterns. `paths: src/**/*.ts` may work, but `paths: **/*.ts` or `paths: {src,lib}/**/*.ts` will break without quotes. The safe habit: always quote.

> "These are real bugs that have been filed and acknowledged. The feature works, but check GitHub issues if something isn't loading as expected. And remember — if a rule absolutely MUST be followed 100% of the time, that's not a rule at all. That's a hook. We'll cover those next."

---

## When to Use What (~2 min)

### The decision framework

**Show this as the mental model for the entire configuration layer:**

```
"Should Claude always know this?"
    │
    ├── YES → "Is it universal to the project?"
    │           │
    │           ├── YES → CLAUDE.md
    │           │         (project-level, committed, team-shared)
    │           │
    │           └── NO, it's personal → CLAUDE.local.md
    │                                    (gitignored)
    │
    └── ONLY SOMETIMES → "Does it apply to specific files?"
                │
                ├── YES → Path-scoped rule
                │         (.claude/rules/ with paths frontmatter)
                │
                └── It's broad but not every-session →
                    Unscoped rule
                    (.claude/rules/ without frontmatter)
```

**Quick reference table:**

| Situation | Use |
|-----------|-----|
| "We use pnpm and vitest across the whole project" | CLAUDE.md |
| "I personally like verbose test output" | CLAUDE.local.md |
| "API routes must validate with Zod" | Path-scoped rule on `src/api/**` |
| "All code should use named exports" | Unscoped rule or CLAUDE.md |
| "Migration files need rollback strategies" | Path-scoped rule on `prisma/migrations/**` |
| "Commits must never include .env files" | **Hook** (deterministic — covered next) |
| "Format code on every save" | **Hook** (deterministic — covered next) |

### The escalation principle

> "If you find yourself thinking 'Claude keeps ignoring this rule' — don't add more emphasis to the rule. Promote it to a hook. Rules are guidance. Hooks are guarantees. We'll cover the difference in Part 4."

This is the bridge to Part 4 (Hooks).

---

## Symlinks for Shared Rules (quick mention, ~30 sec)

### For teams with multiple repos

If your team has standard rules across multiple projects, you can symlink shared rules:

```bash
# Link a shared company rules directory
ln -s ~/company-standards/claude-rules .claude/rules/shared

# Or link individual rule files
ln -s ~/company-standards/security.md .claude/rules/security.md
```

Claude resolves symlinks normally. This lets you maintain one source of truth for rules that apply across your organization.

---

## Closing for Part 2 (~30 sec)

### Recap the configuration layer

> "So to recap Part 2: CLAUDE.md gives Claude persistent context every session. CLAUDE.local.md gives you personal overrides without affecting the team. And Rules let you split instructions into focused files that load only when relevant. Together, these form the **context layer** — they shape how Claude understands your project."
>
> "But everything we've covered so far is *guidance*. Claude sees it, Claude usually follows it — but there's no guarantee. In Part 3 we'll look at Skills, and in Part 4 we'll get to Hooks — where 'usually' becomes 'always.'"
