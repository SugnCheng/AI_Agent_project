# Cross-Project Integration Status Snapshot

## Purpose

This note snapshots the current integration readiness between:

- `ai-meta-kernel/`
- `macro-financial-intelligence-agent/`

It is intentionally located at the repository root because it describes the boundary between two parallel projects. It does not make either project the owner of the other.

This document does not add runtime behavior, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Current Status

Current cross-project status:

```text
file_based_exchange_contract_aligned_but_runtime_handoff_not_implemented
```

The macro side can prepare and write governed local kernel input envelope artifacts. The kernel side has validated contracts, fixture checks, adapter scaffold checks, wrapper checks, and wrapper failure-path checks. The actual kernel-side file reader, P0-P10 runtime invocation, response writer, and failure writer remain unimplemented.

## Macro-Side Readiness

The macro-financial intelligence agent is ready as a governed local scaffold for file-based kernel exchange planning.

Already in place:

- whitelist-first governance and source discipline;
- configured run profiles and source registry;
- ingestion bundle schema and governed static examples;
- fixture-driven raw loading, normalization, dedup, tagging, triage, and bundle assembly path;
- deterministic kernel input envelope helper;
- file-based envelope artifact writer;
- response / failure artifact reader scaffold;
- static standard, restricted, blocked, and failure fixture validation;
- unified local validation wrapper including kernel exchange fixture regression checks.

Still absent on the macro side:

- live acquisition;
- scheduler execution;
- production preprocessing logic;
- production bundle assembly;
- report composition;
- archive/export automation;
- actual `ai-meta-kernel` invocation;
- macro-side generation of canonical kernel task objects, which must remain blocked.

## Kernel-Side Readiness

The kernel side is ready as a governed validation and contract baseline, but not yet as a runtime file-exchange executor.

Already in place:

- static Meta-Layer contract checks;
- static file-exchange fixture checks;
- file-exchange adapter scaffold boundary checks;
- local validation wrapper for success-path helper orchestration;
- wrapper failure-path helper for child failure, missing helper, stop-on-first-failure, and success-signal suppression behavior;
- validation documentation index;
- refreshed validation baseline;
- kernel-side file exchange adapter contract snapshot.

Still absent on the kernel side:

- actual envelope artifact reader implementation;
- envelope-to-P0/P1 intake implementation;
- P0-P10 runtime execution implementation;
- canonical task object production from envelope evidence;
- response artifact writer implementation;
- blocking failure artifact writer implementation;
- CLI or invocation boundary;
- runtime artifact validation beyond static fixtures and scaffold checks.

## File-Based Exchange Alignment

The two projects are aligned on the v0.1 file-based exchange boundary:

| Boundary | Current alignment |
| --- | --- |
| Interface style | File-based envelope / response exchange. |
| Macro input role | Macro agent prepares evidence/context as a kernel input envelope. |
| Kernel reasoning role | Kernel owns P0-P10 framing, classification, verification, challenge, status, and handoff. |
| Canonical task object ownership | Kernel owns `TASK_OBJECT_SCHEMA.json` response production. |
| Response artifact ownership | Kernel writes response artifacts; macro agent must not. |
| Failure artifact semantics | Failures are blocking and must not unlock reporting. |
| Runtime artifact locations | Macro-side runtime exchange directories are defined under `macro-financial-intelligence-agent/runtime/kernel_exchange/`. |
| Fixture distinction | Static fixtures are reviewable examples; runtime artifacts are generated local material and not committed by default. |
| Restricted / blocked semantics | Macro side validates standard, restricted, blocked, and failure states before downstream unlock. |

## Validation And Governance Surfaces

Current macro-side validation surfaces:

- `macro-financial-intelligence-agent/validation/run_all_local_checks.py`
- `macro-financial-intelligence-agent/validation/scaffold_contract_checks.py`
- `macro-financial-intelligence-agent/validation/dependency_backed_contract_checks.py`
- `macro-financial-intelligence-agent/validation/semantic_contract_checks.py`
- `macro-financial-intelligence-agent/validation/kernel_response_fixture_checks.py`
- `macro-financial-intelligence-agent/validation/kernel_exchange_fixture_regression_checks.py`
- macro output contracts for dry-run, fixture pipeline, kernel input envelope, response validation, file exchange write, and response read behavior.

Current kernel-side validation surfaces:

- `ai-meta-kernel/validation/run_all_kernel_local_checks.py`
- `ai-meta-kernel/validation/static_meta_layer_contract_checks.py`
- `ai-meta-kernel/validation/kernel_file_exchange_fixture_checks.py`
- `ai-meta-kernel/validation/kernel_file_exchange_adapter_scaffold_checks.py`
- `ai-meta-kernel/validation/kernel_validation_wrapper_failure_path_checks.py`
- `ai-meta-kernel/docs/KERNEL_VALIDATION_BASELINE.md`
- `ai-meta-kernel/docs/KERNEL_VALIDATION_DOCUMENTATION_INDEX.md`
- kernel output contracts for standalone helpers, wrapper behavior, wrapper failure paths, and adapter scaffold behavior.

## Remaining Runtime Handoff Gaps

Before actual runtime handoff, the following gaps remain:

1. Define and implement kernel-side envelope artifact reading.
2. Define and implement envelope intake validation without weakening canonical kernel contracts.
3. Map envelope evidence/context into kernel-owned P0/P1 intake.
4. Implement or expose the kernel-owned P0-P10 runtime path.
5. Produce canonical task objects only inside `ai-meta-kernel`.
6. Validate kernel-produced responses against `ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`.
7. Write kernel response artifacts only after schema validation succeeds.
8. Write blocking kernel failure artifacts when invocation, parsing, schema validation, or response state validation fails.
9. Preserve restricted and blocked response semantics before macro-side reporting.
10. Define the operator review checkpoint for restricted and blocked outputs.

## Explicitly Blocked Behaviors

The current cross-project baseline must not silently introduce:

- live fetching;
- uncontrolled open-web crawling;
- scheduler runtime;
- report composition;
- archive/export automation;
- CI behavior;
- package migration;
- external service calls;
- macro-side canonical kernel task object generation;
- macro-side kernel response artifact writing;
- kernel contract renaming or schema drift;
- hidden runtime handoff;
- automatic source governance changes;
- unrestricted reporting from restricted, blocked, failed, missing, or ambiguous kernel exchange states.

## Recommended Next Phase

Implement a `Kernel-Side File Exchange Adapter Fixture Planning Pass`.

That pass should define the smallest static kernel-side envelope fixture and expected response/failure fixture strategy for testing the kernel adapter boundary before any runtime file reader, response writer, failure writer, CLI, CI, scheduler behavior, live fetching, report composition, package migration, or actual handoff execution is added.
