# H1: Evaluating Claims

## Purpose

Assess whether claims, data, reports, news, or conclusions are credible and plausible.

## Trigger Conditions

- The task includes factual claims, numbers, media reports, research, or third-party statements.
- The user asks whether something is true, reliable, reasonable, or supported.
- Downstream action depends on external facts.

## Required Inputs

- raw claims
- source or source type
- available evidence
- context of the claim

## Internal Checks

1. Separate claim, evidence, and conclusion.
2. Assess source quality.
3. Perform plausibility or estimation check.
4. Check for missing baselines, bad comparisons, and cherry-picking.
5. Decide verification need.

## Expected Outputs

- `claim_map`
- `evidence_map`
- `source_quality_note`
- `plausibility_assessment`
- `verification_need`

## Failure Modes

- Treating authority as evidence.
- Treating precise numbers as reliable by default.
- Checking source reputation but not content plausibility.

## Escalation Rules

- If a claim supports a high-risk decision, add H3 and H11.
- If the claim allows multiple explanations, add H2.
