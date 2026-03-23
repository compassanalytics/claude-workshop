# Part 2b: Rules — Scoped Instructions for Specific Contexts

---

## The Problem Rules Solve (~1 min)

Alright so next we have rules. In certain cases, you might find yourself adding way too many instructions in your CLAUDE.md files, even while following the best practices of what not to include. And so you might need a more efficient and robust way to manage how and when these instructions should be added to your context.

This is where rules come in. They allow you to split these instructions into their own focused files, each covering a topic, so you get better organization. Path-scoped rules take it a step further — they only load into context when needed, if Claude is reading a specific type of file whose path matches a specific pattern. And that's what adds a lot of efficiency by keeping things clean.

---

## How Rules Work (~4 min)

Every `.md` file in `.claude/rules/` (including subdirectories) automatically becomes part of your project context. There are two types:

1. **Unscoped** — no frontmatter. Loads every session, behaves like extra CLAUDE.md content.
2. **Path-scoped** — has a `paths` field in YAML frontmatter. Loads only when Claude reads files matching the pattern.

**Diagram:** See `rules-diagram.svg` in this directory for how the two-phase loading works.

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

## Caveat (~1 min)

**Path-scoped rules only trigger on file reads** — not writes or creates. So if Claude is creating a brand new API file from scratch, your API rules won't load. If a rule is critical enough that it needs to apply even during file creation, make it unscoped.


