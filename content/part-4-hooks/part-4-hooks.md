# Part 4: Hooks — Deterministic Control

---

## The Distinction (~1 min)

Everything so far — CLAUDE.md, rules, skills — is guidance. Claude sees it, usually follows it. "Usually" isn't always good enough.

Hooks are shell commands that execute at specific points in Claude Code's lifecycle. They don't ask Claude to do something — they do it. Claude doesn't decide whether a hook runs. The system runs it unconditionally.

> **Skills are probabilistic** — Claude uses judgment about whether to invoke them.
> **Hooks are deterministic** — they run every single time, zero exceptions.

---

## Anatomy of a Hook (~3 min)

Three parts: an **event** (when does it fire?), a **matcher** (which tools trigger it?), and a **command** (what runs?).

**Events** — Claude Code has 22 lifecycle events ([hooks docs](https://code.claude.com/docs/en/hooks)). The ones you'll use most:

| Event | When it fires | Can block? |
|---|---|---|
| `PreToolUse` | Before a tool executes | Yes (exit 2) |
| `PostToolUse` | After a tool succeeds | No |
| `Notification` | Claude needs your attention | No |
| `Stop` | Claude finishes responding | Yes |
| `SessionStart` | Session begins or resumes | No |
| `UserPromptSubmit` | User submits a prompt | Yes |

**Matchers** — regex patterns that filter which tools trigger the hook. What the matcher filters on depends on the event: tool name for `PreToolUse`/`PostToolUse`, notification type for `Notification`, session type for `SessionStart`.

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

## Configuration (~1 min)

Hooks live in `settings.json`, not markdown files:

| Location | Scope |
|---|---|
| `~/.claude/settings.json` | All projects (personal) |
| `.claude/settings.json` | This project (committed) |
| `.claude/settings.local.json` | This project (gitignored) |
| Managed policy settings | Organization-wide (admin) |

The JSON structure:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/my-script.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

An event can have multiple matcher groups, each with multiple hooks. The hook command receives context as JSON via stdin — tool input, tool output, session info.

Four hook types exist (`command`, `http`, `prompt`, `agent`), but `command` covers 90% of cases. `prompt` hooks send a condition to an LLM for evaluation; `agent` hooks spawn a subagent for judgment calls. Start with `command`, reach for the others when you need understanding rather than pattern matching.

---

## Examples (~5 min)

**Desktop notifications** — the "go get coffee" hook. You kick off a task, switch to Slack, and get notified when Claude needs you:

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

Use `/hooks` to browse what's configured — it shows all hooks by event, matcher, and source. You can also ask Claude to write hooks for you: "Write a hook that blocks writes to the migrations folder."

---

## The Escalation Ladder (~1 min)

| Situation | Use |
|---|---|
| Claude usually does this correctly | Don't add anything |
| Claude sometimes forgets | CLAUDE.md or a rule |
| Claude keeps ignoring the rule | Promote to a hook |
| Must happen every time, no exceptions | Hook from the start |
| Must happen AND Claude can't override it | `PreToolUse` hook with exit 2 |
