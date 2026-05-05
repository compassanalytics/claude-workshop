#!/usr/bin/env bash
# reset-demo.sh — restore the demo project to a clean pre-demo state.
#
# Run this between dry-runs (or between major demo sections) so you start
# from a known good state instead of accumulating cruft from earlier demos.
#
# Resets:
#   - All unstaged working-tree changes (git restore .)
#   - All staged changes (git restore --staged .)
#
# Removes:
#   - src/api/health/    (created by Part 2b "write doesn't trigger" demo)
#   - .env               (will be re-created from .env.example if you pass --bait)
#
# Does NOT touch:
#   - .venv, .git, .claude/, CLAUDE.local.md
#   - anything outside this directory
#
# Usage:
#   bash reset-demo.sh              # plain reset
#   bash reset-demo.sh --bait       # reset + force-stage .env for the hooks demo

set -euo pipefail

if [[ ! -f "CLAUDE.md" || ! -d ".claude" ]]; then
  echo "✗ Run this from inside the demo project (a copy of compass-claude-101)."
  exit 1
fi

echo "=== Restoring working tree ==="
git restore --staged . 2>/dev/null || true
git restore . 2>/dev/null || true

echo "=== Removing demo artifacts ==="
rm -rf src/api/health/
rm -f .env

if [[ "${1:-}" == "--bait" ]]; then
  echo "=== Setting up hooks-demo bait ==="
  cp .env.example .env
  git add -f .env
  echo "✓ .env force-staged and ready for the hooks demo"
fi

echo ""
echo "=== Final state ==="
git status --short | head -10 || true

echo ""
echo "✓ Reset complete."
