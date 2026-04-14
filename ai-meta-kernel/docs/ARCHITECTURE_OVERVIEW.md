# Architecture Overview

## Purpose

AI Meta Kernel defines a reusable pre-agent reasoning layer. Its job is to prepare work before any specialized downstream agent acts.

The architecture is intentionally split:

- **Meta-Layer / Meta-Cognitive Kernel**: the core reusable system.
- **Downstream agents**: domain workers that consume kernel handoff objects.
- **Reference implementation**: the sibling `../macro-financial-intelligence-agent/` project, used to validate the kernel.

## High-Level Flow

```text
Raw user request
  -> Meta-Layer intake
  -> Task object construction
  -> Framing and reframe check
  -> Risk calibration
  -> Habit trigger selection
  -> Verification plan
  -> Challenge loop
  -> Handoff contract
  -> Downstream agent workflow
  -> Report / artifact / archive
  -> Retro and validation feedback
```

## Meta-Layer Responsibilities

The kernel must:

- Identify the user's request, goal, constraints, and implied success criteria.
- Detect ambiguity, hidden assumptions, urgency, and domain risk.
- Decide which reasoning habits apply.
- Define verification requirements before domain execution.
- Challenge weak framings, overconfident inferences, and unsafe shortcuts.
- Produce a handoff object that downstream agents can consume.
- Preserve uncertainty and unresolved questions.

The kernel must not:

- Overfit its decisions to a single downstream agent.
- Allow convenience to override risk or verification gates.
- Treat a polished report as equivalent to a verified report.

## Downstream Agent Responsibilities

Each downstream agent must:

- Accept the kernel handoff object as its starting point.
- Respect task scope, risk flags, verification requirements, and output constraints.
- Report evidence used, uncertainty, failed checks, and unresolved issues.
- Return information in a format that can be audited.

## Reference Agent Boundary

The macro-financial intelligence agent validates the kernel under high-change, evidence-sensitive conditions. It lives outside this kernel repo at `../macro-financial-intelligence-agent/` and monitors and synthesizes public information from Hong Kong, Macau, Taiwan, Japan, the United States, and Europe.

It is not a trading agent. Its expected outputs are evidence summaries, policy-risk notes, market-risk context, research reports, and archives.

## Core Artifacts

- `meta-layer/TASK_OBJECT_SCHEMA.json`: structured task object schema.
- `meta-layer/CONSTITUTION.md`: non-negotiable kernel principles.
- `meta-layer/RUNTIME_PIPELINE.md`: runtime sequence and gates.
- `meta-layer/prompts/KERNEL_SYSTEM_PROMPT.md`: first system prompt draft.
- `../macro-financial-intelligence-agent/ADAPTER_SPEC.md`: how the reference agent consumes kernel handoff.
- `validation/KERNEL_VALIDATION_MATRIX.md`: how kernel capabilities are tested.
