# Meta-Layer v1.0 Candidate Freeze Note

## Purpose

This document defines the Meta-Layer v1.0 Candidate baseline.

The goal of this freeze is not to claim the kernel is final. The goal is to create a stable contract baseline for reference-agent validation.

## A. v1.0 Candidate Scope

Meta-Layer v1.0 Candidate includes:

- canonical mother spec;
- constitution and policy priority;
- runtime pipeline;
- task object schema;
- handoff contract;
- decision gates;
- status flags;
- challenge loop;
- instruction hierarchy;
- kernel modes;
- H1-H11 habit module specs;
- shared policy layer;
- orchestration rules;
- kernel system/controller prompts;
- kernel output template;
- validation matrix and baseline file list.

The Macro-Financial Intelligence Agent is outside the kernel core. It is included only as a validation reference implementation.

## B. Completed Core Components

Completed v1.0 candidate components:

- `META_LAYER_MASTER_SPEC.md`: canonical mother spec.
- `meta-layer/CONSTITUTION.md`: constitutional rules and policy priority.
- `meta-layer/RUNTIME_PIPELINE.md`: runtime sequence and handoff flow.
- `meta-layer/TASK_OBJECT_SCHEMA.json`: task object contract schema.
- `meta-layer/HANDOFF_CONTRACT.md`: downstream handoff obligations.
- `meta-layer/DECISION_GATES.md`: Gate A-F handoff controls.
- `meta-layer/STATUS_FLAGS.md`: control flags and flag interactions.
- `meta-layer/CHALLENGE_LOOP.md`: challenge checks.
- `meta-layer/INSTRUCTION_HIERARCHY.md`: instruction priority.
- `meta-layer/KERNEL_MODES.md`: K1/K2/K3 modes.
- `meta-layer/habits/`: H1-H11 habit module drafts.
- `meta-layer/policies/`: memory, preference, confidence, verification, reframe, and escalation policies.
- `meta-layer/orchestration/`: pseudocode, trigger matrix, and module interaction rules.
- `meta-layer/prompts/KERNEL_SYSTEM_PROMPT.md`: kernel system prompt.
- `meta-layer/prompts/KERNEL_CONTROLLER_PROMPT.md`: controller prompt.
- `meta-layer/prompts/KERNEL_OUTPUT_TEMPLATE.json`: schema-compatible output template.

## C. Not Complete But Not Blocking v1.0 Candidate

These are intentionally deferred:

- full JSON Schema draft 2020-12 validation with a dedicated validator;
- exhaustive sample task objects for all modes and all handoff outcomes;
- concrete reference-agent validation runs;
- richer examples for return-to-kernel behavior;
- full macro-financial ingestion/reporting/export implementation;
- future agent adapters beyond notes;
- automated test harness for schema and semantic validation.

These do not block v1.0 Candidate because the contract is stable enough for reference-agent validation to begin.

## D. Frozen During v1.0 Candidate

The following should be treated as frozen unless a breaking-change review is explicitly opened:

- top-level task object field names;
- `risk_profile` field names and category semantics;
- `triggered_habits` H1-H11 identifiers;
- `structural_decomposition` field name and child fields;
- `required_checks` shape;
- `status_flags` allowed values;
- `downstream_recommendation` shape;
- decision gate names and blocking semantics;
- K1/K2/K3 mode names and high-level meaning;
- policy priority order;
- Macro-Financial Intelligence Agent's status as validation reference only.

## E. Breaking Changes

Treat a change as breaking if it:

- removes or renames a top-level task object field;
- changes `TASK_OBJECT_SCHEMA.json` in a way that invalidates current v1.0 candidate templates;
- changes `status_flags` meanings or allowed values;
- changes `downstream_recommendation.mode` meanings;
- weakens risk, verification, ethics, or uncertainty requirements;
- allows downstream agents to bypass Layer 0;
- converts the macro-financial reference agent into a primary trading recommendation agent;
- changes the canonical source-of-truth rule.

Breaking changes require explicit review and should update `validation/BREAKING_CHANGE_RULES.md`.

## Freeze Statement

Meta-Layer v1.0 Candidate is ready to serve as the baseline for reference-agent validation.

Further work should validate the kernel through examples and reference-agent runs before changing the contract.
