# H5: Solving Problems

## Purpose

Support obstacle removal, feasibility analysis, troubleshooting, and path design under constraints.

## Trigger Conditions

- The task includes a goal-obstacle gap.
- The user needs a feasible path or troubleshooting.
- Constraints determine possible solutions.

## Required Inputs

- goal state
- current state
- obstacles
- constraints
- available resources

## Internal Checks

1. Define the goal-obstacle gap.
2. Separate hard and soft constraints.
3. Identify feasible pathways.
4. Check whether the true issue is bad framing.
5. Remove obviously infeasible options.

## Expected Outputs

- `problem_gap_statement`
- `constraint_map`
- `feasible_pathways`
- `blockers_to_remove`
- `next_step_sequence`

## Failure Modes

- Jumping to solutions before constraints.
- Treating preferences as hard constraints.
- Ignoring upstream framing problems.

## Escalation Rules

- If the solution requires a new process or product, add H6.
- If execution involves multiple people, add H10.
