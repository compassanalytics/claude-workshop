# Part 4: MCP — Connecting Claude to Everything

---

## What MCP Actually Is (~2 min)

So far, everything we've covered — CLAUDE.md, rules, skills, hooks — operates within Claude Code's built-in capabilities. Claude can read files, run shell commands, and call the Anthropic API. That's it. If you need Claude to interact with your issue tracker, your database, your design tool, or your monitoring stack, it has no way to do that natively.

**Model Context Protocol** fixes that. MCP is an open standard — developed by Anthropic, now adopted widely — that defines how AI assistants connect to external tools. It uses a JSON-RPC-style protocol over stdio or HTTP. The important thing is you don't need to understand the protocol details. What matters is the mental model.

**[Image placeholder: MCP architecture diagram showing Claude Code in the center, with arrows pointing to MCP servers for GitHub, Jira, PostgreSQL, Figma, Slack]**

MCP servers are bridges. Each server exposes two things:

- **Tools** — callable functions. "Create a GitHub PR," "query this PostgreSQL table," "post a Slack message."
- **Resources** — readable data. Database records, API responses, document contents.

There's also a third primitive — **Prompts** — reusable templates for workflows, though you'll encounter tools and resources far more often in practice.

---

## What Becomes Possible (~2 min)

Without MCP, you'd have to copy-paste between Claude and your tools, or write custom shell scripts to bridge the gap. With MCP servers connected, Claude can work across your entire toolchain in a single conversation. Here are real examples of what that looks like:

- "Implement the feature described in JIRA issue ENG-4521 and create a PR on GitHub"
- "Check Sentry and Statsig to check usage of this feature"
- "Find emails of 10 users who used feature X, based on our PostgreSQL database"
- "Update our email template based on the new Figma designs posted in Slack"

Each of these would be painful without MCP — you'd be alt-tabbing, copying issue descriptions, pasting query results. With the right servers connected, Claude handles the entire workflow.

---

## Adding and Configuring Servers (~3 min)

### Adding a server

Two transport types. HTTP is recommended for remote services, stdio for local tools:

```bash
# HTTP (recommended for remote services)
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Stdio (for local tools)
claude mcp add postgres --command "npx" --args "-y @modelcontextprotocol/server-postgres"
```

That's it. Once added, Claude can see the tools that server exposes and use them in conversation.

### Configuration scopes

MCP servers follow the same scoping pattern you've seen with CLAUDE.md and settings:

| Scope | Where it lives | Who sees it |
|---|---|---|
| **Local** (default) | `~/.claude.json` under project path | Just you, this project |
| **Project** | `.claude/.mcp.json` | Committed to git, shared with your team |
| **User** | `~/.claude.json` | You, across all projects |

If your whole team needs the GitHub and Jira servers, put them in `.claude/.mcp.json` and commit it. If you personally use a Notion server for your own notes, keep it in your user config.

---

## The Ecosystem (~2 min)

The MCP ecosystem has grown quickly. Here are the servers you're most likely to reach for:

| Server | What it gives Claude |
|---|---|
| **GitHub** | PRs, issues, code search, reviews |
| **Atlassian** | Jira issues, Confluence pages |
| **Notion** | Pages, databases, comments |
| **Figma** | Design files, components, annotations |
| **Supabase** | Database queries, auth, storage |
| **Playwright** | Browser automation, testing, screenshots |
| **PostgreSQL** | Direct database queries |
| **Filesystem** | Extended file operations |
| **Context7** | Live library documentation |
| **Slack** | Messages, channels, threads |
| **Google Workspace** | Docs, Sheets, Gmail |

You don't need all of these. Connect the ones that match your actual workflow.

**[Image placeholder: grid or icon layout of key MCP ecosystem servers]**

---

## When Not to Overdo It (~1 min)

Every MCP server you connect adds to Claude's context. Each server's tools need to be described so Claude knows what's available, and that eats tokens.

The good news: MCP now supports **Tool Search**, which enables lazy loading. Instead of loading every tool description upfront, Claude discovers tools on demand. This reduces context usage by up to 95% for large server configurations.

But even with lazy loading, don't connect 50 servers "just in case." Each connection is a process running on your machine, and more tools means more potential for Claude to reach for the wrong one. Connect what you actually use. If you find yourself needing a server once a month, add it when you need it and remove it after.

The rule of thumb: if you wouldn't keep the app open on your desktop all day, don't keep the MCP server connected all day.

---
