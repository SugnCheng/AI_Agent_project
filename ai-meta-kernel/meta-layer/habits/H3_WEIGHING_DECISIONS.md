# H3: Weighing Decisions

## Purpose

Support choices, comparisons, prioritization, allocation, and go/no-go judgments.

## Trigger Conditions

- The task asks what to choose, prioritize, allocate, recommend, or avoid.
- Alternatives and trade-offs exist.
- A recommendation may influence action.

## Required Inputs

- decision objective
- options or candidate actions
- time horizon
- risk tolerance, if available
- stakeholders

## Internal Checks

1. List alternatives.
2. Compare short-term and long-term effects.
3. Assess costs, benefits, and risks.
4. Add stakeholder lens.
5. Check reversibility.
6. Identify key trade-offs.

## Expected Outputs

- `option_set`
- `tradeoff_map`
- `stakeholder_impact_map`
- `reversibility_note`
- `provisional_recommendation`

## Failure Modes

- Recommending without alternatives.
- Treating preference as objective optimum.
- Ignoring affected parties or time horizon.

## Escalation Rules

- Medium/high-risk decisions require full challenge loop.
- If decision depends on unstable facts, add H1.
- High-impact decisions require H11.
