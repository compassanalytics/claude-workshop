# Part 4: Hooks — Deterministic Control

---

## The Critical Distinction (~2 min)

### Opening — land this hard

This is the single most important concept in this section. Set it up clearly:

> "Everything we've covered so far — CLAUDE.md, Rules, Skills — is guidance. Claude sees the instructions, Claude usually follows them. But 'usually' isn't always good enough."
>
> "What if you need a formatting check to run after *every* file edit? What if you need to block commits that include `.env` files *every single time*? What if you want a desktop notification *whenever* Claude needs your attention?"
>
> "You can put these in CLAUDE.md. And Claude will follow them... mostly. Until context gets crowded, or a long session drifts, or Claude decides it knows better."

Now deliver the distinction:

> **"Skills are probabilistic — Claude uses judgment about whether to invoke them.**
> **Hooks are deterministic — they run every single time, zero exceptions."**

Hooks are shell commands that execute at specific points in Claude Code's lifecycle. They don't *ask* Claude to do something — they *do* it. Claude doesn't decide whether a hook runs. The system runs it unconditionally.

---

## Anatomy of a Hook (~3 min)

### Three parts

Every hook has three components:

**Diagram:**

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│   EVENT    │ ──→ │  MATCHER   │ ──→ │  COMMAND   │
│            │     │            │     │            │
│ When does  │     │ Which tool │     │ What shell │
│ it fire?   │     │ triggers   │     │ script     │
│            │     │ it?        │     │ runs?      │
└────────────┘     └────────────┘     └────────────┘
```

### Events — when hooks fire

Hooks attach to lifecycle events. These are the ones that matter most:

| Event | When it fires | Can block? |
|-------|--------------|------------|
| **`PreToolUse`** | Before a tool executes | **Yes** (exit code 2) |
| **`PostToolUse`** | After a tool succeeds | Yes |
| **`Notification`** | Claude needs your attention | No |
| **`Stop`** | Claude finishes responding | Yes |
| **`SessionStart`** | Session begins or resumes | No |
| **`UserPromptSubmit`** | User submits a prompt | Yes |
| **`SubagentStart`** | A subagent is spawned | No |
| **`SubagentStop`** | A subagent finishes | Yes |
| **`TaskCompleted`** | A task is marked complete | Yes |
| **`ConfigChange`** | A config file changes | Yes |

**The two you'll use most:** `PreToolUse` (gate actions before they happen) and `PostToolUse` (react after actions complete).

### Matchers — which tools trigger the hook

Matchers are **regex patterns** that filter which tools cause the hook to fire.

```
"Bash"              → only Bash commands
"Edit|Write"        → file edits or writes
"mcp__github__.*"   → any GitHub MCP tool
".*"  or  ""        → everything
```

For events without tool context (like `Stop` or `Notification`), the matcher is either ignored or matches on event-specific values.

### Commands — what runs

The hook executes a shell command. The command receives the hook's context as JSON via stdin — tool input, tool output, session info. The command's exit code determines what happens next.

---

## Exit Codes — The Kill Switch (~2 min)

### The most important thing about hooks

Exit codes are how hooks control Claude's behavior:

| Exit Code | Meaning | What happens |
|-----------|---------|-------------|
| **0** | Success / Allow | Tool proceeds normally. JSON output is processed. |
| **2** | **Block** | Tool call is **cancelled**. Stderr message shown to Claude as an error. |
| Other (1, etc.) | Non-blocking error | Execution continues. Stderr shown in verbose mode only. |

**Exit code 2 is the kill switch.** When a `PreToolUse` hook exits with code 2, the tool call is cancelled — period. Claude sees the error and has to find another approach. This is how you create hard guardrails that Claude cannot override, ignore, or rationalize away.

**Show the flow:**

```
Claude wants to run: git push --force origin main

  PreToolUse hook fires
    → Script checks the command
    → Sees "--force" and "main"
    → Prints "Force push to main blocked" to stderr
    → exit 2

  Result: Command is CANCELLED. Claude sees the error.
  Not "Claude decides not to." The system prevents it.
```

> "This is fundamentally different from CLAUDE.md. You can write 'NEVER force push to main' in CLAUDE.md, and Claude will follow it... until a long session where it decides it needs to. A hook with exit code 2 makes it physically impossible."

---

## Configuration (~2 min)

### Where hooks live

Hooks are defined in `settings.json`, not in markdown files:

| Location | Scope | Shared? |
|----------|-------|---------|
| `~/.claude/settings.json` | All projects | Personal |
| `.claude/settings.json` | This project | Yes (committed) |
| `.claude/settings.local.json` | This project | No (gitignored) |
| Managed policy settings | Organization-wide | Yes (admin) |

### The JSON structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "regex_pattern",
        "hooks": [
          {
            "type": "command",
            "command": "path/to/script.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Talk through the nesting:** An event can have multiple matcher groups. Each matcher group can have multiple hooks. This lets you attach different scripts to different tools within the same event.

### Hook types

There are four types — but most people only need the first:

| Type | What it does |
|------|-------------|
| **`command`** | Runs a shell script. The workhorse. |
| `http` | Calls an HTTP endpoint. For remote integrations. |
| `prompt` | An LLM evaluates a condition (fast model). |
| `agent` | A full Claude model decides. For judgment calls. |

**For this workshop, focus on `command` hooks.** Prompt and agent hooks are advanced patterns — powerful but niche.

---

## Practical Examples (~8 min)

### Example 1: Desktop notification when Claude needs input

This is the "go get coffee" hook. You kick off a task, switch to Slack or a browser, and get a native macOS notification when Claude needs you back.

**The config:**

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

**Walk through it:**
- **Event:** `Notification` — fires when Claude is waiting for input or a permission prompt
- **Matcher:** empty string — matches all notification types
- **Command:** macOS `osascript` to trigger a native notification

> "This is a 4-line hook that fundamentally changes how you use Claude Code. Instead of staring at your terminal waiting, you fire off a task and go do something else. Your Mac tells you when to come back."

**For Linux:**
```bash
notify-send "Claude Code" "Claude needs your attention"
```

### Example 2: Block commits with sensitive files

A `PreToolUse` hook that prevents committing `.env`, `.key`, `.pem`, or credentials files.

**The script (`.claude/hooks/block-secrets.sh`):**

```bash
#!/bin/bash
# Read hook input from stdin
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Only check git commit commands
if ! echo "$COMMAND" | grep -q "git commit"; then
  exit 0
fi

# Check staged files for sensitive patterns
STAGED=$(git diff --cached --name-only 2>/dev/null)
BLOCKED_PATTERNS='\.(env|key|pem)$|credentials|secrets'

if echo "$STAGED" | grep -iE "$BLOCKED_PATTERNS" > /dev/null 2>&1; then
  echo "BLOCKED: Sensitive files detected in staged changes:" >&2
  echo "$STAGED" | grep -iE "$BLOCKED_PATTERNS" >&2
  echo "Remove them from staging before committing." >&2
  exit 2
fi

exit 0
```

**The config:**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-secrets.sh"
          }
        ]
      }
    ]
  }
}
```

**Walk through it:**
- **Event:** `PreToolUse` — fires before any tool executes
- **Matcher:** `"Bash"` — only triggers on Bash tool calls (not file edits, searches, etc.)
- The script checks if the command is a `git commit`
- Inspects staged files for sensitive patterns
- If found: **exit 2** — commit is blocked, Claude sees the error
- If clean: exit 0 — commit proceeds

> "This is a safety guardrail. You can put 'never commit .env files' in CLAUDE.md, and Claude will follow it most of the time. This hook makes it impossible. Exit code 2 is a hard stop."

### Example 3: Auto-format after file edits

Every time Claude writes or edits a file, run your formatter automatically. No more reviewing diffs full of formatting inconsistencies.

**The script (`.claude/hooks/auto-format.sh`):**

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Format based on file extension
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx)
    npx prettier --write "$FILE_PATH" 2>/dev/null
    ;;
  *.py)
    black "$FILE_PATH" 2>/dev/null
    ;;
  *.go)
    gofmt -w "$FILE_PATH" 2>/dev/null
    ;;
  *.rs)
    rustfmt "$FILE_PATH" 2>/dev/null
    ;;
esac

exit 0
```

**The config:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/auto-format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Walk through it:**
- **Event:** `PostToolUse` — fires after a tool completes
- **Matcher:** `"Edit|Write"` — only on file modifications
- Reads the file path from the hook input JSON
- Routes to the correct formatter by extension
- Always exits 0 — formatting is best-effort, shouldn't block Claude

### Example 4: Block destructive commands

Prevent `rm -rf`, `DROP TABLE`, `git push --force`, and other dangerous commands — even in `--dangerously-skip-permissions` mode.

```bash
#!/bin/bash
# .claude/hooks/block-dangerous.sh
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

DANGEROUS_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  "DROP TABLE"
  "DROP DATABASE"
  "git push.*--force.*main"
  "git push.*--force.*master"
  "git reset --hard"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED: Dangerous command detected: $pattern" >&2
    exit 2
  fi
done

exit 0
```

> "This is important: **hooks still fire even in bypass permissions mode.** That's by design. If you've set up guardrails with hooks, `--dangerously-skip-permissions` doesn't override them. Hooks are the last line of defense."

### Example 5: Inject context at session start

Load recent GitHub issues or team context automatically when a session starts.

```bash
#!/bin/bash
# .claude/hooks/load-context.sh
ISSUES=$(gh issue list --limit 5 --json title,number 2>/dev/null)

if [ -z "$ISSUES" ]; then
  exit 0
fi

jq -n --arg issues "$ISSUES" '{
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: "Recent open issues:\n\($issues)"
  }
}'
```

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/load-context.sh"
          }
        ]
      }
    ]
  }
}
```

> "Every time you start a Claude Code session, the five most recent GitHub issues are already in context. You don't have to ask. Claude just knows what's open."

---

## Advanced Hook Types (~2 min)

### Quick mention — prompt-based and agent-based hooks

Hooks aren't limited to shell scripts. Two advanced types add judgment to the deterministic system:

**Prompt hooks** — A fast LLM evaluates a condition:

```json
{
  "type": "prompt",
  "prompt": "Is this Bash command safe to run? Command: $ARGUMENTS. Reply 'safe' or 'dangerous' with a brief reason.",
  "timeout": 30
}
```

The LLM evaluates and returns a decision. Useful when the blocking condition requires understanding context, not just pattern matching.

**Agent hooks** — A full Claude model decides:

```json
{
  "type": "agent",
  "prompt": "Review this code change for security issues: $ARGUMENTS",
  "timeout": 60
}
```

More expensive, but handles complex judgment. Example: automatically reviewing every file write for security vulnerabilities.

> "These are powerful, but they're niche. 90% of hooks are shell scripts with `exit 2`. Start there. Move to prompt/agent hooks when you have a decision that requires understanding, not just pattern matching."

---

## The Decision Framework (~2 min)

### When to use what — the complete picture

Now that we've covered Parts 2-4, place everything in context:

| Mechanism | Deterministic? | Use when... |
|-----------|---------------|-------------|
| **CLAUDE.md** | No (guidance) | General conventions, context Claude needs every session |
| **Rules** (`.claude/rules/`) | No (guidance) | File-type or path-specific conventions |
| **Skills** | No (probabilistic) | Workflows where Claude's judgment about when to run is acceptable |
| **Hooks** | **Yes** | Rules that MUST be followed 100% of the time |

**The escalation ladder:**

```
  "Claude usually does this correctly"
      → Don't add anything. Let Claude be Claude.

  "Claude sometimes forgets this"
      → Add it to CLAUDE.md or a Rule.

  "Claude keeps ignoring this despite the rule"
      → The rule is getting lost in context. Promote to a hook.

  "This must happen every time, no exceptions"
      → Hook from the start. Don't bother with rules.

  "This must happen AND Claude can't override it"
      → PreToolUse hook with exit code 2.
```

### Getting started

> "You can ask Claude Code to write hooks for you. Try: 'Write a hook that runs eslint after every file edit' or 'Write a hook that blocks writes to the migrations folder.' Claude generates the script and the settings.json config."
>
> "Use `/hooks` to browse what's currently configured — it opens a read-only view showing all hooks by event, matcher, and source."

### Bridge to Part 5

> "Hooks give you deterministic control over what happens in a single Claude session. But what if the task is too big for one session? What if you need Claude to research a codebase without cluttering your conversation? What if you need multiple agents working in parallel on different parts of a feature?"
>
> "That's Part 5 — Subagents and Agent Teams."
