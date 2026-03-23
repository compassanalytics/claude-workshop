# Part 7: Plugins — Bundling It All Together

---

## What Plugins Solve (~2 min)

By this point, you've seen skills, hooks, MCP servers, and subagents as individual concepts. Each one lives in its own file or config. That works fine when everything is scoped to a single repo. But what happens when you want the same workflow across multiple projects? Or when you want to share a setup with your team that includes a skill, a couple of hooks, and an MCP server that all work together?

You copy files around. You write setup instructions. Someone forgets a step. Things break.

**Plugins are the packaging layer.** They bundle any combination of skills, subagents, hooks, and MCP servers into a single installable unit. One install, everything configured.

---

## What a Plugin Contains (~2 min)

A plugin is a directory with a `.claude-plugin/plugin.json` manifest. Everything else is optional — you include what you need:

```
my-team-plugin/
├── .claude-plugin/
│   └── plugin.json       # Manifest: name, description, version
├── .mcp.json              # MCP server config (optional)
├── commands/              # Slash commands (optional)
├── agents/                # Subagent definitions (optional)
├── skills/                # Skill definitions (optional)
└── README.md
```

The `plugin.json` manifest is the only required piece — it declares the plugin's name, description, and version. The rest of the structure mirrors what you already know: skills go in `skills/`, subagents go in `agents/`, MCP config goes in `.mcp.json`, and hooks go in the settings.

**The decision rule is simple:** if it's just for one repo, keep things in `.claude/`. If you need the same workflow across multiple projects or across your team, bundle it into a plugin.

---

## Installing and Managing Plugins (~3 min)

### The plugin ecosystem (as of March 2026)

Plugins are distributed through marketplaces:

- **Official Anthropic marketplace** (`claude-plugins-official`) — these are automatically available, no extra setup needed.
- **Community marketplaces** — 43+ marketplaces with 834+ plugins catalogued. Install a marketplace first, then browse its plugins.

```bash
# Add a community marketplace
/plugin marketplace add <owner/repo>

# Install a plugin from any available marketplace
/plugin install <name>
```

### Scopes

Just like everything else in Claude Code, plugins support scoping:

| Scope | Who sees it | Use for |
|---|---|---|
| **User** | You, all projects | Personal workflow tools |
| **Project** | Committed, team-shared | Team standards and workflows |
| **Local** | You, this repo only | Project-specific personal tools |
| **Managed** | Admin-deployed | Organization-wide policies |

---

## LSP Plugins (~1 min)

Worth calling out specifically: the official marketplace includes **LSP plugins** — Language Server Protocol integrations that give Claude real code intelligence. Jump to definition, find references, see type errors immediately after edits.

These are configured per language and require the language server binary installed on your system. But when they're set up, Claude stops guessing about types and symbol locations — it uses the same language intelligence your editor does.

---

## When to Reach for a Plugin (~1 min)

Not everything needs to be a plugin. Here's the quick decision framework:

| Situation | Approach |
|---|---|
| One-off workflow for a single repo | Keep it in `.claude/` — skills, hooks, agents directly |
| Same workflow needed across 2-3 of your repos | Consider a user-scoped plugin |
| Team-wide standards and tooling | Project-scoped plugin, committed to each repo |
| Organization-wide policies and guardrails | Managed plugin, admin-deployed |

Plugins are the natural end state when a workflow matures. You start with a skill in one repo, realize you want it everywhere, and promote it to a plugin. The building blocks are the same — plugins just handle the distribution.

---
