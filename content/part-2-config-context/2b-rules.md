# Part 2b: Rules — Scoped Instructions for Specific Contexts

---

## The Problem Rules Solve (~1 min)

A good CLAUDE.md works until the project outgrows it. Once you're past 200 lines — API conventions, React patterns, testing standards, migration rules — Claude starts dropping things, and every instruction competes for attention regardless of what Claude is actually working on.

`.claude/rules/` fixes this. Split instructions into focused files, one topic each. Path-scoped rules go further: they load only when Claude reads matching files, so your API validation rules aren't consuming context while Claude edits a React component.

---

## How Rules Work (~4 min)

Every `.md` file in `.claude/rules/` (including subdirectories) automatically becomes part of your project context. Two modes:

1. **Unscoped** — no frontmatter. Loads every session. Behaves like extra CLAUDE.md content.
2. **Path-scoped** — has a `paths` field in YAML frontmatter. Loads only when Claude reads files matching the pattern.

Here's what that looks like in practice:

```
SESSION START
─────────────────────────────────────────────────
Scan .claude/rules/ recursively

  code-style.md      → No paths    → LOAD FULL CONTENT
  testing.md          → No paths    → LOAD FULL CONTENT
  frontend/react.md   → paths: [src/**/*.tsx] → INDEX ONLY (name + frontmatter)
  backend/api.md      → paths: [src/api/**/*.ts] → INDEX ONLY
  backend/database.md → paths: [**/migrations/**] → INDEX ONLY

DURING SESSION
─────────────────────────────────────────────────
Claude reads src/api/users.ts
  → Matches src/api/**/*.ts → backend/api.md LOADS into context

Claude reads src/components/Button.tsx
  → Matches src/**/*.tsx → frontend/react.md LOADS into context
  → backend/api.md already loaded — stays in context
─────────────────────────────────────────────────
```

Path-scoped rules cost almost nothing at startup — just filename and frontmatter. The full body enters context only when relevant. Once loaded, a rule stays loaded for the rest of the session.

**The frontmatter is minimal** — `paths` is the only supported field:

```markdown
# .claude/rules/backend/api.md

---
paths:
  - "src/api/**/*.ts"
  - "src/middleware/**/*.ts"
---

# API Rules
- Validate all inputs with Zod schemas from src/lib/schemas/
- Return consistent error shapes: { error: string, code: number, details?: object }
- Use parameterized queries — never interpolate user input into SQL
```

Standard glob syntax: `**` for recursive, `*` for wildcard, `{ts,tsx}` for brace expansion. Always quote patterns — unquoted `*` and `{` are reserved in YAML and will cause parse errors. This was a real bug in the official docs, fixed January 2026 ([GitHub #13905](https://github.com/anthropics/claude-code/issues/13905)).

---

## Caveats (~1 min)

**Path-scoped rules only trigger on file reads.** Not writes, not creates. This is by design — Anthropic closed the feature request as "not planned" ([GitHub #23478](https://github.com/anthropics/claude-code/issues/23478)). If Claude is creating a brand new API file from scratch, the API rules won't load. Workaround: make critical rules unscoped.

**User-level path rules have limitations.** Rules in `~/.claude/rules/` only match files under the primary working directory, not `--add-dir` directories ([GitHub #25562](https://github.com/anthropics/claude-code/issues/25562)). Keep path-scoped rules at the project level.

**Verifying what's loaded:** `/memory` shows which rules are active. The `InstructionsLoaded` hook logs exactly which files load and why ([settings reference](https://code.claude.com/docs/en/settings)).

If a rule must be followed 100% of the time, it's not a rule — it's a hook.

---

## When to Use What (~2 min)

| Situation | Use |
|-----------|-----|
| Universal project context ("use pnpm, run tests with vitest") | CLAUDE.md |
| Personal preferences ("I like verbose test output") | CLAUDE.local.md |
| File-specific conventions ("API routes validate with Zod") | Path-scoped rule |
| Broad conventions not needed every session ("named exports only") | Unscoped rule |
| Must happen every time, no exceptions ("never commit .env") | **Hook** (covered later) |

The escalation principle: if Claude keeps ignoring a rule, don't add emphasis. Promote it to a hook. Rules are guidance. Hooks are guarantees.

---

## Symlinks for Shared Rules (~30 sec)

For teams with standard rules across repos, symlinks work. The official docs confirm Claude resolves them normally ([Memory & Rules docs](https://code.claude.com/docs/en/memory)):

```bash
ln -s ~/company-standards/claude-rules .claude/rules/shared
```

---

## Closing for Part 2 (~30 sec)

CLAUDE.md, CLAUDE.local.md, and rules form the context layer — they shape how Claude understands your project. But everything here is guidance. Claude sees it, usually follows it — no guarantee. Part 5 covers hooks, where "usually" becomes "always."
