# Status Flags

Source of truth: `../META_LAYER_MASTER_SPEC.md`.

## Purpose

Status flags control whether and how downstream agents may proceed. They are not decorative labels.

## Flag Definitions

### `ready_for_handoff`

The task object is sufficiently framed, decomposed, checked, and routed for downstream execution.

Allowed handoff:

- `standard_handoff`
- `restricted_handoff` if paired with unresolved caveats

### `needs_reframe`

The problem definition is incomplete, too broad, or likely wrong.

Required action:

- return to Frame stage;
- produce a narrower objective;
- update success criteria and triggers.

### `needs_verification`

The task depends on facts that must be checked before high-confidence output.

Required action:

- mark `must_verify`;
- lower confidence;
- restrict handoff until verification is complete or explicitly delegated.

### `needs_user_alignment`

User preference, value ordering, risk tolerance, or trade-offs materially affect the recommendation.

Required action:

- ask alignment questions, or
- provide a comparison framework instead of a final recommendation.

### `needs_user_clarification`

The missing information is material enough that assumptions would distort the answer.

Required action:

- ask the user for missing constraints or goals;
- avoid silent assumptions.

### `high_risk_restricted`

The task is high-risk, high-impact, or externally consequential.

Required action:

- use K3 High-Stakes Guarded Mode;
- strengthen verification and challenge loop;
- restrict downstream recommendation behavior.

### `ethics_escalated`

The task involves ethical, fairness, privacy, safety, affected-party, externality, or legitimacy concerns.

Required action:

- trigger H11;
- include ethics note and impacted parties;
- define acceptable and unacceptable boundaries.

## Flag Interaction Rules

- `ready_for_handoff` must not coexist with unresolved `needs_reframe`.
- `ready_for_handoff` may coexist with `needs_verification` only when the handoff is restricted and verification is delegated.
- `high_risk_restricted` should normally force full challenge loop.
- `ethics_escalated` forces H11.
- `needs_user_alignment` blocks final recommendation when preferences determine the outcome.

## Schema Semantics

`status_flags` is a top-level array in the task object. It must contain at least one flag and must not contain duplicates.

Flags control downstream behavior:

- blocking flags prevent `standard_handoff`;
- delegated unresolved flags may allow `restricted_handoff`;
- `ready_for_handoff` signals that handoff structure exists, not that every factual claim is verified.
