#!/usr/bin/env bash
# setup-demo.sh — Spin up a working copy of the compass-claude-101 demo project.
#
# Usage:
#   # From anywhere, pulls from GitHub:
#   curl -sL https://raw.githubusercontent.com/compassanalytics/claude-workshop/main/setup-demo.sh | bash
#
#   # With an explicit target dir:
#   curl -sL https://raw.githubusercontent.com/compassanalytics/claude-workshop/main/setup-demo.sh | bash -s -- ~/scratch/demo-1
#
#   # If you're already inside the workshop repo, it uses the local copy instead of cloning:
#   bash setup-demo.sh                     # → ./compass-claude-101
#   bash setup-demo.sh path/to/anywhere    # → path/to/anywhere

set -euo pipefail

REPO_URL="https://github.com/compassanalytics/claude-workshop.git"
TARGET="${1:-compass-claude-101}"
TMP_DIR=""

cleanup() {
  [[ -n "$TMP_DIR" && -d "$TMP_DIR" ]] && rm -rf "$TMP_DIR"
}
trap cleanup EXIT

# --- 1. Refuse to clobber an existing target ---
if [[ -e "$TARGET" ]]; then
  echo "✗ $TARGET already exists. Pick a different target or rm it first."
  exit 1
fi

# --- 2. Get the scaffold (local copy if running inside the repo, else clone) ---
if [[ -d "$PWD/compass-claude-101" && -f "$PWD/compass-claude-101/CLAUDE.md" ]]; then
  echo "Using local copy from $PWD/compass-claude-101"
  SOURCE="$PWD/compass-claude-101"
else
  echo "Cloning $REPO_URL..."
  TMP_DIR="$(mktemp -d)"
  git clone --depth 1 "$REPO_URL" "$TMP_DIR" 2>&1 | tail -3
  SOURCE="$TMP_DIR/compass-claude-101"
fi

cp -R "$SOURCE" "$TARGET"
cd "$TARGET"

# --- 3. Materialize .local.md from .example if missing ---
# The actual CLAUDE.local.md is gitignored by convention, so a fresh
# GitHub clone won't include it. Copy from the .example companion.
if [[ -f "CLAUDE.local.md.example" && ! -f "CLAUDE.local.md" ]]; then
  cp CLAUDE.local.md.example CLAUDE.local.md
  echo "✓ Created CLAUDE.local.md from .example"
fi

# --- 4. Fresh git so demo commits don't share history with the workshop repo ---
rm -rf .git
git init -q
git add -A
git -c user.email='demo@local' -c user.name='Demo' commit -q -m "chore: initial scaffold"
echo "✓ Fresh git initialized"

# --- 4. Python venv + deps ---
echo ""
echo "=== Python deps ==="
if command -v uv >/dev/null 2>&1; then
  uv venv --quiet
  # shellcheck disable=SC1091
  source .venv/bin/activate
  uv pip install --quiet -e ".[dev]"
  echo "✓ uv venv + deps installed"
elif command -v python3 >/dev/null 2>&1; then
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  python -m pip install --quiet --upgrade pip
  pip install --quiet -e ".[dev]"
  echo "✓ venv + deps installed (pip)"
else
  echo "⚠ python3 not found — skipping. Install Python 3.11+ and re-run."
  exit 1
fi

# --- 5. Verify with pytest ---
echo ""
echo "=== pytest ==="
if pytest -q; then
  echo "✓ All tests passed"
else
  echo "⚠ pytest reported failures — check output above"
fi

# --- 6. Done ---
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Demo project ready at: $(pwd)"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "  cd $TARGET"
echo "  source .venv/bin/activate     # activate the venv in your shell"
echo "  claude                          # open Claude Code in the project"
echo ""
echo "See README.md for host setup; DEMOS.md for the demo flow."
