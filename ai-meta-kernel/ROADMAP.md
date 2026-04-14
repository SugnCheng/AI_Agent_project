# Roadmap

This roadmap separates the core kernel from the reference agent. The Meta-Layer is the first priority; downstream agents exist to test transferability.

## Phase 0: Skeleton and Review Draft

Status: in progress.

Goals:

- Create repository structure for the kernel, downstream agents, examples, validation, and future agent notes.
- Draft the first set of reviewable specification documents.
- Define the task object schema and kernel prompt contract.
- Define the macro-financial intelligence agent only as a validation reference.

Exit criteria:

- All planned files exist.
- Priority documents have useful first drafts.
- `TASK_OBJECT_SCHEMA.json` is valid JSON.
- Validation hooks map reference-agent behaviors to kernel capabilities.

## Phase 1: Meta-Layer Contract Stabilization

Primary owner: Meta-Layer.

Goals:

- Refine `CONSTITUTION.md`, `RUNTIME_PIPELINE.md`, `HANDOFF_CONTRACT.md`, and policy documents.
- Formalize instruction hierarchy and kernel modes.
- Define how habits are triggered and how conflicts are resolved.
- Define confidence, uncertainty, and escalation rules.
- Add examples for multiple task types beyond finance.

Exit criteria:

- Kernel can produce a stable task object and handoff object for at least five distinct request classes.
- Risk, verification, and ethics gates are auditable.
- Challenge loop rules are testable against failure cases.

## Phase 2: Reference Agent Validation

Primary owner: Macro-Financial Intelligence Agent as a test harness.

Goals:

- Use the macro-financial reference agent to test ingestion, synthesis, verification, reporting, and archival handoff.
- Validate high-risk information workflows without generating direct trading advice.
- Exercise source-quality evaluation, jurisdiction tagging, policy-risk classification, evidence freshness, and uncertainty reporting.

Exit criteria:

- Each reference-agent workflow maps back to specific kernel capabilities.
- The validation matrix identifies pass/fail criteria for framing, risk calibration, verification, challenge loop, and handoff quality.
- Reports include evidence boundaries and confidence notes.

## Phase 3: Transferability Checks

Primary owner: Meta-Layer.

Goals:

- Add future downstream agent specs for learning, writing, project, and investment-adjacent research agents.
- Confirm the kernel does not overfit to macro-financial research.
- Refactor common adapter requirements.

Exit criteria:

- At least three non-financial future-agent scenarios can consume the same kernel task object.
- New agent specs require no change to the core constitution unless a real kernel gap is discovered.

## Phase 4: Implementation Planning

Primary owner: TBD.

Goals:

- Decide whether the kernel should be implemented as prompt-only, library, service, workflow runner, or hybrid.
- Define storage, logging, testing, and review workflows.
- Create minimal executable prototypes only after the specification is coherent.

Exit criteria:

- Implementation architecture is selected with documented tradeoffs.
- Test cases are traceable to validation documents.
- No implementation bypasses the kernel's upper-level risk, verification, or ethics rules.
