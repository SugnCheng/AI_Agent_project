# Kernel File Exchange Adapter Fixtures

## Purpose

This folder contains the smallest static fixture set for future kernel-side file exchange adapter testing.

The fixtures are examples only. They do not implement runtime invocation, file readers, file writers, live fetching, scheduler runtime, report composition, CI, package migration, or external service calls.

## Fixture Set

| Fixture | Purpose |
| --- | --- |
| `envelopes/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.example.json` | Valid macro-produced evidence/context envelope for kernel intake testing. |
| `responses/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_response.example.json` | Minimal schema-valid example of a kernel-produced canonical task object response artifact. |
| `failures/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_failure.example.json` | Blocking kernel-side failure artifact example. |

## Guardrails

- The envelope fixture is not a canonical task object.
- The response fixture must stay valid against `../../meta-layer/TASK_OBJECT_SCHEMA.json`.
- The failure fixture must remain blocking.
- These fixtures must not be used to imply actual runtime handoff exists.

## Local Validation

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\kernel_file_exchange_fixture_checks.py'
```

Expected output:

```text
kernel-file-exchange-fixture-checks-ok
```
