# AGENTS.md

Canonical source: `META_LAYER_MASTER_SPEC.md`. If this guide conflicts with that file, the master spec wins until intentionally revised.

## Project identity

This repository is **not** a single-purpose agent project.

It contains:

1. **Meta-Layer / Meta-Cognitive Kernel**
   - The primary and most important artifact in this repository.
   - A universal pre-processing thinking layer that all downstream agents must pass through first.
   - Responsible for framing, classification, structural decomposition, risk calibration, habit triggering, verification discipline, challenge checks, decision gates, status flags, and structured handoff.

2. **External reference agents**
   - These are validation implementations used to test whether the Meta-Layer is strong enough.
   - They are not allowed to redefine the Meta-Layer's purpose.
   - They should live outside this kernel repository.
   - The first reference implementation is the sibling project `../macro-financial-intelligence-agent/`.

## Top priority rule

If there is ever a conflict between:
- making a downstream agent more convenient, and
- preserving Meta-Layer integrity,

**preserve Meta-Layer integrity.**

## Repository goals

### Step 1 ??Build the formal Meta-Layer
The main goal of this repository is to produce a formally usable Meta-Layer / Meta-Cognitive Kernel that can be reused across future agents.

This includes:
- Constitution
- Runtime pipeline
- Habit modules
- Policies
- Decision gates
- Challenge loop
- Handoff contract
- Codex-ready system prompt
- Structured task object schema
- Structural decomposition contract
- Status flags

### Step 2 ??Validate Step 1 with a real reference agent
Reference agents exist to validate the Meta-Layer under realistic pressure.
They are not the final core deliverable.

## How to work in this repo

### When editing files under `/meta-layer/`
Focus on:
- consistency
- structure
- policy discipline
- unambiguous definitions
- reusable logic
- downstream handoff quality

Do **not** optimize these files for conversational style.
Optimize them for long-term maintainability and system coherence.

### When editing external reference agents
Treat each external agent as a validation harness for the Meta-Layer.

For every important workflow, ask:
- Which part of the Meta-Layer does this validate?
- Does this expose a framing gap?
- Does this expose a verification gap?
- Does this expose a challenge-loop weakness?
- Does this expose a handoff contract problem?
- Does this expose a policy interaction problem?

### When editing files under `/validation/`
Be explicit.
Turn vague concerns into:
- validation criteria
- failure cases
- retro items
- kernel improvement suggestions

## Rules for downstream agents

Downstream agents must not:
- bypass the Meta-Layer
- redefine user goals without explicit reframe logic
- ignore risk profile
- ignore required checks
- silently reconstruct missing kernel fields
- ignore status flags
- treat assumptions as facts
- suppress material uncertainty
- skip ethics constraints where applicable

Downstream agents should:
- accept structured handoff objects
- operate within the provided risk and verification boundaries
- return the task for reframe when material scope, decomposition, verification, or handoff fields are missing
- report back validation findings when the Meta-Layer is insufficient

## Preferred work pattern

1. Build or update structure first
2. Improve specs second
3. Only implement execution workflows after specs are clear
4. Prefer reviewable drafts over premature completeness
5. Keep files modular and narrowly scoped

## File-writing expectations

When creating or updating a spec file:
- Use clear headings
- Keep responsibilities narrow
- Avoid mixing identity, policy, workflow, and output contract in one file unless intentional
- Prefer durable system language over ad hoc prose
- Make future refactoring easier, not harder

## Special note for the Macro-Financial Intelligence Agent

This agent is **not** primarily a trading recommender.

It now lives outside this repository at `../macro-financial-intelligence-agent/`.

Its primary purpose is:
- evidence gathering
- source-aware synthesis
- macro/policy/risk monitoring
- research reporting
- validation of the Meta-Layer under complex real-world conditions

If a draft starts drifting toward direct trading advice as the main purpose, correct that drift.

## If uncertain

If you are unsure whether a change belongs to:
- Meta-Layer core logic, or
- reference-agent implementation details,

prefer preserving and clarifying the Meta-Layer first.
