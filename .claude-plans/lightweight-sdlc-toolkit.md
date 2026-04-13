# Lightweight SDLC Toolkit — Plan

## Goal

Build a prototype SDLC toolkit skill for `workshop-session-2/` that:
- Is a **working demo** participants can use during the workshop
- Shows spec-driven development in practice (not just theory)
- Maps directly to the presentation topics (persistence, knowledge flow, orchestration, parallelization)
- Has a `/sdlc` command with subcommands for each phase + a guide/help mode that explains the "why" behind each part
- Lightweight — single skill file, minimal state, easy to grok in 15 minutes

## Inspiration Sources

- **atelier-fashion/sdlc-toolkit**: 8 phases, `.sdlc/` directory, per-phase commands, knowledge loop via `/wrapup`
- **Julien's TDD**: Tickets as evolving specs, file-as-state, phase boundary protocol (shutdown agents → write findings → re-read)
- **Julien's deep-feature**: Fat tickets with context IDs (D###, R###), traceability chain, complexity-adaptive agent spawning
- **agent-swarm**: Parallel research agents, RARV verification, cross-swarm learning

## Design

### Invocation

Single command with subcommands (hybrid pattern from presentation Section 5):

```
/sdlc                    → show status + guide (what phase you're on, what's next)
/sdlc init [name]        → initialize a new feature workspace
/sdlc discover           → phase 1: interview user, capture intent + constraints
/sdlc research           → phase 2: explore codebase + external patterns
/sdlc plan               → phase 3: produce implementation plan from spec + research
/sdlc implement          → phase 4: execute the plan
/sdlc review             → phase 5: verify implementation against spec
/sdlc guide [topic]      → explain a concept from the presentation (context-decay, knowledge-flow, parallelization, etc.)
```

### Phases (5 — trimmed from atelier's 8 for lightweight)

| Phase | Reads | Writes | Key Concept Demonstrated |
|---|---|---|---|
| **discover** | nothing (or existing codebase) | `.sdlc/{feature}/spec.md` + `state.json` | Spec as contract, structured knowledge capture |
| **research** | `spec.md` | `research.md`, updates `knowledge.json` | Knowledge flow, context loading strategy (spec-anchored) |
| **plan** | `spec.md` + `research.md` + `knowledge.json` | `plan.md` | Cumulative reading, decisions + assumptions tracking |
| **implement** | `plan.md` + `spec.md` (spec-anchored) | code + updates `state.json` | Distributed reasoning, parallelization potential |
| **review** | `spec.md` + code diff | `review.md` | Fresh-context verification, anti-drift |

### State Management (from presentation Section 3)

```
.sdlc/
├── state.json              # active feature, global config
└── features/
    └── {feature-name}/
        ├── spec.md          # discovery output — the anchor
        ├── research.md      # research findings
        ├── knowledge.json   # decisions, assumptions, open questions
        ├── plan.md          # implementation plan
        ├── review.md        # review findings
        └── state.json       # phase status tracking
```

`state.json` per feature (explicit state from presentation):
```json
{
  "feature": "auth-system",
  "currentPhase": "research",
  "phases": {
    "discover": { "status": "complete" },
    "research": { "status": "in-progress" },
    "plan":     { "status": "not-started" },
    "implement":{ "status": "not-started" },
    "review":   { "status": "not-started" }
  }
}
```

### Guide Mode (the teaching part)

`/sdlc guide` maps presentation concepts to what participants just experienced:

| Topic | Ties To |
|---|---|
| `context-decay` | Why we write artifacts instead of relying on chat history |
| `spec-anchor` | Why spec.md is loaded in every phase |
| `knowledge-flow` | How decisions/assumptions/questions survive via knowledge.json |
| `persistence` | The .sdlc/ directory layout and why it's designed this way |
| `orchestration` | How /sdlc reads state.json to know what phase to run next |
| `parallelization` | How independent features or research agents could run concurrently |
| `re-run-safety` | What happens when you re-run a phase (acknowledgment, not overwrite) |

### What Makes It Lightweight vs Full TDD/Atelier

- **No MCP servers** — pure file-based state
- **No knowledge graph** — simple knowledge.json with flat arrays
- **No parallel agents** — single-threaded phases (but guide explains how you'd add them)
- **No ticket system** — one feature at a time
- **No hooks** — no enforcement, just convention
- **Single SKILL.md** — everything in one file, easy to read and learn from

## File Plan

```
workshop-session-2/
└── skills/
    └── sdlc/
        └── SKILL.md          # The entire toolkit — phases, guide, state management
```

One new skill alongside the existing `sdlc-coach`. The coach helps you *design* a plugin. The toolkit *is* a working plugin you can use and learn from.

## Implementation Steps

1. Write `skills/sdlc/SKILL.md` with:
   - Frontmatter (name, description, triggers, argument-hint)
   - Argument routing (init/discover/research/plan/implement/review/guide + bare status)
   - Phase instructions for each of the 5 phases
   - Guide mode with topic explanations
   - State management conventions
   - Re-run safety handling

2. Update `plugin.json` to add Julien as co-author

3. Test that `/sdlc` invocation routes correctly
