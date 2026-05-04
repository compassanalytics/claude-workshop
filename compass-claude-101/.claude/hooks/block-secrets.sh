#!/usr/bin/env bash
# PreToolUse Bash hook — blocks `git commit` if any sensitive file is staged.
# Triggered by: matcher "Bash" on PreToolUse.
# Exit 0 = allow. Exit 2 = block (stderr surfaces to Claude as an error message).

set -uo pipefail

INPUT="$(cat)"
COMMAND="$(echo "$INPUT" | jq -r '.tool_input.command // empty')"

# Only act on git commit invocations
if ! echo "$COMMAND" | grep -qE 'git[[:space:]]+commit'; then
  exit 0
fi

STAGED="$(git diff --cached --name-only 2>/dev/null || true)"
if [ -z "$STAGED" ]; then
  exit 0
fi

# Sensitive patterns — extend as needed
SENSITIVE_REGEX='\.(env|key|pem|p12|pfx)$|/credentials|/secrets|id_rsa|id_ed25519'

MATCHED="$(echo "$STAGED" | grep -iE "$SENSITIVE_REGEX" || true)"
if [ -n "$MATCHED" ]; then
  {
    echo "BLOCKED: refusing to commit files that look like secrets:"
    echo "$MATCHED" | sed 's/^/  - /'
    echo ""
    echo "If this is a false positive, unstage and commit explicitly without this hook."
  } >&2
  exit 2
fi

exit 0
