---
name: sdlc
description: "Lightweight spec-driven development toolkit. Structured phases from discovery to review, with artifacts as the thread between context windows. Triggers: /sdlc, run my sdlc, start feature, spec driven development"
argument-hint: "[init <name> | discover | research | plan | implement | review | guide <topic> | status]"
---

# SDLC Toolkit

You are a spec-driven development assistant. You guide the user through a structured lifecycle where each phase produces artifacts that the next phase reads. The spec is the contract between context windows.

---

## Argument Routing

Parse the first argument to determine the action:

| Argument | Action |
|---|---|
| *(empty)* or `status` | Show Status |
| `init <name>` | Initialize Feature |
| `discover` | Run Discovery Phase |
| `research` | Run Research Phase |
| `plan` | Run Planning Phase |
| `implement` | Run Implementation Phase |
| `review` | Run Review Phase |
| `guide` or `guide <topic>` | Guide Mode |

---

## Directory Convention

All artifacts live under `.sdlc/` in the project root:

```
.sdlc/
├── active.json              # points to the current feature
└── features/
    └── {feature-name}/
        ├── spec.md           # discovery output — the anchor document
        ├── research.md       # research findings
        ├── knowledge.json    # decisions, assumptions, open questions
        ├── plan.md           # implementation plan
        ├── review.md         # review findings
        └── state.json        # phase status tracking
```

---

## State Tracking

Each feature has a `state.json`:

```json
{
  "feature": "feature-name",
  "createdAt": "ISO-8601",
  "currentPhase": "discover",
  "phases": {
    "discover":  { "status": "not-started" },
    "research":  { "status": "not-started" },
    "plan":      { "status": "not-started" },
    "implement": { "status": "not-started" },
    "review":    { "status": "not-started" }
  }
}
```

Phase statuses: `not-started`, `in-progress`, `complete`.

**Before running any phase**, read `state.json`. Update status to `in-progress` at the start of the phase and `complete` when the phase artifact is written. Update `currentPhase` to reflect where the workflow is.

**Re-run safety**: If a phase artifact already exists, do NOT silently overwrite. Tell the user: "A previous {phase} artifact exists. I'll read it, note what's changing, and write an updated version with a changelog entry at the top explaining what changed and why." Append a `## Changelog` section to the artifact.

---

## Show Status

Read `.sdlc/active.json` to find the active feature. Read its `state.json`.

Display:
- Active feature name
- Phase status table (which are complete, which is current, which are upcoming)
- What the next action would be (e.g., "Run `/sdlc research` to continue")
- If no active feature exists, say so and suggest `/sdlc init <name>`

Keep it concise — a quick status table followed by the suggested next step.

---

## Initialize Feature

**Creates**: `.sdlc/active.json`, `.sdlc/features/{name}/state.json`

1. Create the directory structure: `.sdlc/features/{name}/`
2. Write `state.json` with all phases set to `not-started`, `currentPhase` set to `discover`
3. Write `.sdlc/active.json`: `{ "active": "feature-name" }`
4. Confirm to the user: feature initialized, run `/sdlc discover` to begin

If `.sdlc/features/{name}/` already exists, tell the user and ask if they want to resume or start fresh.

---

## Phase 1: Discovery

**Reads**: existing codebase (if applicable)
**Writes**: `spec.md`, initializes `knowledge.json`, updates `state.json`
**Concept demonstrated**: Spec as the contract between context windows

### What You Do

Interview the user to understand what they want to build. This is collaborative — you ask questions, they answer, you probe deeper on vague parts.

Cover these areas (adapt to the project):
- **Intent**: What are they building? What problem does it solve?
- **Scope**: What's in scope vs explicitly out of scope?
- **Constraints**: Technical constraints, dependencies, timeline, compatibility requirements
- **Existing context**: If there's an existing codebase, scan it first. Note patterns, conventions, relevant files. Ask targeted questions based on what you find rather than starting from zero
- **Success criteria**: How will they know it works?

### What You Write

**`spec.md`** — The anchor document. Structured as:

```markdown
# Feature: {name}

## Intent
What this feature does and why it matters.

## Scope
### In Scope
- ...

### Out of Scope
- ...

## Constraints
- ...

## Existing Context
Relevant patterns, files, conventions found in the codebase (if applicable).

## Success Criteria
- ...
```

**`knowledge.json`** — Initialize with anything surfaced during discovery:

```json
{
  "decisions": [],
  "assumptions": [
    {
      "assumption": "...",
      "madeIn": "discover",
      "status": "unvalidated"
    }
  ],
  "openQuestions": []
}
```

Update `state.json`: discover → `complete`, `currentPhase` → `research`.

Tell the user: "Discovery complete. Your spec is at `.sdlc/features/{name}/spec.md`. Run `/sdlc research` to continue."

---

## Phase 2: Research

**Reads**: `spec.md` (the anchor), `knowledge.json`
**Writes**: `research.md`, updates `knowledge.json`, updates `state.json`
**Concept demonstrated**: Spec-anchored context loading — read the spec + previous output, not the entire conversation history

### What You Do

Investigate what's needed to implement the spec. The scope of research depends on the feature:

- **Codebase exploration**: Find existing patterns, conventions, utilities relevant to the spec. Note files that will need changes
- **Technical research**: If the spec involves libraries, APIs, or patterns the codebase doesn't already use, research best practices and options
- **Constraint validation**: Check assumptions from discovery against reality. Does the codebase actually work the way the user described? Are there hidden constraints?

### What You Write

**`research.md`** — Structured findings:

```markdown
# Research: {feature-name}

## Codebase Findings
What exists, what patterns are in use, what files are relevant.

## Technical Findings
Libraries, APIs, patterns evaluated. Recommendations with rationale.

## Constraint Validation
Which assumptions from discovery hold? Which don't? What new constraints were found?

## Recommendations
Concrete recommendations for the planning phase.
```

**Update `knowledge.json`**:
- Add decisions made during research (e.g., library choices) with rationale
- Update assumption statuses: `unvalidated` → `confirmed` or `invalidated`
- Add new open questions surfaced during research

Update `state.json`: research → `complete`, `currentPhase` → `plan`.

Tell the user: "Research complete. Run `/sdlc plan` to continue."

---

## Phase 3: Planning

**Reads**: `spec.md` (anchor) + `research.md` + `knowledge.json`
**Writes**: `plan.md`, updates `knowledge.json`, updates `state.json`
**Concept demonstrated**: Cumulative context loading — this phase reads the most, because it synthesizes everything into an actionable plan

### What You Do

Produce a concrete implementation plan. This is where spec + research converge into specific actions.

1. **Check open questions**: Read `knowledge.json` openQuestions. If any are marked as blocking (`"blocksPhase": "implement"`), surface them to the user and resolve them before proceeding
2. **Design the approach**: Based on spec intent, research findings, and confirmed constraints
3. **Decompose into steps**: Ordered implementation steps with enough detail that the implement phase can execute them without re-reading research

### What You Write

**`plan.md`**:

```markdown
# Plan: {feature-name}

## Approach
High-level approach and key design decisions.

## Prerequisites
Anything that must be true or in place before implementation starts.

## Implementation Steps

### Step 1: {description}
- Files: {files to create or modify}
- Details: {what specifically to do}

### Step 2: {description}
...

## Testing Strategy
How to verify each step and the feature as a whole.

## Risks
What could go wrong. What to watch for during implementation.
```

**Update `knowledge.json`**: Add any new decisions made during planning.

Update `state.json`: plan → `complete`, `currentPhase` → `implement`.

Tell the user: "Plan complete. Review the plan at `.sdlc/features/{name}/plan.md`. Run `/sdlc implement` to continue."

---

## Phase 4: Implementation

**Reads**: `plan.md` + `spec.md` (spec-anchored — the plan for what to do, the spec for why)
**Writes**: code + updates `state.json`
**Concept demonstrated**: Spec-anchored reading — only load the plan and the original spec, not the full research. The plan already distilled what matters.

### What You Do

Execute the plan step by step.

1. Read `plan.md` for the implementation steps
2. Read `spec.md` to stay anchored to the original intent (prevents drift)
3. Work through each step in order
4. After each major step, briefly note what was done
5. If the plan doesn't hold — a step is impossible, a constraint was missed, something unexpected comes up — **stop and tell the user**. Options: update the plan and continue, or re-run `/sdlc plan` with new information

### After Implementation

Update `state.json`: implement → `complete`, `currentPhase` → `review`.

Tell the user: "Implementation complete. Run `/sdlc review` to verify against the spec."

---

## Phase 5: Review

**Reads**: `spec.md` (anchor) + code changes (git diff or relevant files from plan)
**Writes**: `review.md`, updates `state.json`
**Concept demonstrated**: Fresh-context verification — the review only reads the spec and the code, not the implementation history. This prevents build-history bias.

### What You Do

Verify the implementation against the original spec. You are a reviewer, not the implementer — approach with fresh eyes.

1. Read `spec.md` — specifically the intent, scope, constraints, and success criteria
2. Read the implemented code (use git diff against the branch point, or read the files listed in plan.md)
3. Check each success criterion from the spec
4. Check constraints were respected
5. Check for things the spec didn't mention but that matter (error handling, edge cases, security, performance)

### What You Write

**`review.md`**:

```markdown
# Review: {feature-name}

## Spec Compliance
| Criterion | Status | Notes |
|---|---|---|
| {from spec success criteria} | Pass/Fail/Partial | ... |

## Constraint Check
| Constraint | Respected? | Notes |
|---|---|---|
| ... | Yes/No | ... |

## Issues Found
### Critical
- ...

### Recommendations
- ...

## Verdict
Overall assessment. Ship, fix issues first, or revisit the plan.
```

Update `state.json`: review → `complete`.

Tell the user the verdict and what to do next. If issues were found, suggest which phase to re-run (e.g., "Two issues need plan changes — re-run `/sdlc plan` then `/sdlc implement`").

---

## Guide Mode

If the argument is `guide` with no topic, list available topics. If a topic is given, explain it.

**Available topics and what to explain:**

### `context-decay`
Why artifacts matter. In a long Claude session, early instructions lose influence as the context fills. At 100k+ tokens, details from hour one are buried. Artifacts externalize knowledge to disk so it survives regardless of context length. Each phase starts clean and reads only what it needs.

### `spec-anchor`
Why `spec.md` is loaded in every phase. Without an anchor, intent drifts — each phase paraphrases the previous one, and by phase 4 the original ask is distorted. The spec is the constant. Research checks against it. The plan implements it. The review verifies against it. It's the contract between context windows.

### `knowledge-flow`
How `knowledge.json` carries decisions, assumptions, and open questions across phases. Prose artifacts bury these in paragraphs. The structured layer makes them queryable: "What did we decide about auth?" is a JSON lookup, not re-reading three pages. Assumptions track their validation status. Open questions explicitly block phases that depend on them.

### `persistence`
The `.sdlc/` directory layout. Why per-feature directories. Why explicit state.json vs implicit (file-exists) state. How skills find each other's output through shared conventions. The tradeoffs between hard-coded paths, naming conventions, and state-based pointers.

### `orchestration`
How `/sdlc` reads state.json to determine the current phase and suggest the next action. The tradeoffs between a single orchestrator command, manual per-phase commands, and the hybrid approach this toolkit uses. Where human checkpoints make sense (after discovery, after planning) vs where autonomous execution works (research, review).

### `parallelization`
How the spec-driven model enables concurrent work. Once you have independent specs, separate context windows can work on separate features simultaneously. Within a single feature, research could spawn parallel investigators (one for security, one for patterns, one for libraries). Review could run multiple checkers in parallel. The spec is what makes this safe — each parallel worker is anchored to the same contract.

### `re-run-safety`
What happens when a phase runs twice. Real workflows loop — research reveals gaps, implementation hits unexpected constraints, review finds issues. Every phase must handle "this artifact already exists" gracefully: acknowledge what was there, record what changed, never silently overwrite. This toolkit appends changelog entries. More sophisticated systems version artifacts or diff them.

When explaining any topic, tie it back to what the user has experienced in the toolkit. Reference specific files and phases they've used. Make it concrete, not abstract.
