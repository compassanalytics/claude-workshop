#!/usr/bin/env bash
# PreToolUse Bash hook — blocks dangerous rm operations.
# Catches `rm -rf /`, `rm -rf ~`, and `rm -rf` paths outside the project root.

set -uo pipefail

INPUT="$(cat)"
COMMAND="$(echo "$INPUT" | jq -r '.tool_input.command // empty')"
PROJECT_ROOT="$(pwd)"

# Only inspect rm -rf style commands
if ! echo "$COMMAND" | grep -qE 'rm[[:space:]]+(-[rRf]+[[:space:]]+)+'; then
  exit 0
fi

# Always block these obvious foot-guns. The trailing ([[:space:]]|$) is critical:
# without it, `rm -rf /tmp/foo` would match the bare-/ branch and return a misleading message.
if echo "$COMMAND" | grep -qE 'rm[[:space:]]+-[rRf]+[[:space:]]+(/|~|\$HOME|\*)([[:space:]]|$)'; then
  echo "BLOCKED: refusing rm -rf on / ~ \$HOME or *" >&2
  exit 2
fi

# Block rm -rf with absolute paths outside the project root
ABS_TARGET="$(echo "$COMMAND" | grep -oE 'rm[[:space:]]+-[rRf]+[[:space:]]+/[^[:space:]]+' | awk '{print $NF}' | head -n1 || true)"
if [ -n "$ABS_TARGET" ] && [[ "$ABS_TARGET" != "$PROJECT_ROOT"* ]]; then
  echo "BLOCKED: rm -rf target $ABS_TARGET is outside project root $PROJECT_ROOT" >&2
  exit 2
fi

exit 0
