# Kernel File Exchange Adapter Scaffold Output Contract

## Purpose

This document snapshots the current developer-facing behavior contract for:

```text
ai-meta-kernel/file_exchange_adapter_scaffold.py
```

It fixes the scaffold function boundary, fail-closed behavior, placeholder rules, local-only guarantees, and drift rules. It does not implement actual kernel runtime handoff, file exchange runtime, response/failure artifact writing, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or changes to kernel contracts.

## Scope

This contract applies only to the current local scaffold module:

```text
ai-meta-kernel/file_exchange_adapter_scaffold.py
```

It must remain compatible with:

- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_SCAFFOLD_PLAN.md`
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_CONTRACT.md`
- `meta-layer/TASK_OBJECT_SCHEMA.json`

If this snapshot conflicts with canonical kernel contracts, the canonical kernel contracts win.

## Current Scaffold Function Boundary

The current scaffold exposes the following function boundary:

| Function | Current behavior | Output / failure behavior |
| --- | --- | --- |
| `read_envelope_artifact(path)` | Reads exactly one local JSON file and returns a JSON object. | Returns `dict`; raises `KernelFileExchangeAdapterScaffoldError` for missing file, invalid JSON, or non-object JSON. |
| `validate_envelope_intake(envelope)` | Validates required envelope fields and guardrails. | Returns the validated envelope `dict`; raises `KernelFileExchangeAdapterScaffoldError` on shape, required-field, type, or leaked canonical-field failure. |
| `prepare_kernel_intake(envelope)` | Validates envelope intake, then returns a context-only `kernel_intake_context`. | Stops before P0/P1 and runtime invocation. |
| `invoke_kernel_runtime(kernel_intake)` | Verifies object-like input, then blocks. | Raises `NotImplementedError`. |
| `validate_kernel_response(task_object)` | Validates a caller-provided object against `meta-layer/TASK_OBJECT_SCHEMA.json`. | Returns the validated `task_object`; raises `KernelFileExchangeAdapterScaffoldError` on missing `jsonschema`, invalid object shape, missing schema, invalid schema JSON, or schema validation failure. |
| `read_json_object(path, label)` | Reads a local JSON object for scaffold validation boundaries. | Returns `dict`; raises `KernelFileExchangeAdapterScaffoldError` for missing file, invalid JSON, or non-object JSON. |
| `write_response_artifact(task_object, destination)` | Validates a provided response object, then blocks before writing. | Raises `NotImplementedError`; must not write files. |
| `write_failure_artifact(failure, destination)` | Verifies object-like failure input, then blocks before writing. | Raises `NotImplementedError`; must not write files. |

The scaffold also defines:

```text
KernelFileExchangeAdapterScaffoldError
```

This error is used for scaffold boundary validation failures that are not intentionally blocked placeholder behavior.

## Current Envelope Guardrails

`validate_envelope_intake(envelope)` currently requires:

- `envelope_type`
- `envelope_version`
- `source_project`
- `profile_id`
- `run_mode`
- `report_target`
- `regions`
- `operator_intent`
- `evidence_bundle`
- `evidence_context`
- `kernel_task_object_expectation`
- `deferred_runtime_behavior`

Current enforced guardrails:

1. `envelope_type` must equal `kernel_input_envelope`.
2. `regions` must be a non-empty list.
3. `operator_intent` must be a non-empty string.
4. `evidence_bundle` must be an object.
5. `evidence_context` must be an object.
6. `kernel_task_object_expectation` must be an object.
7. `deferred_runtime_behavior` must be a list.
8. Failure artifacts are rejected as envelope intake.
9. Canonical task object top-level fields are rejected if they appear in the envelope.

The current rejected canonical top-level fields are:

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

## Current Blocked Runtime Behavior

The following functions are intentionally blocked:

- `invoke_kernel_runtime(kernel_intake)`
- `write_response_artifact(task_object, destination)`
- `write_failure_artifact(failure, destination)`

Current rule:

```text
Runtime invocation and writer functions must raise NotImplementedError until a governed implementation pass explicitly replaces the placeholder behavior.
```

They must not:

- return fabricated success;
- invoke P0-P10;
- generate canonical task objects from envelopes;
- write response artifacts;
- write failure artifacts;
- unlock downstream reporting;
- mutate envelope, response, failure, or runtime artifacts.

## Current Local-Only Guarantees

The scaffold is local-only.

It may:

- read a caller-provided local JSON file path;
- validate JSON object shape;
- validate envelope guardrails;
- validate a caller-provided kernel response object against `TASK_OBJECT_SCHEMA.json`.

It must not:

- discover artifacts automatically;
- poll runtime directories;
- perform cleanup;
- perform retry/backoff;
- call external services;
- fetch web sources;
- run scheduler behavior;
- compose reports;
- generate macro-agent outputs;
- modify kernel contracts;
- modify macro-agent contracts;
- write runtime artifacts.

## Current Response Validation Boundary

`validate_kernel_response(task_object)` validates only an object supplied by the caller.

It does not:

- create a task object;
- repair missing fields;
- infer kernel conclusions;
- run the kernel runtime pipeline;
- write response artifacts;
- downgrade schema failures into warnings.

It uses:

```text
meta-layer/TASK_OBJECT_SCHEMA.json
```

as the schema target.

If `jsonschema` is unavailable, validation fails closed with `KernelFileExchangeAdapterScaffoldError`.

## Changes Requiring A Governed Pass

The following changes require a governed pass before implementation:

- changing the scaffold module path;
- renaming scaffold functions;
- changing function return types;
- allowing more than one envelope artifact per invocation;
- changing required envelope fields;
- changing canonical field leak detection;
- allowing envelope intake to include canonical task object fields;
- broadening `prepare_kernel_intake` beyond context-only `kernel_intake_context`;
- replacing `invoke_kernel_runtime` `NotImplementedError` with real runtime invocation;
- allowing response artifact writing;
- allowing failure artifact writing;
- changing response validation target away from `meta-layer/TASK_OBJECT_SCHEMA.json`;
- suppressing schema validation errors;
- allowing runtime artifact polling or discovery;
- adding retry/backoff or cleanup behavior;
- adding CLI behavior;
- adding validation wrapper inclusion;
- adding package layout changes;
- adding CI;
- adding live fetching;
- adding scheduler runtime;
- adding report composition;
- broadening from local scaffold boundaries to production multi-profile exchange.

## Explicitly Absent Runtime Behaviors

The following remain explicitly absent:

- actual kernel-side adapter runtime;
- actual P0-P10 invocation;
- intake mapping beyond context-only `kernel_intake_context`;
- canonical task object generation from envelope;
- response artifact writing;
- failure artifact writing;
- file exchange CLI;
- runtime artifact directory scanning;
- artifact polling;
- artifact cleanup automation;
- retry/backoff behavior;
- broader validation wrapper orchestration;
- live fetching;
- scheduler runtime;
- report composition;
- external service calls;
- package migration;
- CI integration.

## Basic Local Checks

The current scaffold can be checked locally without invoking runtime behavior.

Syntax check:

```powershell
python -B -c "import ast, pathlib; ast.parse(pathlib.Path('ai-meta-kernel/file_exchange_adapter_scaffold.py').read_text(encoding='utf-8')); print('adapter-scaffold-syntax-ok')"
```

Envelope guardrail check against the governed fixture:

```powershell
python -B -c "import importlib.util, pathlib; p=pathlib.Path('ai-meta-kernel/file_exchange_adapter_scaffold.py'); spec=importlib.util.spec_from_file_location('adapter_scaffold', p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); envelope=m.read_envelope_artifact('ai-meta-kernel/examples/file-exchange/envelopes/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.example.json'); m.validate_envelope_intake(envelope); print('adapter-scaffold-envelope-guardrails-ok')"
```

These checks do not imply runtime handoff exists.

## Recommended Next Phase

Implement a `Kernel-Side File Exchange Adapter Scaffold Fixture Check Pass`.

That pass should add a small local validation helper for this scaffold boundary only if needed. It should not add wrapper orchestration, runtime invocation, response/failure artifact writing, or canonical task object generation.
