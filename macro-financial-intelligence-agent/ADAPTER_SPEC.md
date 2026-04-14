# Macro-Financial Intelligence Adapter Spec

## Purpose

This adapter defines how the Macro-Financial Intelligence Agent consumes Meta-Layer handoff objects.

The agent is a reference implementation for validating the kernel. It is not the center of the project and must not bypass kernel controls.

`../ai-meta-kernel/META_LAYER_MASTER_SPEC.md` is the canonical source of truth for the kernel. This adapter may add finance-domain constraints, but it cannot weaken kernel framing, verification, challenge, ethics, or handoff requirements.

## Mission Boundary

The agent may perform:

- Public finance and macroeconomic news monitoring.
- Policy-risk monitoring across Hong Kong, Macau, Taiwan, Japan, the United States, and Europe.
- Financial-market risk context and evidence synthesis.
- Research report drafting.
- Source notes and archive/export preparation.

The agent must not perform:

- Direct trading instructions.
- Personalized investment recommendations.
- Unsupported predictions presented as certainty.
- Advice that implies professional financial, legal, or tax authority.

## Required Kernel Inputs

The adapter expects a handoff object containing:

- User goal.
- Geographic and market scope.
- Topic scope and non-goals.
- Task classification.
- `structural_decomposition` of facts, assumptions, inferences, unknowns, constraints, stakeholders, and `tradeoffs`.
- Risk profile.
- Freshness requirement.
- Citation requirement.
- Triggered habits.
- Verification plan.
- Required checks.
- Status flags.
- Expected report format.
- Open questions and assumptions.

If any of these are missing and material to the task, the adapter must return the task to the Meta-Layer rather than silently proceeding.

## Mapping From Kernel Fields

| Kernel field | Adapter use |
| --- | --- |
| `framed_objective.core_goal` | Defines research objective and report framing. |
| `framed_objective.scope` | Determines jurisdictions, topics, and source classes. |
| `framed_objective.non_goals` | Blocks advice, unsupported forecasting, or unrelated market commentary. |
| `risk_profile` | Sets caution level, disclaimer strength, and verification depth. |
| `triggered_habits` | Selects analysis checklist, especially claims, inference, decision, and ethics habits. |
| `structural_decomposition` | Prevents assumptions, inferences, and unknowns from being treated as facts. |
| `required_checks` | Determines which challenge-loop checks must be visible in output or validation notes. |
| `status_flags` | Determines whether the agent may proceed, restrict scope, or return for reframe. |
| `downstream_recommendation.agent_type` | Identifies this adapter as the target downstream agent type. |
| `downstream_recommendation.output_format` | Defines the expected report or archive format. |
| `verification_plan` | Determines source freshness, corroboration, and citation requirements. |
| `challenge_loop.result` | Determines whether to proceed, narrow, clarify, or return. |
| `handoff.expected_outputs` | Determines report structure and archive artifacts. |

## Adapter Workflow

1. Validate the handoff object.
2. Confirm the task is within the mission boundary.
3. Apply the kernel risk and verification requirements.
4. Ingest sources according to `SOURCE_POLICY.md`.
5. Separate facts, interpretations, uncertainty, and implications.
6. Produce evidence synthesis and policy/market-risk context.
7. Mark confidence and unresolved questions.
8. Export or archive according to the requested target.
9. Return validation notes to the kernel.

## Failure Behavior

Return to the Meta-Layer when:

- The request asks for direct trading advice.
- The jurisdiction or time window is unclear and material.
- Source freshness cannot satisfy the verification plan.
- Evidence conflicts cannot be resolved or clearly reported.
- The output format would hide uncertainty.

## Reference Validation Role

This adapter validates whether the kernel can produce handoffs that are complete enough for a high-change, evidence-sensitive research workflow.
