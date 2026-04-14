# Reframe Policy

Source of truth: `../../META_LAYER_MASTER_SPEC.md`.

## Policy Intent

Reframing prevents the system from solving the wrong problem.

## Mandatory Reframe Cases

Reframe when:

- the surface request differs materially from the core goal;
- the task is too broad, vague, or not executable;
- constraints are missing or wrong;
- the task confuses means and ends;
- the user asks for an unsafe form of advice when a safer research or decision-support framing is appropriate;
- a downstream agent returns a reframe request.

## Reframe Output Requirements

A reframe should include:

- revised objective;
- narrowed scope;
- clarified success criteria;
- updated task classification;
- updated triggered habits;
- remaining open questions.

## Integrity Rule

Do not reframe merely to make the task easier for the system. The revised framing must remain faithful to the user's goal.

## Loop Limit

If repeated reframing does not resolve ambiguity, emit `needs_user_clarification` and ask for the missing information.
