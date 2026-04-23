# Kernel File Exchange Fixture Validation Output Contract

## Purpose

This document snapshots the current developer-facing output contract for:

```text
validation/kernel_file_exchange_fixture_checks.py
```

It fixes the helper's execution scope, success signal, failure behavior, and drift rules. It does not add runtime adapter code, file readers, file writers, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Scope

This contract applies only to static kernel-side file exchange fixture validation.

Current script:

```text
ai-meta-kernel/validation/kernel_file_exchange_fixture_checks.py
```

Current fixture root:

```text
ai-meta-kernel/examples/file-exchange/
```

Current fixtures:

- `envelopes/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.example.json`
- `responses/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_response.example.json`
- `failures/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_failure.example.json`

The helper is local, static, and `daily_us_core` scoped.

## Current Execution Scope

The helper currently performs these checks:

| Order | Fixture | Validation scope |
| --- | --- | --- |
| 1 | Envelope fixture | JSON parseability, required envelope fields, fixed `daily_us_core` metadata, non-empty `operator_intent`, no canonical task object top-level fields, expectation object shape. |
| 2 | Response fixture | JSON parseability, `TASK_OBJECT_SCHEMA.json` validation, `schema_version == "0.2.0"`, required top-level fields, at least one primary habit, valid downstream mode. |
| 3 | Failure fixture | JSON parseability, required failure fields, fixed `daily_us_core` metadata, allowed failure stage, `blocking == true`, no canonical task object top-level fields. |

The helper reads only committed fixture files and `meta-layer/TASK_OBJECT_SCHEMA.json`.

## Success Signal

When all checks pass, the helper must print exactly:

```text
kernel-file-exchange-fixture-checks-ok
```

This success signal means only that the current static fixture set still satisfies the current fixture validation contract.

It does not mean:

- kernel runtime invocation exists;
- file exchange adapter implementation exists;
- runtime artifacts are valid;
- downstream reporting is unlocked;
- live fetching or scheduler execution works.

## Expected Failure Behavior

If validation fails, the helper should:

1. raise an error with a specific failure reason;
2. exit non-zero;
3. not print `kernel-file-exchange-fixture-checks-ok`;
4. not modify any fixture or runtime artifact.

Typical failure categories:

- missing fixture file;
- invalid JSON;
- non-object JSON fixture;
- envelope missing required fields;
- envelope leaking canonical task object fields;
- response failing `TASK_OBJECT_SCHEMA.json`;
- response missing a primary habit;
- response using an invalid downstream handoff mode;
- failure fixture missing required fields;
- failure fixture using `blocking != true`;
- failure fixture using an unsupported `failure_stage`;
- missing `jsonschema` dependency.

## Drift Rules

The following changes require a governed pass before implementation:

- changing the helper path;
- changing fixture file paths;
- changing fixture file names;
- changing execution scope beyond the three current fixtures;
- changing the success signal;
- suppressing validation failure details;
- allowing warnings to pass silently where errors are currently required;
- changing envelope required fields;
- allowing envelope fixtures to include canonical task object fields;
- changing response schema validation target;
- changing response schema version expectations;
- changing downstream handoff mode expectations;
- changing failure artifact required fields;
- adding or removing allowed failure stages;
- allowing failure fixtures with `blocking == false`;
- adding runtime artifact validation;
- invoking adapter runtime code;
- generating response or failure artifacts;
- adding network, scheduler, reporting, CI, package migration, or external service behavior.

## Explicitly Absent Behaviors

The helper must not silently introduce:

- actual kernel-side adapter implementation;
- actual runtime invocation;
- file reader implementation for runtime exchange artifacts;
- response writer implementation;
- failure writer implementation;
- canonical task object generation from envelopes;
- runtime artifact validation;
- artifact polling;
- retry/backoff behavior;
- artifact cleanup automation;
- live fetching;
- scheduler runtime;
- report composition;
- CI integration;
- package migration;
- external service calls;
- generic multi-profile validation.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\kernel_file_exchange_fixture_checks.py'
```

Expected output:

```text
kernel-file-exchange-fixture-checks-ok
```

## Recommended Next Phase

Implement a `Kernel-Side Validation Wrapper Planning Pass`.

That pass should decide whether this helper should remain standalone or later be included in a broader `ai-meta-kernel` local validation wrapper. It should not add runtime adapter code.
