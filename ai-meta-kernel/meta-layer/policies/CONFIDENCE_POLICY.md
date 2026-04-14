# Confidence Policy

Source of truth: `../../META_LAYER_MASTER_SPEC.md`.

## Policy Intent

Confidence must reflect evidence quality, ambiguity, risk, and verification status.

## Confidence Levels

- `low`: limited facts, unresolved ambiguity, unverified critical claims, or high-risk uncertainty.
- `medium`: adequate facts and framing, but some uncertainty or verification gaps remain.
- `high`: sufficient facts, verified critical information, stable framing, low ambiguity, and no major challenge-loop failure.

## Confidence Basis

Confidence depends on:

- facts completeness;
- verification status;
- inference ambiguity;
- task risk level;
- challenge-loop result;
- whether assumptions are explicit.

## Forced Downgrade

Do not mark confidence as high when:

- the answer depends on unverified assumptions;
- critical information is missing;
- plausible alternatives remain unresolved;
- the task is high-risk and verification is incomplete;
- user goals remain ambiguous;
- the challenge loop finds an unresolved major issue.

## Disclosure

Confidence labels must include a short rationale:

- why the label was chosen;
- what blocks higher confidence;
- what evidence or clarification would improve confidence.
