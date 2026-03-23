# Closing: Tying It All Together

---

## The Layered Architecture (~2 min)

We've covered a lot of ground. Let's zoom out and look at the whole picture — because all of these pieces fit together in a specific way.

```
┌─────────────────────────────────────────────────┐
│  Agent Teams (experimental, multi-session)       │
├─────────────────────────────────────────────────┤
│  Subagents (isolated workers, own context)       │
├─────────────────────────────────────────────────┤
│  Plugins (bundled shareable packages)            │
├─────────────────────────────────────────────────┤
│  MCP Servers (external tool connections)         │
├─────────────────────────────────────────────────┤
│  Hooks (deterministic lifecycle control)         │
├─────────────────────────────────────────────────┤
│  Skills (probabilistic prompt-based)             │
├─────────────────────────────────────────────────┤
│  Rules (.claude/rules/ - scoped guidance)        │
├─────────────────────────────────────────────────┤
│  CLAUDE.md (persistent project context)          │
├─────────────────────────────────────────────────┤
│  Permissions (safety & access control)           │
└─────────────────────────────────────────────────┘
```

**[Image placeholder: layered architecture diagram as a visual stack, color-coded by deterministic vs. probabilistic]**

Each layer builds on the one below. You don't need all of them on day one. Start with a good CLAUDE.md. Add hooks for the things that must be deterministic. Connect MCP servers for your actual tools. Build up from there as the need arises.

---

## The Mental Model That Matters (~2 min)

If there's one thing to take away from this session, it's the distinction between deterministic and probabilistic control. Everything we covered falls into one of those two categories.

| Layer | Type | Guarantee |
|---|---|---|
| CLAUDE.md / Rules | Guidance | Claude sees it, usually follows it |
| Skills | Probabilistic | Claude may auto-invoke, or you invoke manually |
| Subagents | Probabilistic | Claude may delegate, or you request it explicitly |
| Hooks | **Deterministic** | Runs every time, no exceptions |
| Permissions | **Deterministic** | Allow/deny enforced regardless of Claude's intent |

The rule of thumb is simple:

If something **must** happen 100% of the time — use a hook or a permission rule. Block secrets from commits. Run formatters on every edit. Deny force pushes. These are deterministic. Claude doesn't get a vote.

If something **should** happen when relevant — use a skill, a subagent, or CLAUDE.md guidance. Code review patterns. Architecture conventions. Research delegation. These are probabilistic. Claude uses judgment, and judgment is usually right — but not always.

When people get frustrated with Claude Code, it's almost always because they put something in the probabilistic category that belongs in the deterministic one. They write "never commit .env files" in CLAUDE.md and get burned when Claude does it anyway on a long session. The fix isn't a better prompt — it's a hook.

---

## Bridge to Session 2 (~1 min)

Session 2 is hands-on. We're going to take everything we just covered and actually build it.

You'll set up a real CLAUDE.md for your project. Configure hooks that enforce your team's conventions. Connect MCP servers to your actual tools. Write a custom skill. Build a subagent. And if time allows, spin up an agent team.

Come with a real project or codebase you want to work with. The more real the context, the more useful the session will be.

See you there.

---
