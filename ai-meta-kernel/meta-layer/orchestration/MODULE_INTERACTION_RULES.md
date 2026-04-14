# Module Interaction Rules

Source of truth: `../../META_LAYER_MASTER_SPEC.md`.

## Core Rules

### O1: Trigger Selection

Kernel selects primary and support habits from task classification, risk profile, and context complexity.

### O2: Primary Before Support

Every task must have at least one primary habit. Support habits cannot replace the primary habit.

### O3: Ethical Override

If H11 is triggered, recommendation-like output requires an ethics note and impacted-party check.

### O4: Decision Override

If H3 is triggered and risk is medium or higher, the full challenge loop is mandatory.

### O5: Evidence Override

If H1 finds verification need is high, downstream agents must not emit definitive recommendations until verification is completed or the output is restricted.

### O6: Reframe Override

If H2 or H5 reveals that the core objective or constraints are wrong, return to Frame stage.

### O7: Output Normalization

All habit outputs must be normalized into the shared task object so downstream agents receive one coherent handoff.

## Combination Patterns

- H1 + H2: evidence-sensitive analysis.
- H3 + H11: high-impact or ethically sensitive decision support.
- H5 + H6: feasible solution design.
- H7 + H8: written and multimodal presentation.
- H9 + H10: negotiation across role and motivation differences.
