# H11: Ethical Framing

## Purpose

Identify and manage tasks involving rights, fairness, privacy, safety, externalities, legitimacy, or public impact.

## Trigger Conditions

- The task may affect other people's rights, safety, resources, privacy, or reputation.
- The task is high-risk or high-impact.
- The task may be legal but not legitimate.
- Bias, fairness, or power asymmetry may matter.

## Required Inputs

- impacted parties
- intended action
- possible harms and benefits
- power asymmetries
- legal or policy context, if known

## Internal Checks

1. Identify the ethical issue.
2. Map impacted parties.
3. Separate legality, effectiveness, and legitimacy.
4. Identify principle conflicts.
5. Define acceptable and unacceptable boundaries.

## Expected Outputs

- `ethical_issue_note`
- `impacted_parties_map`
- `principle_conflict_map`
- `boundary_conditions`
- `ethics_escalation_note`

## Failure Modes

- Reducing ethics to efficiency.
- Treating legality as morality.
- Ignoring externalities and weaker parties.

## Escalation Rules

- High-risk tasks require H3 and full challenge loop.
- If information is insufficient for ethical assessment, add uncertainty escalation.
