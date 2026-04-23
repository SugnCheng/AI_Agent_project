# Kernel Static Meta-Layer Contract Check Plan

## Purpose

This document decides whether `ai-meta-kernel` should add a standalone static contract check for core Meta-Layer artifacts before any kernel validation wrapper implementation is considered.

It is a planning document only. It does not add validation code, wrapper code, runtime handoff, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or changes to kernel contracts.

## Path Note

The canonical master spec currently exists at:

```text
ai-meta-kernel/META_LAYER_MASTER_SPEC.md
```

The path below was checked and is not present:

```text
ai-meta-kernel/meta-layer/META_LAYER_MASTER_SPEC.md
```

Any future static contract check should validate the actual canonical path unless the repository intentionally moves the master spec through a governed restructuring pass.

## Current Context

Current kernel-side standalone validation helpers cover file-exchange fixtures and adapter scaffold boundaries:

- `validation/kernel_file_exchange_fixture_checks.py`
- `validation/kernel_file_exchange_adapter_scaffold_checks.py`

The wrapper reassessment concluded that wrapper implementation should wait because there is not yet a core Meta-Layer baseline validation helper.

Relevant governance note:

- `docs/KERNEL_VALIDATION_WRAPPER_REASSESSMENT.md`

## Governed Decision

Add a standalone static Meta-Layer contract check in a future implementation pass.

Do not add a wrapper yet.

Reasoning:

- The core Meta-Layer artifacts are the upstream authority for file-exchange, adapter, and downstream validation work.
- Current validation coverage checks file-exchange fixtures and scaffold behavior, but not the canonical kernel baseline itself.
- A wrapper should not be introduced until core contracts have their own standalone check.
- A standalone check is the smallest step that improves kernel validation coverage without adding orchestration overhead.

## Core Artifacts To Cover

The first static contract check should cover:

| Artifact | Role |
| --- | --- |
| `META_LAYER_MASTER_SPEC.md` | Canonical mother specification and alignment authority. |
| `meta-layer/RUNTIME_PIPELINE.md` | Pipeline stage definitions and handoff sequence. |
| `meta-layer/HANDOFF_CONTRACT.md` | Required handoff fields, field semantics, modes, and downstream obligations. |
| `meta-layer/TASK_OBJECT_SCHEMA.json` | Machine-checkable task object contract. |

Optional later additions may include:

- `meta-layer/STATUS_FLAGS.md`
- `meta-layer/DECISION_GATES.md`
- `meta-layer/CHALLENGE_LOOP.md`
- `meta-layer/prompts/KERNEL_OUTPUT_TEMPLATE.json`

These should remain out of the first helper unless a governed pass expands scope.

## Minimum Validation Scope

The first standalone helper should validate only static, local contract integrity.

Minimum checks:

1. Required files exist at their canonical paths.
2. `TASK_OBJECT_SCHEMA.json` parses as JSON.
3. `TASK_OBJECT_SCHEMA.json` declares draft 2020-12 schema metadata.
4. `TASK_OBJECT_SCHEMA.json` requires the canonical top-level fields:
   - `schema_version`
   - `task_id`
   - `raw_request`
   - `kernel_stage`
   - `framed_objective`
   - `task_classification`
   - `risk_profile`
   - `triggered_habits`
   - `structural_decomposition`
   - `required_checks`
   - `status_flags`
   - `verification_plan`
   - `challenge_loop`
   - `downstream_recommendation`
   - `handoff`
5. `TASK_OBJECT_SCHEMA.json` preserves canonical field names:
   - `structural_decomposition`
   - `tradeoffs`
   - `risk_profile.overall_level`
   - `risk_profile.categories`
   - `downstream_recommendation.agent_type`
   - `downstream_recommendation.output_format`
6. `TASK_OBJECT_SCHEMA.json` requires at least one primary triggered habit.
7. `TASK_OBJECT_SCHEMA.json` includes the handoff modes:
   - `standard_handoff`
   - `restricted_handoff`
   - `do_not_handoff`
8. `META_LAYER_MASTER_SPEC.md` contains the major canonical sections:
   - Identity
   - Core Mission
   - Runtime Pipeline
   - Task Object Contract
   - Downstream Handoff Contract
   - Canonical Alignment Rule
9. `RUNTIME_PIPELINE.md` references P0 through P10.
10. `HANDOFF_CONTRACT.md` references the required handoff fields and handoff modes.

## Out Of Scope For First Helper

The first static helper should not:

- semantically prove full equivalence between master spec and split files;
- rewrite or repair files;
- generate task objects;
- invoke kernel runtime;
- read or write file-exchange runtime artifacts;
- validate macro-agent contracts;
- run existing file-exchange fixture helpers;
- introduce wrapper orchestration;
- connect to CI;
- fetch external sources;
- call external services.

## Standalone Status

The future helper should remain standalone at first.

Suggested future path:

```text
ai-meta-kernel/validation/static_meta_layer_contract_checks.py
```

Suggested success signal:

```text
kernel-static-meta-layer-contract-checks-ok
```

Wrapper inclusion should be reconsidered only after this helper exists and its output contract is stable.

## Future Output Contract Requirement

After the helper is implemented, a separate governed pass should create an output contract snapshot defining:

- execution scope;
- success signal;
- expected failure behavior;
- dependency assumptions;
- drift rules;
- explicit non-goals.

## Main Constraints

The helper must preserve:

- master-spec authority;
- canonical field naming;
- JSON schema validity;
- split-file responsibility boundaries;
- local-only validation behavior;
- no runtime or wrapper behavior.

## Recommended Next Phase

Implement a `Kernel-Side Static Meta-Layer Contract Check Helper Pass`.

That pass should add only the standalone static helper described here. It should not add wrapper code, runtime invocation, artifact reads/writes, CI, or downstream agent validation.
