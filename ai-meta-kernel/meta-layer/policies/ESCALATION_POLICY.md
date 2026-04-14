# Escalation Policy

Source of truth: `../../META_LAYER_MASTER_SPEC.md`.

## Policy Intent

Escalation increases review depth when risk, ambiguity, verification, ethics, or specialization demands exceed the normal path.

## Escalation Categories

- risk escalation
- ethics escalation
- verification escalation
- ambiguity escalation
- downstream specialization escalation
- user clarification escalation

## Risk Escalation

Escalate when a task affects capital, health, legal standing, safety, privacy, security, reputation, rights, or other high-impact outcomes.

Required actions:

- raise kernel mode to K3 when appropriate;
- strengthen challenge loop;
- restrict handoff if critical gates fail.

## Ethics Escalation

Escalate when a task may harm others, create unfairness, invade privacy, reinforce bias, or create externalities.

Required actions:

- trigger H11;
- add `ethics_escalated`;
- include impacted parties and boundaries.

## Verification Escalation

Escalate when a recommendation depends on unverified critical facts.

Required actions:

- add `needs_verification`;
- lower confidence ceiling;
- prevent unrestricted recommendation.

## Ambiguity Escalation

Escalate when repeated framing does not resolve core uncertainty.

Required actions:

- add `needs_user_clarification`;
- ask focused clarification questions;
- avoid stacking speculative assumptions.

## Specialization Escalation

Escalate to a downstream domain agent only after the kernel has created a usable task object and handoff constraints.
