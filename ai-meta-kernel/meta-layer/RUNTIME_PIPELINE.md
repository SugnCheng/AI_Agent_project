# Runtime Pipeline

## Overview

The runtime pipeline defines the required sequence from raw request to downstream handoff.

```text
P0. Intake
P1. Normalize
P2. Frame
P3. Classify
P4. Trigger
P5. Decompose
P6. Calibrate
P7. Challenge
P8. Gate
P9. Emit
P10. Handoff
P11. Downstream execution
P12. Return and retro capture
```

## 1. Intake

Capture the raw request, user-stated goal, constraints, explicit output format, and relevant context.

Questions:

- What is the user asking for?
- What outcome would count as useful?
- Are there hidden time, jurisdiction, domain, or safety constraints?

## 2. Normalize / Task Object Construction

Normalize the request into the task object schema. Preserve raw text and distinguish between user-provided facts, inferred assumptions, and kernel-generated fields. Extract subject, task form, scope, time horizon, delivery expectations, and visible constraints.

## 3. Framing and Reframe Check

Determine whether the request is framed appropriately.

Trigger a reframe when:

- The goal is ambiguous.
- The request asks for a risky conclusion without enough evidence.
- The user asks for a downstream agent but the actual need is prior clarification.
- The request implies direct advice in a high-stakes domain.

## 4. Classify

Assign a primary task type and optional secondary task types:

- information
- analysis
- decision
- creation
- planning
- debugging
- negotiation
- ethical

Classification controls habit triggers, risk thresholds, verification standards, challenge depth, and downstream routing.

## 5. Habit Triggering

Select relevant cognitive habits. Every task must have at least one primary habit. Support habits cannot replace the primary habit.

Examples:

- H1 Evaluating Claims for factual claims and sources.
- H2 Analyzing Inferences for reasoning chains.
- H3 Weighing Decisions for tradeoffs.
- H5 Solving Problems for execution constraints.
- H11 Ethical Framing for harm, fairness, and misuse risk.

## 6. Structural Decomposition

Before handoff, separate:

- facts
- assumptions
- inferences
- unknowns
- hard and soft constraints
- stakeholders
- tradeoffs

This prevents downstream agents from inheriting vague or contaminated inputs.

## 7. Risk Calibration

Assign risk categories and severity. Consider:

- Financial, legal, medical, safety, privacy, security, reputational, and ethical risk.
- Time sensitivity and source freshness.
- Whether the output could be mistaken for professional advice.
- Whether the downstream agent must browse, verify, cite, or escalate.
- Ambiguity level, alignment need, and confidence ceiling.

## 8. Verification Planning

Define what must be checked and how. This may include source freshness, cross-source corroboration, schema validation, output review, or explicit uncertainty marking.

## 9. Challenge Loop

Challenge:

- The user's framing.
- The kernel's assumptions.
- The likely downstream execution path.
- Missing evidence.
- Overconfident conclusions.
- Stakeholder or externality blind spots.
- Whether the handoff is clear enough for domain execution.

The result may be proceed, proceed with constraints, ask clarification, narrow scope, or refuse/escalate.

## 10. Decision Gate

The kernel decides whether downstream execution is allowed.

Allowed outcomes:

- `proceed`
- `proceed_with_constraints`
- `clarify_first`
- `reframe_first`
- `escalate`
- `decline`

Before unrestricted handoff, the kernel must pass framing, trigger, separation, verification, challenge, and handoff gates.

## 11. Handoff Packaging

Produce a handoff object with:

- Task summary.
- Scope and non-goals.
- Risk profile.
- Triggered habits.
- Verification plan.
- Output expectations.
- Constraints for the downstream agent.
- Open questions and assumptions.
- `status_flags` and `downstream_recommendation`.

## 12. Downstream Execution

The downstream agent follows its adapter spec and must preserve kernel constraints.

## 13. Return and Retro Capture

After downstream execution, capture:

- What worked.
- What failed.
- Whether verification was sufficient.
- Whether the kernel handoff was complete.
- Whether the downstream agent exposed new kernel gaps.
