# Reframe Protocol

Source of truth: `../META_LAYER_MASTER_SPEC.md`.

## When to Reframe

Reframe when:

- the surface request differs from the core goal;
- the task is too broad or vague;
- constraints are missing or wrong;
- means and ends are confused;
- a downstream agent reports insufficient handoff;
- the requested form is unsafe but a safer research or decision-support framing exists.

## Output

A reframe must include:

- revised objective;
- narrowed scope;
- clarified success criteria;
- updated task classification;
- updated triggered habits;
- open questions.

## Return Format

```json
{
  "reframe_reason": "string",
  "revised_objective": "string",
  "narrowed_scope": ["string"],
  "updated_triggers": ["string"],
  "questions_for_user": ["string"]
}
```
