# H2: Analyzing Inferences

## Purpose

Evaluate reasoning from facts to conclusions and prevent a single plausible explanation from being treated as the only explanation.

## Trigger Conditions

- The task asks for causation, motive, interpretation, explanation, or trend inference.
- The same evidence can support multiple conclusions.
- Pattern interpretation is required.

## Required Inputs

- known facts
- observed patterns
- current hypothesis, if any
- context boundaries

## Internal Checks

1. Separate observation from inference.
2. Generate 2-3 plausible hypotheses.
3. Check for confounders and mistaken causality.
4. Identify evidence that would discriminate between explanations.
5. Mark the current best inference as provisional.

## Expected Outputs

- `observation_set`
- `competing_hypotheses`
- `current_best_inference`
- `discriminating_evidence_needed`
- `confidence_note`

## Failure Modes

- Treating correlation as causation.
- Keeping only the most comfortable explanation.
- Hiding provisional reasoning.

## Escalation Rules

- If inference leads to a decision, add H3.
- If inference has social, ethical, or externality impact, add H11.
