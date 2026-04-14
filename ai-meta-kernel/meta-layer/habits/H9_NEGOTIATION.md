# H9: Negotiation / Mediation / Persuasion

## Purpose

Support conflict handling, persuasion, bargaining, mediation, and influence framing.

## Trigger Conditions

- The task involves different positions or interests.
- The user asks for persuasion, negotiation, alignment, or conflict resolution.

## Required Inputs

- parties involved
- stated positions
- suspected interests
- desired outcome
- non-negotiables, if any

## Internal Checks

1. Separate positions from interests.
2. Rank must-win, nice-to-have, and concession items.
3. Design persuasion framing.
4. Analyze process design.
5. Predict likely reactions.

## Expected Outputs

- `party_map`
- `position_interest_split`
- `concession_strategy`
- `persuasion_frame`
- `process_suggestion`

## Failure Modes

- Treating persuasion as one-way output.
- Negotiating positions without interests.
- Failing to prioritize concessions.

## Escalation Rules

- If role and motivation differences matter, add H10.
- If high-impact interests or fairness concerns exist, add H11.
