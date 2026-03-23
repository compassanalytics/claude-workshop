# Part 8: Permissions & `--dangerously-skip-permissions`

---

## The Permission System (~2 min)

Claude Code asks for permission before executing anything potentially dangerous — bash commands, file modifications, network operations, dependency installation. This is correct from a security standpoint. You don't want an agent silently running `rm -rf` or `curl`-ing your credentials to a remote server.

But in practice, it creates real workflow friction. Claude asks roughly 100 permission prompts per hour during active sessions. That's a prompt every 36 seconds. And what happens is predictable: you stop reading them. You start rubber-stamping. Click accept, accept, accept without evaluating whether each operation is actually safe.

One LessWrong commenter put it well: this creates a false sense of security that may be *worse* than no permissions at all. You think you have a safety net, but you're not actually using it. You're just adding latency.

So the question becomes: how do you get the safety guarantees you need without the friction that undermines them?

---

## The Five Permission Modes (~3 min)

There are five ways to handle permissions, from most restrictive to least. Think of them as a spectrum.

**[Image placeholder: permission modes spectrum, from "Default" on the left to "Bypass" on the right, with friction decreasing and risk increasing]**

| Mode | How it works | When to use |
|---|---|---|
| **Default** | Prompts for everything potentially dangerous | First time using Claude Code, unfamiliar codebases |
| **Auto-accept (Shift+Tab)** | Proceeds without pausing, but remains interactive — you can still watch and intervene | Active pairing sessions where you're watching the output |
| **AllowedTools whitelist** | Configure specific tools/commands in `settings.json` that skip approval | Day-to-day development — allow your common commands |
| **Deny rules** | Explicitly block specific tools/commands (takes precedence over allow) | Guardrails for dangerous operations you never want |
| **`--dangerously-skip-permissions`** | Disables ALL permission checks | Containerized/sandboxed environments only |

The sweet spot for most people is a combination of AllowedTools and deny rules. You whitelist the commands you run constantly — `npm run`, `git commit`, version checks — and you explicitly deny the ones that are genuinely dangerous. More on that in a moment.

---

## The Flag Everyone's Curious About (~3 min)

Let's talk about `--dangerously-skip-permissions`. It does exactly what it says. No confirmation dialogs, no pauses, no human-in-the-loop. Claude executes whatever it decides to execute. It's technically equivalent to `--permission-mode bypassPermissions`.

Three critical details that most people miss:

**First — subagent inheritance.** When you run in bypass mode, ALL subagents inherit full autonomous access. You can't override this. You can't say "skip permissions for the main session but ask for subagents." It's all or nothing, and subagents get the same unrestricted access.

**Second — the name is deliberate.** There's no `-y` shortcut. No `--yes` alias. No abbreviated form. You type `--dangerously-skip-permissions` every single time. Anthropic made it inconvenient on purpose. The friction of typing that flag is the last line of defense.

**Third — hooks still fire.** Even in bypass mode, a `PreToolUse` hook can block a tool call. So if you have a hook that exits 2 on `rm -rf`, that hook still runs and still cancels the command. Hooks are the one safety mechanism that survives bypass mode.

### The real risks

These aren't theoretical.

In October 2025, a developer named Wolak reported that Claude Code executed `rm -rf` from root on a firmware project. The error logs showed thousands of "Permission denied" messages for system paths — the command tried to delete everything on the machine. The operating system's own file permissions were the only thing that limited the damage.

A study found that 32% of developers using the flag encountered unintended file modifications. 9% reported actual data loss.

### When it's actually appropriate

Anthropic's own engineers use bypass mode. But the context matters. Their blog post about building a C compiler with parallel Claude sessions includes the parenthetical: "(Run this in a container, not your actual machine.)"

That's the rule. Bypass mode belongs inside isolation boundaries:

- **Docker container or VM** with no access to your real filesystem
- **`--network none`** to prevent external connections
- **Git checkpoints** before every session so you can roll back
- **Well-scoped tasks** with clear specifications and test-driven verification

If you're not in a container, you probably shouldn't be using this flag.

---

## The Better Alternative (~2 min)

For most people, the right answer is granular AllowedTools configuration in `settings.json`. You get 90% of the speed without the risk.

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(* --version)",
      "Bash(uv run *)",
      "Bash(npx prettier *)"
    ],
    "deny": [
      "Bash(git push *)",
      "Bash(rm -rf *)"
    ]
  }
}
```

Allow patterns let Claude run common dev commands without asking. Deny patterns block operations you never want — and deny always takes precedence over allow. So even if `Bash(rm -rf *)` somehow matched an allow pattern, the deny rule wins.

**[Image placeholder: flowchart showing permission evaluation — deny checked first, then allow, then default prompt]**

Start by running Claude Code normally for a day. Pay attention to which permissions you're rubber-stamping — those are your allow list. Pay attention to which ones make you nervous — those are your deny list. Then configure accordingly.

Combine this with hooks for the operations that must be blocked deterministically. An AllowedTools deny rule prevents Claude from running a command. A `PreToolUse` hook with exit 2 does the same thing — but the hook can also inspect the arguments, check the environment, and make more nuanced decisions. Use both.

---
