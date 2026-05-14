# Kernel Validation Baseline

## Purpose

This document refreshes the current kernel-side validation baseline for `ai-meta-kernel`.

It records the current standalone validation helpers, the implemented local validation wrapper, the wrapper failure-path helper, the first-slice adapter fixture validation surface, the runtime envelope reader output contract surface and helper, the runtime reader wrapper inclusion gate and reassessment, the writer-boundary planning and output contract surfaces, the intake-mapping planning and output contract surfaces, what success-path and failure-path validation mean, what they do not mean, and which runtime behaviors remain explicitly blocked.

This is a baseline note only. It does not add runtime code, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Documentation Index

For the current validation documentation map, see:

```text
docs/KERNEL_VALIDATION_DOCUMENTATION_INDEX.md
```

## Current Standalone Validation Helpers

The current kernel-side standalone helpers are:

| Helper | Responsibility | Success signal | Output contract |
| --- | --- | --- | --- |
| `validation/static_meta_layer_contract_checks.py` | Checks static core Meta-Layer contract artifacts, including master spec, runtime pipeline, handoff contract, and task object schema. | `kernel-static-meta-layer-contract-checks-ok` | `docs/KERNEL_STATIC_META_LAYER_CONTRACT_CHECK_OUTPUT_CONTRACT.md` |
| `validation/kernel_file_exchange_fixture_checks.py` | Checks the governed static `daily_us_core` file-exchange envelope, response, and failure fixtures. | `kernel-file-exchange-fixture-checks-ok` | `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_OUTPUT_CONTRACT.md` |
| `validation/kernel_file_exchange_adapter_scaffold_checks.py` | Checks the current file-exchange adapter scaffold boundary and confirms blocked placeholder functions remain fail-closed. | `kernel-file-exchange-adapter-scaffold-checks-ok` | `docs/KERNEL_FILE_EXCHANGE_ADAPTER_SCAFFOLD_CHECK_OUTPUT_CONTRACT.md` |
| `validation/kernel_runtime_envelope_reader_contract_checks.py` | Checks the future runtime envelope reader contract surface against the current scaffold reader and intake guardrails without implementing runtime reader behavior. | `kernel-runtime-envelope-reader-contract-checks-ok` | `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md` |

These helpers remain canonical standalone checks.

They may be run individually for focused debugging even though a wrapper now exists.

## Current First-Slice Adapter Fixture Validation Surface

The current first implementation slice validation surface is:

```text
validate_existing_daily_us_core_static_adapter_fixtures_and_fail_closed_scaffold_boundaries
```

It is governed by:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_VALIDATION_OUTPUT_CONTRACT.md
docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_HELPER_COVERAGE.md
```

The first-slice surface covers only:

- the existing `daily_us_core` static kernel input envelope fixture;
- the existing `daily_us_core` expected kernel response fixture;
- the existing `daily_us_core` expected blocking kernel failure fixture;
- the current fail-closed adapter scaffold boundaries.

Helper-free coverage decision:

```text
existing_helpers_fully_cover_first_slice_adapter_fixture_validation_contract
```

No new validation helper is currently needed for this slice.

Current coverage is provided by:

| Helper | First-slice coverage |
| --- | --- |
| `validation/kernel_file_exchange_fixture_checks.py` | Validates fixture existence, JSON object shape, governed `daily_us_core` values, response schema validity, blocking failure shape, and forbidden canonical task object leakage in envelope/failure fixtures. |
| `validation/kernel_file_exchange_adapter_scaffold_checks.py` | Exercises the scaffold against the static fixtures and confirms `prepare_kernel_intake`, `invoke_kernel_runtime`, `write_response_artifact`, and `write_failure_artifact` remain fail-closed. |

This surface is local-only and deterministic. It does not scan runtime artifact directories, discover live work, mutate fixtures, generate artifacts, or call runtime code.

## Current Runtime Envelope Reader Output Contract Surface

The current runtime envelope reader output contract is:

```text
future_reader_accepts_one_explicit_local_envelope_and_stops_before_intake_mapping
```

It is documented in:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md
```

It fits into the implementation sequence as step 1:

```text
Runtime envelope reader boundary
```

At the current stage, this document means:

- the future reader boundary is governed before implementation;
- the future reader may accept exactly one explicit local file path;
- the future reader output is one parsed and reader-validated `kernel_input_envelope` object;
- reader failure must be local, explicit, and fail-closed;
- reader output must stop before `kernel_intake_context` construction and intake mapping.

At the current stage, this document does not mean:

- runtime reader implementation exists;
- runtime directory scanning exists;
- queue discovery, polling, watcher, retry, or cleanup behavior exists;
- reader output can be treated as `kernel_intake_context`;
- reader output can unlock reporting;
- reader failure can write a blocking failure artifact;
- intake mapping, P0/P1 execution, P0-P10 invocation, response validation, response writing, or failure writing exists.

Current helper:

```text
validation/kernel_runtime_envelope_reader_contract_checks.py
```

Current helper success signal:

```text
kernel-runtime-envelope-reader-contract-checks-ok
```

The helper covers:

- successful read of the governed `daily_us_core` envelope fixture through `read_envelope_artifact`;
- successful validation of the parsed object through `validate_envelope_intake`;
- preservation of the original validated envelope object as the reader output;
- rejection of a missing path;
- rejection of a directory path;
- rejection of invalid JSON input;
- rejection of non-object JSON input;
- rejection of missing required envelope fields;
- rejection of a non-`kernel_input_envelope` artifact type;
- rejection of a failure artifact passed as envelope input;
- rejection of top-level canonical task object field leakage;
- confirmation that `prepare_kernel_intake` and `invoke_kernel_runtime` remain blocked with `NotImplementedError`.

The helper remains standalone. It is not currently included in `validation/run_all_kernel_local_checks.py`.

This standalone status is intentional for the current milestone: the wrapper remains the stable three-helper success-path baseline, while the reader helper separately covers the newly governed future reader boundary.

## Current Runtime Reader Wrapper Inclusion Gate

The current runtime reader wrapper inclusion gate decision is:

```text
runtime_reader_contract_helper_remains_standalone_outside_main_wrapper
```

It is documented in:

```text
docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_GATE.md
```

At the current stage, this means:

- `validation/kernel_runtime_envelope_reader_contract_checks.py` remains standalone;
- `validation/run_all_kernel_local_checks.py` remains unchanged;
- the wrapper's `CHECKS` list still contains only the three stable success-path helpers;
- the wrapper final success signal still means those three helpers passed in order;
- the reader helper may be run separately for focused reader-contract validation.

Before future wrapper inclusion, a governed pass must at minimum:

- re-review wrapper execution order;
- update the wrapper output contract;
- update this validation baseline;
- update the validation documentation index;
- confirm or update wrapper failure-path coverage for the expanded `CHECKS` list;
- preserve the reader helper's local-only, deterministic, no-mutation behavior;
- avoid introducing runtime reader implementation or runtime handoff behavior.

At the current stage, the inclusion gate does not mean:

- the reader helper is wrapper-included;
- the wrapper success signal includes reader-contract coverage;
- wrapper behavior has changed;
- runtime reader implementation is authorized;
- runtime artifact reads, writes, discovery, polling, retry, cleanup, CLI, or handoff are authorized.

## Current Runtime Reader Wrapper Inclusion Reassessment

The current TASK 114 reassessment decision is:

```text
runtime_reader_contract_helper_remains_standalone_outside_main_wrapper_for_next_milestone
```

It is documented in:

```text
docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_REASSESSMENT.md
```

At the current stage, this means:

- `validation/kernel_runtime_envelope_reader_contract_checks.py` remains standalone for the next milestone;
- `validation/run_all_kernel_local_checks.py` remains unchanged;
- the reader helper is still not part of the wrapper `CHECKS` list;
- `kernel-local-validation-checks-ok` does not include runtime reader helper coverage;
- `kernel-runtime-envelope-reader-contract-checks-ok` remains separately runnable for focused reader-contract validation.

If a future governed pass includes the reader helper in the main wrapper, the wrapper success signal meaning must be refreshed because `kernel-local-validation-checks-ok` would then also imply that the runtime reader contract helper passed. That change is intentionally not made in the current baseline.

Before any future inclusion, the project must complete governed updates to the wrapper output contract, wrapper failure-path coverage, this validation baseline, the validation documentation index, and the reader helper relationship notes.

At the current stage, the reassessment does not mean:

- the reader helper is wrapper-included;
- the wrapper success signal includes reader-contract coverage;
- wrapper behavior has changed;
- runtime reader implementation is authorized;
- runtime artifact discovery, polling, retry, cleanup, CLI, or runtime invocation is authorized.

## Current Writer-Boundary Planning And Output Contract Surface

The current writer-boundary planning decision is:

```text
plan_response_and_blocking_failure_writers_before_implementation
```

It is documented in:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_PLAN.md
```

The current writer-boundary output contract is:

```text
future_writers_must_validate_before_write_and_emit_exactly_one_terminal_artifact
```

It is documented in:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md
```

At the current stage, these documents mean:

- future response writer and blocking failure writer boundaries are planned before implementation;
- future response artifacts must be schema-validated before write;
- future blocking failure artifacts must remain `blocking == true`;
- one envelope invocation should produce exactly one terminal artifact: response or blocking failure;
- failure stages, artifact naming expectations, and pre-write validation order are governed before implementation.

At the current stage, these documents do not mean:

- response writing exists;
- failure writing exists;
- runtime handoff exists;
- P0-P10 runtime invocation exists;
- canonical task object generation from envelopes exists;
- writer code is authorized in the current baseline.

## Current Intake-Mapping Planning And Output Contract Surface

The current intake-mapping planning decision is:

```text
plan_envelope_to_kernel_owned_p0_p1_intake_before_implementation
```

It is documented in:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_PLAN.md
```

The current intake-mapping output contract is:

```text
future_mapping_may_emit_kernel_owned_intake_context_but_not_kernel_conclusions
```

It is documented in:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_OUTPUT_CONTRACT.md
```

At the current stage, these documents mean:

- future envelope-to-P0/P1 intake mapping is planned before implementation;
- validated envelope fields may flow into future intake only as evidence, metadata, request text, source context, expectation context, or deferred-behavior context;
- future mapping output may be a `kernel_intake_context`, not a canonical task object;
- canonical task object fields remain excluded from mapping output;
- the mapping boundary stops before P0/P1 execution and P0-P10 runtime invocation.

At the current stage, these documents do not mean:

- intake mapping code exists;
- kernel-owned P0/P1 intake object construction exists;
- P0/P1 execution exists;
- P0-P10 runtime invocation exists;
- canonical task object generation from envelope evidence exists;
- mapping output can unlock reporting;
- mapping output can be treated as a response artifact.

## Current Local Validation Wrapper

Implemented wrapper:

```text
validation/run_all_kernel_local_checks.py
```

Wrapper role:

- local-only validation orchestration;
- developer-facing command entrypoint;
- sequential execution of the three governed standalone helpers;
- child stdout and stderr preservation;
- stop-on-first-failure behavior.

The wrapper's implemented behavior is governed by:

```text
docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md
```

## Current Wrapper Failure-Path Helper

Implemented failure-path helper:

```text
validation/kernel_validation_wrapper_failure_path_checks.py
```

Failure-path helper role:

- local-only validation of wrapper failure-path behavior;
- developer-facing helper for wrapper process-control checks;
- imports `validation/run_all_kernel_local_checks.py` as a module;
- temporarily replaces the wrapper module's `CHECKS` list with controlled test entries;
- uses temporary helper scripts and a temporary marker file to verify stop-on-first-failure behavior;
- checks a deliberately missing helper path;
- verifies final wrapper success signal suppression on failure;
- does not mutate real validation helper files.

The failure-path helper's implemented behavior is governed by:

```text
docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_OUTPUT_CONTRACT.md
```

## Wrapper Execution Order

The wrapper runs exactly this order:

1. `validation/static_meta_layer_contract_checks.py`
2. `validation/kernel_file_exchange_fixture_checks.py`
3. `validation/kernel_file_exchange_adapter_scaffold_checks.py`

Reasoning:

- core Meta-Layer static contracts should pass before file-exchange fixtures are trusted;
- file-exchange fixtures should pass before adapter scaffold boundary checks rely on them;
- adapter scaffold fail-closed behavior should remain the final local check until runtime handoff is intentionally implemented.

## Local Command

Run the success-path wrapper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\run_all_kernel_local_checks.py'
```

Expected final success signal:

```text
kernel-local-validation-checks-ok
```

Run the wrapper failure-path helper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\kernel_validation_wrapper_failure_path_checks.py'
```

Expected final success signal:

```text
kernel-validation-wrapper-failure-path-checks-ok
```

Run the runtime envelope reader contract helper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\kernel_runtime_envelope_reader_contract_checks.py'
```

Expected final success signal:

```text
kernel-runtime-envelope-reader-contract-checks-ok
```

## What Success-Path Validation Means

A successful local wrapper run means:

- the core static Meta-Layer contract helper passed;
- the governed static file-exchange fixtures passed;
- the adapter scaffold boundary helper passed;
- the first-slice adapter fixture validation surface is covered by the existing fixture and scaffold helpers;
- the helper-free first-slice coverage decision remains valid for the current `daily_us_core` static fixture set;
- the writer-boundary plan and output contract are documented as future governed surfaces, not implemented behavior;
- the intake-mapping plan and output contract are documented as future governed surfaces, not implemented behavior;
- the runtime envelope reader output contract and standalone helper are documented as future governed surfaces, not implemented behavior;
- the runtime reader wrapper inclusion gate is documented and keeps the reader helper standalone;
- the TASK 114 runtime reader wrapper inclusion reassessment keeps the reader helper standalone for the next milestone;
- all three helpers passed in the governed order;
- the wrapper reached the final success signal.

It is the current success-path local validation baseline signal only.

It does not exercise wrapper child-failure paths, missing-helper paths, or the standalone runtime envelope reader contract helper. Those surfaces are covered separately by their focused helpers.

In particular, `kernel-local-validation-checks-ok` does not include `validation/kernel_runtime_envelope_reader_contract_checks.py` at the current milestone. The reader helper remains separately runnable and reports `kernel-runtime-envelope-reader-contract-checks-ok` when its standalone contract checks pass.

## What Failure-Path Validation Means

A successful wrapper failure-path helper run means:

- a temporary child helper exiting non-zero causes the wrapper to return that child exit code;
- the wrapper emits the expected failure message for a child non-zero exit;
- the wrapper stops before running a later helper after an earlier failure;
- the wrapper does not print `kernel-local-validation-checks-ok` after a child failure;
- a missing configured helper path causes the wrapper to return `1`;
- the wrapper emits the expected missing-helper failure message;
- the wrapper does not print `kernel-local-validation-checks-ok` after a missing helper;
- real validation helpers were not renamed, modified, deleted, or made to fail.

It is a local wrapper process-control validation signal only.

## What Local Validation Does Not Mean

A successful success-path wrapper run or failure-path helper run does not mean:

- kernel runtime exists;
- P0-P10 runtime execution exists;
- canonical task object generation exists;
- file-exchange runtime intake exists;
- runtime artifact reads or writes exist;
- response artifact writing exists;
- failure artifact writing exists;
- downstream macro reporting is unlocked;
- live fetching or scheduler runtime works;
- CI has run;
- production validation is complete;
- first-slice fixture validation has opened runtime handoff;
- writer-boundary planning has opened response or failure artifact writing;
- intake-mapping planning has opened P0/P1 intake construction or runtime invocation.
- runtime envelope reader planning has opened runtime artifact queue discovery, runtime directory scanning, or reader implementation.

## Explicitly Blocked Runtime Behaviors

The current validation baseline must not silently introduce:

- runtime adapter invocation;
- P0-P10 runtime invocation;
- canonical task object generation from envelopes;
- kernel intake preparation;
- response artifact writing;
- failure artifact writing;
- runtime artifact reads or writes;
- runtime artifact polling;
- retry/backoff behavior;
- artifact cleanup automation;
- live fetching;
- scheduler runtime;
- report composition;
- CI behavior;
- package migration;
- external service calls;
- generic multi-profile production validation;
- contract auto-repair.

The first-slice adapter fixture validation surface also must not silently introduce:

- additional fixture classes beyond envelope, expected response, and blocking failure;
- additional profiles beyond `daily_us_core`;
- generated runtime artifacts as committed fixtures;
- runtime reader discovery;
- response or failure writer behavior;
- CLI command behavior;
- macro-side production of kernel response artifacts.

The runtime envelope reader output contract surface also must not silently introduce:

- runtime reader implementation beyond the existing scaffold boundary;
- runtime directory scanning;
- artifact queue discovery;
- artifact polling or watcher behavior;
- retry/backoff behavior;
- cleanup automation;
- accepting more than one envelope per invocation;
- accepting response or failure artifacts as envelope input;
- treating reader output as `kernel_intake_context`;
- reader output unlocking downstream reporting;
- response or failure artifact writing from reader failures.

The runtime envelope reader contract helper also must not silently introduce:

- file mutation;
- generated runtime artifacts;
- temporary committed fixtures;
- runtime reader implementation;
- wrapper inclusion without a governed wrapper update;
- external dependencies beyond the Python standard library and the existing scaffold module.

The runtime reader wrapper inclusion gate also must not silently introduce:

- adding the reader helper to `validation/run_all_kernel_local_checks.py`;
- changing wrapper execution order;
- changing wrapper final success signal meaning;
- weakening wrapper stop-on-first-failure behavior;
- bypassing wrapper failure-path validation;
- treating standalone reader-helper success as wrapper success;
- treating wrapper inclusion as runtime reader implementation.

The TASK 114 runtime reader wrapper inclusion reassessment also must not silently introduce:

- adding the reader helper to `validation/run_all_kernel_local_checks.py`;
- changing the wrapper `CHECKS` list;
- changing the meaning of `kernel-local-validation-checks-ok`;
- treating `kernel-runtime-envelope-reader-contract-checks-ok` as part of wrapper success;
- weakening the existing wrapper inclusion gate;
- skipping governed wrapper output contract, failure-path, baseline, or index updates before any future inclusion.

The writer-boundary planning and output contract surfaces also must not silently introduce:

- response writer implementation;
- failure writer implementation;
- response artifact emission;
- failure artifact emission;
- writing both response and failure artifacts for one invocation;
- writing failure artifacts with `blocking == false`;
- writing response artifacts before schema and state validation;
- partial canonical task object content in failure artifacts;
- writer-side repair of invalid kernel outputs.

The intake-mapping planning and output contract surfaces also must not silently introduce:

- intake mapping implementation;
- kernel-owned P0/P1 intake object construction;
- P0/P1 execution;
- canonical task object fields in mapping output;
- mapping output treated as a response artifact;
- mapping output unlocking downstream reporting;
- mapping output bypassing P0-P10 runtime;
- direct population of kernel-owned reasoning fields from macro evidence.

## Changes Requiring A Governed Pass

The following changes require a governed pass before implementation:

- adding or removing standalone validation helpers;
- changing helper success signals;
- changing helper output contracts;
- changing wrapper execution order;
- changing wrapper final success signal;
- changing stop-on-first-failure behavior;
- suppressing, capturing, or transforming child stdout or stderr;
- adding wrapper-level dependencies;
- removing standalone helper support;
- changing the wrapper failure-path helper path;
- changing the wrapper failure-path helper success signal;
- changing the wrapper failure-path helper's monkeypatched `CHECKS` strategy;
- replacing temporary helper scripts with committed failing fixtures;
- mutating real validation helpers to simulate wrapper failure behavior;
- connecting validation to CI;
- broadening validation beyond the current standalone helper, wrapper, and wrapper failure-path helper baseline;
- changing fixture scope beyond the current governed static fixtures;
- changing the first-slice adapter fixture validation contract;
- changing the helper-free first-slice coverage decision;
- adding a new first-slice validation helper when existing helpers still cover the contract;
- changing the existing `daily_us_core` fixture set used by first-slice validation;
- changing the runtime envelope reader output contract decision;
- changing reader input from one explicit local file to directory discovery;
- allowing more than one envelope per reader invocation;
- allowing response or failure artifacts as reader input;
- allowing canonical task object fields in reader output;
- treating reader output as intake context, runtime result, response artifact, failure artifact, or reporting unlock;
- adding runtime envelope reader implementation beyond the existing scaffold boundary;
- changing the runtime envelope reader contract helper path;
- changing the runtime envelope reader contract helper success signal;
- adding the runtime envelope reader contract helper to the local wrapper;
- changing the runtime reader wrapper inclusion gate decision;
- changing the TASK 114 runtime reader wrapper inclusion reassessment decision;
- changing the wrapper inclusion prerequisites;
- changing whether `kernel-local-validation-checks-ok` includes runtime reader helper coverage;
- changing whether `kernel-runtime-envelope-reader-contract-checks-ok` remains separately runnable;
- changing the list of documents/contracts required for future wrapper inclusion;
- changing the writer-boundary planning decision;
- changing the writer-boundary output contract decision;
- changing response or failure artifact naming semantics;
- changing writer mutual exclusivity rules;
- changing writer pre-write validation order;
- adding response or failure writer implementation;
- changing the intake-mapping planning decision;
- changing the intake-mapping output contract decision;
- changing allowed envelope inputs for intake mapping;
- changing acceptable intake-context output fields;
- allowing canonical task object fields in mapping output;
- adding intake mapping implementation;
- adding P0/P1 execution or P0-P10 runtime invocation;
- adding runtime artifact validation;
- adding runtime adapter behavior;
- adding file mutation, cleanup, or auto-repair behavior.

## Current Baseline Status

The current baseline is:

```text
standalone_helpers_plus_local_wrapper_plus_wrapper_failure_path_helper_plus_first_slice_adapter_fixture_coverage_plus_runtime_reader_contract_and_standalone_helper_plus_wrapper_inclusion_gate_and_reassessment_plus_writer_boundary_contracts_plus_intake_mapping_contracts
```

The kernel now has a usable local success-path validation entrypoint, a focused wrapper failure-path helper, an explicit helper-free first-slice adapter fixture validation coverage decision, a governed runtime envelope reader output contract with a standalone local helper, a governed wrapper inclusion gate and TASK 114 reassessment that keep that helper outside the main wrapper for the next milestone, governed writer-boundary planning/output contracts, and governed intake-mapping planning/output contracts while preserving individually reviewable helper contracts.

## Recommended Next Phase

Implement a `Kernel-Side Validation Documentation Index Runtime Reader Inclusion Reassessment Refresh Pass`.

That pass should refresh the kernel validation documentation index so the TASK 114 runtime reader wrapper inclusion reassessment is easy to find while keeping wrapper changes, reader implementation code, intake mapping code, runtime invocation, response/failure writers, CLI, CI, scheduler behavior, live fetching, report composition, package migration, external service calls, and actual kernel runtime handoff out of scope.
