# Trigger Matrix

Source of truth: `../../META_LAYER_MASTER_SPEC.md`.

## Task-Type Routing

| Primary type | Primary habits | Support habits |
| --- | --- | --- |
| `information` | H1 | H2, H7 |
| `analysis` | H1, H2 | H4, H7, H11 |
| `decision` | H3 | H1, H2, H11 |
| `creation` | H6, H7 | H8, H3 |
| `planning` | H5, H3 | H10, H11 |
| `debugging` | H5, H2 | H1 |
| `negotiation` | H9, H10 | H3, H11 |
| `ethical` | H11 | H1, H2, H3 |

## Mandatory Overrides

- If external factual claims or time-sensitive information are present, add H1.
- If explanation, causation, or motive is requested, add H2.
- If the task requires choosing or recommending, add H3.
- If the task is open-ended research, add H4.
- If the task is obstacle-centered, add H5.
- If the task creates a deliverable, add H6 and H7.
- If visual or multimodal output is required, add H8.
- If persuasion or conflict is present, add H9.
- If role or motivation differences matter, add H10.
- If affected parties, externalities, fairness, privacy, safety, or power asymmetry are present, add H11.

## Priority Rules

- H11 overrides convenience and requires ethics note.
- H3 plus medium/high risk requires challenge loop.
- H1 with high verification need blocks definitive recommendation.
- H2 or H5 may force reframe if the core objective or constraints are wrong.
- H7 and H8 cannot dominate before framing is complete.
