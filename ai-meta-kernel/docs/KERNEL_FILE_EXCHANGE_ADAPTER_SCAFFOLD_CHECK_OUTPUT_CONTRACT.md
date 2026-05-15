# Kernel File Exchange Adapter Scaffold Check Output Contract

## Purpose

This document snapshots the current developer-facing output contract for:

```text
ai-meta-kernel/validation/kernel_file_exchange_adapter_scaffold_checks.py
```

It fixes the helper's execution scope, success signal, expected failure behavior, and drift rules. It does not add runtime code, wrapper orchestration, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Scope

This contract applies only to the local scaffold fixture check helper:

```text
ai-meta-kernel/validation/kernel_file_exchange_adapter_scaffold_checks.py
```

The helper exercises the current scaffold module:

```text
ai-meta-kernel/file_exchange_adapter_scaffold.py
```

It uses only the committed static fixtures under:

```text
ai-meta-kernel/examples/file-exchange/
```

This helper is standalone. It is not part of a kernel validation wrapper yet.

## Current Execution Scope

The helper currently performs these checks:

| Order | Check | Expected behavior |
| --- | --- | --- |
| 1 | Envelope boundary | `read_envelope_artifact` reads the governed envelope fixture and `validate_envelope_intake` accepts it. |
| 2 | Response validation boundary | `read_json_object` reads the governed response fixture and `validate_kernel_response` accepts it against `meta-layer/TASK_OBJECT_SCHEMA.json`. |
| 3 | Kernel intake mapping boundary | `prepare_kernel_intake` returns a context-only `kernel_intake_context` and stops before runtime. |
| 4 | Kernel runtime candidate boundary | `invoke_kernel_runtime` returns a candidate-only pre-writer object from validated intake. |
| 5 | Response writer placeholder | `write_response_artifact` remains fail-closed with `NotImplementedError`. |
| 6 | Failure writer placeholder | `write_failure_artifact` remains fail-closed with `NotImplementedError`. |

The helper reads:

- `examples/file-exchange/envelopes/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.example.json`
- `examples/file-exchange/responses/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_response.example.json`
- `examples/file-exchange/failures/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_failure.example.json`
- `meta-layer/TASK_OBJECT_SCHEMA.json` indirectly through `validate_kernel_response`

## Success Signal

When all checks pass, the helper must print exactly:

```text
kernel-file-exchange-adapter-scaffold-checks-ok
```

This success signal means only that the current scaffold boundary still matches the committed fixture expectations and blocked-boundary expectations.

It does not mean:

- actual kernel runtime invocation exists;
- P0-P10 is executable;
- context-only kernel intake mapping exists, but P0/P1 execution does not;
- response artifacts can be written;
- failure artifacts can be written;
- downstream reporting is unlocked;
- a kernel validation wrapper exists.

## Expected Failure Behavior

If validation fails, the helper should:

1. raise an error with a specific failure reason;
2. exit non-zero;
3. not print `kernel-file-exchange-adapter-scaffold-checks-ok`;
4. not write, modify, delete, or discover runtime artifacts.

Typical failure categories:

- missing envelope fixture;
- invalid envelope JSON;
- envelope failing `validate_envelope_intake`;
- missing response fixture;
- invalid response JSON;
- response failing `validate_kernel_response`;
- missing failure fixture;
- writer boundary unexpectedly returning instead of raising `NotImplementedError`;
- runtime invocation returning anything other than candidate-only pre-writer output;
- missing `jsonschema` dependency when response schema validation is required;
- scaffold module import failure.

## Current Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\kernel_file_exchange_adapter_scaffold_checks.py'
```

Expected output:

```text
kernel-file-exchange-adapter-scaffold-checks-ok
```

## Changes Requiring A Governed Pass

The following changes require a governed pass before implementation:

- changing the helper path;
- changing the success signal;
- changing execution order;
- adding or removing fixture inputs;
- changing fixture file names or paths;
- broadening the check beyond the committed static fixture set;
- suppressing failure details;
- allowing warnings to pass where errors are currently required;
- allowing writer blocked boundaries to return successfully;
- broadening runtime invocation beyond candidate-only pre-writer output;
- adding response artifact writing;
- adding failure artifact writing;
- broadening kernel intake mapping beyond context-only output;
- adding real P0-P10 runtime invocation;
- adding runtime artifact directory reads;
- adding artifact polling, cleanup, or retry behavior;
- adding wrapper orchestration;
- connecting this helper to CI;
- adding live fetching, scheduler runtime, report composition, package migration, or external service calls.

## Explicitly Absent Runtime Behaviors

The helper must not silently introduce:

- actual kernel-side adapter runtime;
- actual runtime handoff;
- P0-P10 invocation;
- canonical task object generation from envelope;
- response artifact writing;
- failure artifact writing;
- runtime artifact scanning;
- artifact polling;
- retry/backoff behavior;
- artifact cleanup automation;
- validation wrapper orchestration;
- live fetching;
- scheduler runtime;
- report composition;
- external service calls;
- package migration;
- CI integration.

## Recommended Next Phase

Implement a `Kernel-Side Validation Wrapper Reassessment Pass` only if the kernel now has enough standalone validation helpers to justify wrapper planning.

Otherwise, keep this helper standalone until a governed wrapper inclusion pass explicitly defines wrapper path, scope, execution order, final success signal, dependency assumptions, and blocked behaviors.
