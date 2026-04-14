# H4: Facilitating Discovery

## Purpose

Support exploration, research design, hypothesis generation, model sketching, and test planning.

## Trigger Conditions

- The task is open-ended or research-oriented.
- The user wants new directions, patterns, hypotheses, or discovery paths.
- No clear solution path exists yet.

## Required Inputs

- observed phenomenon
- current knowledge boundaries
- available data or signals
- exploration objective

## Internal Checks

1. Generate multiple hypotheses.
2. Sketch a model for each useful hypothesis.
3. Derive testable predictions.
4. List next tests or data needs.
5. Distinguish model from reality.

## Expected Outputs

- `hypothesis_set`
- `model_sketches`
- `prediction_set`
- `next_test_plan`

## Failure Modes

- Treating a story as a model.
- Producing ideas without testable predictions.
- Overfitting to current observations.

## Escalation Rules

- If discovery leads to design, add H6.
- If selecting between hypotheses matters, add H3.
