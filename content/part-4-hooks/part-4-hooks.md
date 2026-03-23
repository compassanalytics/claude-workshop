# Part 4: Hooks — Deterministic Control

---

## The Distinction (~1 min)

Everything so far — CLAUDE.md, rules, skills — is guidance. Claude sees it, usually follows it. But "usually" isn't always good enough.

Hooks are shell commands that execute at specific points in Claude Code's lifecycle. They don't ask Claude to do something — they do it. Claude doesn't decide whether a hook runs. The system runs it unconditionally.

> **Skills are probabilistic** — Claude uses judgment about whether to invoke them.
> **Hooks are deterministic** — they run every single time, zero exceptions.

---

## What a Hook Looks Like (~2 min)

Before we break down the pieces, here's the simplest useful hook — a desktop notification for when Claude needs your attention:

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "osascript -e 'display notification \"Claude needs your attention\" with title \"Claude Code\"'"
      }]
    }]
  }
}
```

This lives in your `settings.json`. Three parts: an **event** (`Notification` — when does it fire?), a **matcher** (`""` — which tools trigger it? empty means all), and a **command** (the shell script that runs).

You kick off a task, switch to Slack, and get a notification when Claude needs you. That's the "go get coffee" hook.

---

## How Hooks Work (~3 min)

Now let's break down each piece.

**Events** — specific points in Claude's lifecycle where a hook can fire. The ones you'll use most:

| Event | When it fires | Can block? |
|---|---|---|
| `PreToolUse` | Before a tool executes | Yes (exit 2) |
| `PostToolUse` | After a tool succeeds | No |
| `Notification` | Claude needs your attention | No |
| `Stop` | Claude finishes responding | Yes |
| `SessionStart` | Session begins or resumes | No |
| `UserPromptSubmit` | User submits a prompt | Yes |

**Matchers** — regex patterns that filter which tools trigger the hook:

```
"Bash"              → only Bash commands
"Edit|Write"        → file edits or writes
"mcp__github__.*"   → any GitHub MCP tool
""                  → everything (or omit matcher entirely)
```

Some events like `Stop` and `UserPromptSubmit` don't support matchers — they always fire.

**Exit codes** — this is how hooks control behavior:

| Exit Code | Effect |
|---|---|
| 0 | Allow — tool proceeds normally |
| **2** | **Block — tool call cancelled. Stderr shown to Claude as error.** |
| Other | Non-blocking error. Stderr shown in verbose mode only. |

Exit code 2 is the kill switch. A `PreToolUse` hook that exits 2 cancels the tool call — period. Claude sees the error and has to find another approach. This is fundamentally different from CLAUDE.md: you can write "NEVER force push to main" in CLAUDE.md, and Claude will follow it until a long session where it decides it needs to. A hook with exit 2 makes it impossible.

---

## More Examples (~3 min)

**Block commits with sensitive files** — a `PreToolUse` hook that prevents committing `.env`, `.key`, `.pem` files:

```bash
#!/bin/bash
# .claude/hooks/block-secrets.sh
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if ! echo "$COMMAND" | grep -q "git commit"; then exit 0; fi

STAGED=$(git diff --cached --name-only 2>/dev/null)
if echo "$STAGED" | grep -iE '\.(env|key|pem)$|credentials|secrets' > /dev/null 2>&1; then
  echo "BLOCKED: Sensitive files in staged changes" >&2
  exit 2
fi
exit 0
```

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{ "type": "command", "command": ".claude/hooks/block-secrets.sh" }]
    }]
  }
}
```

Exit 2 = commit cancelled. You can write "never commit .env files" in CLAUDE.md. This hook makes it impossible.

**Auto-format after edits** — `PostToolUse` on `Edit|Write` that runs your formatter:

```bash
#!/bin/bash
# .claude/hooks/auto-format.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[ -z "$FILE_PATH" ] && exit 0

case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx) npx prettier --write "$FILE_PATH" 2>/dev/null ;;
  *.py) black "$FILE_PATH" 2>/dev/null ;;
esac
exit 0
```

Always exits 0 — formatting is best-effort, shouldn't block Claude.

Use `/hooks` to browse what's configured. You can also ask Claude to write hooks for you: "Write a hook that blocks writes to the migrations folder."

---

## Where Hooks Live

Hooks are configured in `settings.json`, not markdown files:

| Location | Scope |
|---|---|
| `~/.claude/settings.json` | All projects (personal) |
| `.claude/settings.json` | This project (committed) |
| `.claude/settings.local.json` | This project (gitignored) |

The hook command receives context as JSON via stdin — tool input, tool output, session info. This is how the block-secrets script knows what command Claude is running.

Hooks aren't limited to shell scripts either. You can use `prompt` hooks that trigger LLM inference, or `agent` hooks that spawn a Claude subagent to review or evaluate something. For example, a `PreToolUse` agent hook could have Claude review every commit message before it's created, or evaluate whether a code change follows your architecture patterns — deterministically triggered, with AI-level judgment.

