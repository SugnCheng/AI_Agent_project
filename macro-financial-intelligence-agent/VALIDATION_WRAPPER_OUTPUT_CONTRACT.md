# Validation Wrapper Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for `validation/run_all_local_checks.py`.

It fixes the current execution order, success signal, failure behavior, and drift rules for the unified local validation wrapper. It does not implement runtime behavior, live fetching, scheduler execution, report composition, CI, package migration, external service calls, archive/export automation, or ai-meta-kernel runtime handoff.

## Scope

This contract applies only to:

- script: `validation/run_all_local_checks.py`
- baseline note: `VALIDATION_BASELINE_SNAPSHOT.md`

The wrapper is local validation orchestration only. It must not replace the individual validation scripts and must not broaden their behavior.

## Current Execution Order

The wrapper currently runs these checks in this exact order:

| Order | Printed label | Script |
| --- | --- | --- |
| 1 | `running scaffold contract checks...` | `validation/scaffold_contract_checks.py` |
| 2 | `running dependency-backed contract checks...` | `validation/dependency_backed_contract_checks.py` |
| 3 | `running semantic contract checks...` | `validation/semantic_contract_checks.py` |
| 4 | `running kernel exchange fixture regression checks...` | `validation/kernel_exchange_fixture_regression_checks.py` |

The wrapper sets `PYTHONDONTWRITEBYTECODE=1` for child checks and runs each script from the repository root.

## Expected Success Signal

When all checks pass, the wrapper must print:

```text
all-local-validation-checks-ok
```

This is the current final success signal.

Individual child scripts may print their own structured summaries and success markers before the wrapper success signal. The wrapper success signal means only that each configured local validation script exited with status code `0`.

## Expected Failure Behavior

If any child check exits non-zero:

1. The wrapper prints:

```text
<label> failed with exit code <code>
```

2. The wrapper exits with that same non-zero status code.
3. Later checks are not run.
4. The wrapper must not print `all-local-validation-checks-ok`.

The wrapper does not catch, reinterpret, or repair child validation failures.

## Drift Rules

The following changes require a governed validation pass:

- changing the execution order;
- adding or removing a validation script;
- renaming printed labels;
- changing the final success signal;
- changing stop-on-first-failure behavior;
- allowing the wrapper to continue after a failed check;
- suppressing child script output;
- adding network, scheduler, report, runtime handoff, or artifact mutation behavior;
- making the wrapper a CI gate;
- broadening from `daily_us_core` fixture validation to generic multi-profile validation.

## Explicitly Absent Behaviors

The wrapper must not silently introduce:

- live fetching;
- open-web crawling;
- scheduler runtime;
- report composition;
- archive/export automation;
- ai-meta-kernel runtime invocation;
- kernel response generation;
- kernel failure artifact generation;
- canonical kernel task object generation inside the macro agent;
- artifact polling or watcher behavior;
- retry/backoff runtime behavior;
- runtime artifact mutation or deletion;
- external service calls;
- CI behavior;
- package layout migration;
- generic multi-profile production orchestration.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\validation\run_all_local_checks.py'
```
