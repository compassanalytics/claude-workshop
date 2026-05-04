---
name: pr-prep
description: Prepare a PR — run lint, type-check, tests, draft a PR title and description from the diff, and open it via gh.
argument-hint: "[base-branch] — defaults to main"
allowed-tools: Bash, Read, Grep
---

# PR Prep

Run all the gates that should pass before review, then open a PR with a thoughtful description.

## Pre-flight context

The lines below use the `!`...`` dynamic-context syntax. Each command runs at
invocation time, *before* Claude reads the rest of this skill. Claude sees the
rendered output, not the commands themselves. That means the skill body
already has fresh repo state injected into context — no extra tool calls required.

- Current branch: !`git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "(not a git repo)"`
- Working tree status: !`git status --short 2>/dev/null | head -20`
- Recent commits on this branch: !`git log --oneline -10 2>/dev/null`
- Diff vs main (stat): !`git diff main...HEAD --stat 2>/dev/null | tail -25`

## Steps

1. Determine the base branch from `$ARGUMENTS` or default to `main`. Use the pre-flight context above to confirm we're not on it and that the working tree state is sane.
2. Run quality gates:
   - `ruff check src/ tests/`
   - `ruff format --check src/ tests/`
   - `mypy src/`
   - `pytest -q`
   - `cd web && npm run lint && npm run typecheck` (only if `web/` files changed)
3. If any gate fails, print which one and stop. Do NOT open the PR.
4. Use the diff/log already in pre-flight context to draft a PR title (≤70 chars, imperative mood) and a body with:
   - **Summary** — 1–3 bullets on what changed and why.
   - **Testing** — list of tests added or affected.
   - **Notes** — anything reviewers should know (migrations, follow-ups, breaking changes).
5. Show the user the draft. Wait for confirmation before pushing/opening.
6. On confirm: `git push -u origin HEAD` then `gh pr create --base <base> --title ... --body ...` (HEREDOC for the body).
7. Print the PR URL.

## Don't

- Don't open a PR if any gate fails. Surface the failure clearly.
- Don't push to `main`. Don't force-push. Don't skip hooks.
- Don't include the diff in the PR body — `gh pr view` already shows it.
