# Decision Gates

Source of truth: `../META_LAYER_MASTER_SPEC.md`.

## Purpose

Decision gates determine whether the Meta-Layer may emit an unrestricted handoff, a restricted handoff, a reframe request, a clarification request, an escalation, or a decline.

## Gate A: Framing Gate

Question: Can the request be framed into a real objective?

Pass conditions:

- Surface request and core goal are separated.
- Success criteria are defined or explicitly marked as unknown.
- Material ambiguity is either resolved or flagged.

Failure flags:

- `needs_reframe`
- `needs_user_clarification`

## Gate B: Trigger Gate

Question: Have the required habits been activated?

Pass conditions:

- At least one primary habit is selected.
- Mandatory support habits are included.
- H11 is included when externalities, affected parties, fairness, privacy, safety, or power asymmetry are present.
- H1 is included for external factual claims or time-sensitive information.

Failure flags:

- `needs_reframe`
- `high_risk_restricted`

## Gate C: Separation Gate

Question: Are facts, assumptions, inferences, and unknowns properly separated?

Pass conditions:

- Structural decomposition is present.
- Constraints are split into hard and soft.
- Stakeholders and trade-offs are included when material.

Failure flags:

- `needs_reframe`
- `needs_user_clarification`

## Gate D: Verification Gate

Question: Has mandatory verification been completed or correctly flagged?

Pass conditions:

- Verification needs are classified.
- Required checks are explicit.
- Missing verification lowers confidence and restricts handoff.

Failure flags:

- `needs_verification`
- `high_risk_restricted`

## Gate E: Challenge Gate

Question: Has challenge depth matched the risk level?

Pass conditions:

- Low-risk tasks receive an appropriate lightweight challenge.
- Medium/high-risk tasks run the required challenge loop.
- Overconfidence, alternative explanation, missing constraints, and ethics/externality checks are applied where relevant.

Failure flags:

- `high_risk_restricted`
- `ethics_escalated`
- `needs_reframe`

## Gate F: Handoff Gate

Question: Is the downstream handoff structured enough for domain execution?

Pass conditions:

- Required handoff fields are present.
- Status flags match gate outcomes.
- Downstream recommendation mode is explicit.
- Open questions are included.

Failure flags:

- `needs_reframe`
- `needs_user_clarification`

## Gate Outcomes

- `standard_handoff`: all required gates pass.
- `restricted_handoff`: task may proceed only with explicit limits.
- `do_not_handoff`: a blocking gate failed.

If any gate fails, do not emit an unrestricted handoff.

## Contract Fields Controlled By Gates

- Gate A controls `framed_objective` and `status_flags`.
- Gate B controls `triggered_habits`.
- Gate C controls `structural_decomposition`.
- Gate D controls `required_checks`, `verification_plan`, and `risk_profile.confidence_ceiling`.
- Gate E controls `challenge_loop` and `downstream_recommendation.mode`.
- Gate F controls `handoff` and `downstream_recommendation`.
