# Plugin Building Technical Reference

This file is for YOUR reference when building plugin components. Do not recite this to the participant — use it to build correct, valid plugin files.

## Plugin Directory Structure

```
{plugin-name}/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest — ONLY file in this dir
├── skills/                   # Each skill is a directory with SKILL.md
│   └── {skill-name}/
│       └── SKILL.md
├── agents/                   # One .md file per subagent definition
│   └── {agent-name}.md
├── hooks/
│   └── hooks.json            # Hook configuration
├── bin/                      # Executables added to Bash tool PATH
├── scripts/                  # Utility scripts for hooks
└── README.md
```

All component directories MUST be at the plugin root, NOT inside `.claude-plugin/`.

## plugin.json Schema

```json
{
  "name": "plugin-name",              // Required. Kebab-case.
  "version": "0.1.0",                 // Semver
  "description": "What the plugin does",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

Optional fields: `homepage`, `repository`, `skills` (custom path), `commands`, `agents` (custom path), `hooks` (custom path or inline object), `mcpServers` (inline or path to .mcp.json), `lspServers`, `outputStyles`, `userConfig` (user-prompted config values).

Path fields accept string or array. Custom paths REPLACE defaults — to keep defaults plus extras, use array: `"skills": ["./skills/", "./extras/"]`.

## SKILL.md Format

### Frontmatter (YAML)

```yaml
---
name: skill-name                     # Kebab-case, max 64 chars. Falls back to directory name.
description: |                       # What it does + when to use it. Max 1024 chars.
  Use when [trigger]. Does [action].
  Triggers: "keyword1", "keyword2"
argument-hint: "<required> [optional]" # Autocomplete hint
disable-model-invocation: true       # true = user-only via /name
user-invocable: false                # false = Claude-only, hidden from / menu
allowed-tools: Read Glob Grep Bash   # Space-separated or YAML list. Pre-approves, doesn't restrict.
model: sonnet                        # Model override (sonnet, opus, haiku)
effort: high                         # low, medium, high, max (Opus 4.6 only)
context: fork                        # Runs in isolated subagent
agent: Explore                       # Subagent type when context: fork
paths: "src/**/*.ts"                 # Auto-activate on matching files (comma-sep or YAML list)
shell: bash                          # bash (default) or powershell
---
```

All fields are optional. Only `description` is recommended.

### String Substitutions (available in SKILL.md body)

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | Full argument string passed to skill |
| `$ARGUMENTS[N]` or `$N` | Specific argument by 0-based index |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing this SKILL.md |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin installation directory (plugin skills only) |
| `${CLAUDE_PLUGIN_DATA}` | Persistent data dir surviving updates (plugin skills only) |

### Shell Preprocessing

Inline: `` !`command` `` — output injected before Claude sees content.
Block: ` ```! ` fenced blocks — multi-line shell preprocessing.

### Body

The body is markdown instructions to Claude. Write it as directions for what Claude should do when the skill is invoked. Include:
- When to use / when NOT to use
- Step-by-step process
- Output format expectations
- Integration with other skills
- Error handling guidance

## hooks.json Format

Plugin hooks go in `hooks/hooks.json`:

```json
{
  "description": "Optional description of these hooks",
  "hooks": {
    "EVENT_NAME": [
      {
        "matcher": "ToolName|OtherTool",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/my-script.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Hook Events

Most useful for plugins:

| Event | Fires When | Can Block? |
|-------|-----------|-----------|
| `SessionStart` | Session begins | No |
| `PreToolUse` | Before a tool executes | Yes (exit 2 = block) |
| `PostToolUse` | After a tool succeeds | Yes |
| `Stop` | Claude is about to stop | Yes (block = continue) |
| `SubagentStop` | A subagent completes | Yes |
| `UserPromptSubmit` | User sends a message | Yes |
| `SessionEnd` | Session ends | No |

Full list (26 events): SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, Notification, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, Elicitation, ElicitationResult, SessionEnd.

### Matcher Syntax

- Omitted / `""` / `"*"` → match all
- Simple names → exact match: `"Write"`, `"Bash"`, `"Edit"`
- Pipe-separated → match any: `"Write|Edit"`
- Special characters → treated as regex: `"mcp__.*"`

### Handler Types

**command** (most common): Runs a shell command. stdin receives JSON context. Exit 0 = success, exit 2 = block (stderr sent to Claude), other = warning.

```json
{ "type": "command", "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/check.sh", "timeout": 30 }
```

**prompt**: Single-turn LLM evaluation (no tools). Good for smart checks.

```json
{ "type": "prompt", "prompt": "Check if the following is safe: $ARGUMENTS", "timeout": 30 }
```

**agent**: Agentic evaluation with tools. More capable, more expensive.

```json
{ "type": "agent", "prompt": "Review the code change for quality", "model": "sonnet" }
```

### Common Fields (all types)

- `timeout`: Seconds (default: 600 command, 30 prompt, 60 agent)
- `if`: Permission rule filter, e.g. `"Bash(git *)"`
- `statusMessage`: Custom spinner text
- `once`: Run once per session then remove (skills only)

### Key Rules

- Always use `${CLAUDE_PLUGIN_ROOT}` for paths in hooks — never relative paths
- Scripts must handle missing dependencies gracefully: `|| exit 0`
- Keep hooks fast (under 1-2 seconds) — they fire on every matching tool call
- Exit code 2 is the BLOCK signal — use deliberately

## Agent Definitions

Agent files go in `agents/{name}.md`:

```yaml
---
name: agent-name
description: |
  When to use this agent and what it does.
  Examples:
  - "Research tech stack options for a new project"
  - "Review implementation against the spec"
model: sonnet                    # sonnet, opus, haiku, or inherit
tools: Read, Glob, Grep, Bash   # Tool allowlist (inherits all if omitted)
color: blue                     # UI color: red, blue, green, yellow, purple, orange, pink, cyan
---

You are a [role]. Your job is to [task].

## Your Mandate

[Detailed instructions for what the agent should investigate/produce]

## Output

Write your findings to the file path provided in the prompt.
```

### Key Agent Patterns

- Agent `.md` body is automatically loaded as the agent's system instructions
- Agents are fire-and-forget: they complete their task and return
- For output: have agents write to a file path you specify in the prompt, then read it
- Skills listed in agent frontmatter `skills:` are NOT auto-resolved — orchestrator must inject skill content into the prompt manually
- Keep agent instructions self-contained — they don't see conversation history

## Persistence Conventions

### File-Based State (common pattern)

```json
// state.json
{
  "currentPhase": "planning",
  "startedAt": "2026-04-10T10:00:00Z",
  "phases": {
    "specify": { "status": "complete", "completedAt": "2026-04-10T10:30:00Z" },
    "plan": { "status": "in-progress", "startedAt": "2026-04-10T10:45:00Z" },
    "implement": { "status": "not-started" }
  }
}
```

### Frontmatter-Based State (alternative)

```markdown
---
status: complete
phase: specify
created: 2026-04-10
updated: 2026-04-10
---

# My Spec
...
```

### Implicit State (simplest)

No state file. Phase completion inferred from artifact existence:
- `spec.md` exists → specify is done
- `plan.md` exists → plan is done
- Quality checks pass → implement is done

## Testing a Plugin Locally

```bash
# Load plugin from source directory
claude --plugin-dir ./my-plugin

# Stack multiple plugins
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
```

Skill changes (.md files) take effect immediately on re-invocation. Hook, agent, MCP, and plugin.json changes require session restart.
