# Part 1: The Evolution — From Autocomplete to Agent Orchestration

---

## Opening (~1 min)

### Setting the stage

Alright, let's start with where we've been and where we are — because the speed of this shift is genuinely remarkable. We're going to walk through the last five years of AI-assisted coding, and I want to ground it in what actually happened, with dates, products, and real numbers. Not vibes.

The reason this matters: if you understand *how* we got here, the rest of the workshop — the config, the tools, the agent orchestration — stops feeling like a bag of tricks and starts feeling like the logical next step.

**[Image placeholder: timeline of AI coding evolution, four phases from 2021 to 2026]**

---

## The Journey — Four Phases (~10 min)

### Phase 1: Autocomplete (2021-2022) — "IntelliSense on steroids"

GitHub Copilot launches mid-2021, built on OpenAI's Codex. For the first time, AI is predicting entire lines and blocks of code from context. You're writing a function signature, and it fills in the body. You're writing a comment, and it writes the code underneath.

Impressive — but fundamentally passive. You type, it suggests, you accept or reject. Every decision is still yours. The developer drives every keystroke. Think of it like a really good autocomplete that occasionally reads your mind. The ceiling is "I type less." The floor is "I hit Escape a lot."

### Phase 2: Conversational coding (2023-early 2024) — "Ask it, don't just type"

ChatGPT drops in late 2022, GPT-4 follows in March 2023, and the interface changes completely. Copilot Chat arrives. AI stops being just inline suggestions and becomes a second interface for coding — you can ask for patterns, debug explanations, scaffolding, alternative implementations. Cursor launches in March 2023 as a VS Code fork with AI baked in.

At this stage it's still chat plus autocomplete. Powerful, yes — but the developer drives everything. You ask a question, you get an answer, you copy-paste it in, you verify it works. Quality control is entirely human. The AI is a knowledgeable colleague sitting next to you, but you're still the one with your hands on the keyboard.

### Phase 3: Agentic coding emerges (late 2024-2025) — "Delegate, don't dictate"

This is where the paradigm actually shifts.

Cursor ships Agent Mode in November 2024 — the AI can now read terminal output, run commands, make multi-file changes, and iterate on errors inside the IDE. Claude Code launches in February 2025 as terminal-native: no IDE at all, just an agent that reads your codebase, plans, executes, and loops. Copilot adds agent mode in May 2025. Codex, Windsurf, and others follow.

The AI isn't suggesting code anymore — it's *executing tasks*. You describe intent; the agent handles execution. "Add pagination to the users endpoint" stops being a prompt you paste into a chat window, and becomes a task the agent plans, implements across multiple files, runs the tests, and fixes its own errors.

Here's a number that tells the story: by late 2025, Cursor reports a dramatic flip. Where they once had 2.5x more tab-completion users than agent users, they now have 2x more agent users than tab users. The majority of their user base shifted from "suggest code for me" to "do the task for me" in under a year.

**The key distinction here:** agentic isn't one tool — it's a mode of working that all the major players converged on roughly simultaneously. Cursor does it inside the IDE. Claude Code does it in the terminal. Copilot does it across GitHub. Different interfaces, same fundamental shift from "you type, AI suggests" to "you describe, AI executes."

### Phase 4: Multi-agent orchestration (early 2026 — where we are now)

And now we're here. Agent teams. Parallel execution. Peer-to-peer communication between agents. One lead coordinates, teammates work independently with their own context windows. You're not just delegating a single task anymore — you're managing a team of AI engineers working in parallel.

We've gone from "AI autocomplete" to "managing a team of AI engineers" in under five years. That's the trajectory. And it's why "I use Copilot for suggestions sometimes" and "I orchestrate multiple agents working on my codebase" are now fundamentally different skill sets.

**[Image placeholder: four-phase diagram showing the shift from passive to autonomous — autocomplete, chat, single agent, multi-agent]**

---

## Where We Actually Are Right Now — The Numbers (~5 min)

### Adoption

Let's ground this in real data. These come from Anthropic's 2026 Agentic Coding Trends Report, the Sonar State of Code survey, Stack Overflow, and independent studies.

- **84%+ of developers** are now using or planning to use AI coding tools (Stack Overflow 2025). 51% of professional developers use AI daily.
- **64% of developers** have started using agentic AI tools specifically — 25% regularly, another 39% experimenting (Sonar State of Code 2026).
- **41% of all code** is now estimated to be AI-generated (global estimates, early 2026).

So the question is no longer "are people using this." The question is "how well are people using this."

### Productivity

- **Developers save ~3.6 hours per week** on average; daily users save more. 75% say AI reduces "toil work" — the repetitive, low-creativity stuff nobody enjoys. That's from the DX Q4 2025 report, surveying 135,000+ developers.
- **22% of merged code** is AI-authored based on actual repo telemetry (DX analysis). Not survey responses — actual commit data.
- GitHub studied 129K+ projects and found **15-22% agent adoption** — remarkable for technology that's only been available for months.

### Enterprise case studies

These are the ones that tend to land with people who are still on the fence:

- **Rakuten:** Claude Code completed activation vector extraction across a 12.5 million-line codebase in 7 autonomous hours, achieving 99.9% numerical accuracy.
- **TELUS:** 13,000+ custom AI solutions, engineering code shipped 30% faster, 500,000 total hours saved.
- **Zapier:** 89-97% AI adoption across their *entire* organization — not just engineering.
- **Stripe:** Cursor adoption went from single digits to over 80% of developers.
- **Salesforce:** 90% of 20,000 developers using AI coding tools.

These aren't startups experimenting. These are large organizations seeing measurable results at scale.

---

## Where It's All Headed (~2 min)

### The near-term

This section is about giving everyone a reason to invest in learning the tooling properly — because it's not slowing down.

**In 2026,** agents are progressing from short tasks to work that continues for hours or days. Multi-agent coordination is becoming standard — not just parallelism, but agents that share findings, challenge each other, and coordinate independently. And non-engineers — security, ops, design, data, legal, marketing — are starting to build their own tools using agents.

### The convergence

Compare Claude Code, Codex, Copilot CLI, Gemini CLI, Cursor, Windsurf — they're all converging on the same architecture under the hood. Config files (CLAUDE.md, AGENTS.md). Tool use. Multi-step planning. Agent delegation. The open standards — MCP for tools, Agent Skills spec for skills — mean skills work across Claude Code, Codex CLI, Gemini CLI, and Cursor without modification. This isn't a walled garden; the ecosystem is standardizing.

That's actually good news for you. The patterns you learn today aren't locked to one vendor.

### The role shift

Anthropic's report frames it bluntly: engineering is shifting from writing code to *orchestrating agents that write code*. The developer becomes a conductor, not a composer. The gap between "person who prompts a chatbot" and "person who orchestrates an AI workforce" is widening fast.

That's what this workshop is about — making sure everyone in the room is on the right side of that gap.

---

## The Honest Caveats (~2 min)

### What's still hard

I want to be upfront about the limitations too, because overselling this helps nobody.

- **Developers still fully delegate only 0-20% of tasks.** This isn't "AI replaces you" — it's "AI amplifies you." The vast majority of work is still collaborative, not autonomous. That's from Anthropic's own report.
- **CodeRabbit's analysis found roughly 1.7x more issues in AI-coauthored PRs.** Verification matters. The code gets written faster, but that doesn't mean it's correct by default.
- **Long sessions suffer from context rot.** Assumptions compound. The agent starts confidently building on mistakes it made 200 messages ago.
- **75% of devs still manually review every AI snippet before merging.** That's healthy — and it's going to stay that way for a while.
- **The tools are powerful but need proper setup to be reliable.** Which is exactly what the rest of this session covers.

So the framing for everything that follows: these tools are genuinely transformative when configured well, and genuinely frustrating when they're not. Let's make sure yours are configured well.
