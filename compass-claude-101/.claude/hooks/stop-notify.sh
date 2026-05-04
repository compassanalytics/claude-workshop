#!/usr/bin/env bash
# Stop hook — desktop notification when Claude finishes responding.
# macOS via osascript; Linux falls back to notify-send.

if command -v osascript >/dev/null 2>&1; then
  osascript -e 'display notification "Claude finished responding" with title "Claude Code" sound name "Pop"' 2>/dev/null || true
elif command -v notify-send >/dev/null 2>&1; then
  notify-send "Claude Code" "Claude finished responding" 2>/dev/null || true
fi

exit 0
