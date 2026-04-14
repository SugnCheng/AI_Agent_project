# Handoff Contract

Source of truth: `../META_LAYER_MASTER_SPEC.md`.

## Purpose

The handoff contract defines what the Meta-Layer must provide before any downstream agent may act.

Downstream agents do not receive raw user requests as their primary input. They receive a structured kernel task object.

## Required Handoff Fields

A handoff is incomplete unless it contains:

- `raw_request`
- `framed_objective`
- `task_classification`
- `risk_profile`
- `triggered_habits`
- `structural_decomposition`
- `required_checks`
- `status_flags`
- `downstream_recommendation`

Canonical JSON field naming:

- use `structural_decomposition`, not `structure`;
- use `tradeoffs`, not `trade_offs` or `trade-offs`;
- use `risk_profile.overall_level` and `risk_profile.categories`;
- use `downstream_recommendation.agent_type`, `mode`, `output_format`, `rationale`, and optional `restrictions`;
- use top-level `status_flags`.

## Canonical Field Semantics

| Field | Meaning |
| --- | --- |
| `risk_profile.overall_level` | Aggregate task risk after domain, ambiguity, reversibility, externality, and verification dependence are considered. |
| `risk_profile.categories` | Risk domains or features present in the task. `none_identified` must not be combined with other categories. |
| `triggered_habits` | H1-H11 modules selected by the kernel; at least one must be primary. |
| `structural_decomposition` | Facts, assumptions, inferences, unknowns, constraints, stakeholders, and tradeoffs. |
| `tradeoffs` | Explicit tensions between goals, risks, constraints, stakeholders, or time horizons. |
| `required_checks` | Verification, challenge, uncertainty-disclosure, and user-alignment checks required before commitment. |
| `status_flags` | Control flags determining whether handoff is ready, restricted, blocked, or escalated. |
| `downstream_recommendation` | Routing instruction to a downstream agent or workflow. |
| `downstream_recommendation.agent_type` | Target downstream agent category or adapter identifier. |
| `downstream_recommendation.output_format` | Expected downstream artifact shape. |

## Required Structural Decomposition

The kernel must separate:

- facts
- assumptions
- inferences
- unknowns
- hard constraints
- soft constraints
- stakeholders
- tradeoffs

No downstream agent may treat assumptions or inferences as facts.

## Downstream Agent Obligations

Downstream agents must:

- accept the handoff object as their starting point;
- preserve risk, verification, ethics, and uncertainty constraints;
- perform required checks assigned to them;
- report any missing material field back to the kernel;
- return validation findings when the kernel handoff is insufficient.

Downstream agents must not:

- bypass kernel framing;
- silently reconstruct missing fields;
- ignore `status_flags`;
- ignore `required_checks`;
- convert a restricted handoff into an unrestricted recommendation;
- hide uncertainty in final output.

## Return-To-Kernel Conditions

A downstream agent must request reframe or clarification when:

- `framed_objective.core_goal` is unclear;
- success criteria are missing and material;
- required facts, constraints, or time horizon are absent;
- `risk_profile` appears too low for the task;
- `required_checks` do not match the task type;
- `triggered_habits` omit a mandatory habit;
- `status_flags` include `needs_reframe`, `needs_user_clarification`, or unresolved `needs_verification`;
- the task asks the agent to violate the constitution.

## Handoff Modes

- `standard_handoff`: downstream execution may proceed within the stated scope.
- `restricted_handoff`: downstream execution may proceed only with explicit limits, caveats, or verification gaps.
- `do_not_handoff`: downstream execution is blocked until reframe, clarification, verification, or escalation is complete.

## Reframe Request Format

```json
{
  "reframe_reason": "string",
  "missing_fields": ["string"],
  "suggested_new_triggers": ["string"],
  "suggested_user_alignment_questions": ["string"]
}
```
