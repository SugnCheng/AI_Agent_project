# Memory Policy

Source of truth: `../../META_LAYER_MASTER_SPEC.md`.

## Policy Intent

Memory should improve continuity without creating false certainty.

## Memory Scope Separation

- **Long-term user memory**: stable goals, durable preferences, recurring task types, risk tolerance, common output formats.
- **Task memory**: framing, triggers, checks, assumptions, and intermediate outputs within one task.
- **Session memory**: recent clarifications, current limits, current focus, and same-session revisions.

## Admission Rules

Only store long-term memory when the information:

- has future value across multiple tasks;
- appears stable;
- improves future task quality;
- is explicit or strongly confirmed by the user.

## Prohibited Memory

Do not promote these into long-term memory:

- unverified inferences;
- one-off constraints;
- temporary moods or short-term preferences;
- facts that may quickly change;
- sensitive information not needed for future work.

## Provenance

Memory items should identify provenance:

- `user_explicit`
- `user_implied`
- `task_inferred`
- `system_generated`

Only `user_explicit` and high-confidence `user_implied` items may be considered for long-term memory.

## Conflict Handling

When new user statements conflict with memory, prefer the current explicit statement and flag the conflict for review.
