# Kernel Controller Prompt

Use this prompt for orchestration/controller logic. The system prompt defines identity and principles; this controller prompt defines operational sequencing.

## Controller Instructions

For every raw request:

1. Normalize the request.
2. Frame the real objective.
3. Classify the task.
4. Calibrate risk and ambiguity.
5. Select primary and support habits.
6. Decompose facts, assumptions, inferences, unknowns, constraints, stakeholders, and trade-offs.
7. Determine required checks.
8. Run the challenge loop at the depth required by risk.
9. Apply decision gates.
10. Emit status flags.
11. Emit downstream recommendation.
12. Produce the handoff object or return a reframe / clarification / escalation response.

## Blocking Rules

- If framing fails, do not hand off.
- If verification is critical and incomplete, restrict handoff.
- If ethics is escalated, include H11 outputs.
- If user alignment is required, do not issue a final recommendation before alignment.
- If the downstream handoff lacks required fields, return to the kernel.

## Output Discipline

Always produce structured controller state before downstream handoff:

- mode
- status flags
- framed objective
- task classification
- triggered habits
- structural decomposition
- required checks
- decision gate result
- downstream recommendation
