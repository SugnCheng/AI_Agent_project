# Kernel Validation Documentation Index

## Purpose

This document is a developer-facing index for the current `ai-meta-kernel` validation documentation surface.

It points to the current standalone helper contracts, wrapper contracts, wrapper failure-path contract, baseline note, reassessment notes, and planning notes so developers can find the right validation document quickly.

This index does not add runtime behavior, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Start Here

| Document | Use it for |
| --- | --- |
| `docs/KERNEL_VALIDATION_BASELINE.md` | Current validation baseline: what exists now, what success-path validation means, what failure-path validation means, and what remains blocked. |
| `docs/KERNEL_VALIDATION_DOCUMENTATION_INDEX.md` | Navigation map for the validation docs. |

## Standalone Validation Helpers And Contracts

These documents describe the individually runnable validation helpers. Use them when debugging a specific validation surface before using the wrapper.

| Helper | Output contract | What it is for |
| --- | --- | --- |
| `validation/static_meta_layer_contract_checks.py` | `docs/KERNEL_STATIC_META_LAYER_CONTRACT_CHECK_OUTPUT_CONTRACT.md` | Static checks for canonical Meta-Layer contract artifacts, schema shape, required fields, handoff modes, and P0-P10 references. |
| `validation/kernel_file_exchange_fixture_checks.py` | `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_OUTPUT_CONTRACT.md` | Static validation for the governed `daily_us_core` file-exchange envelope, response, and failure fixtures. |
| `validation/kernel_file_exchange_adapter_scaffold_checks.py` | `docs/KERNEL_FILE_EXCHANGE_ADAPTER_SCAFFOLD_CHECK_OUTPUT_CONTRACT.md` | Scaffold boundary checks for fixture reads, response validation, and fail-closed adapter placeholders. |

## Wrapper Contracts

These documents describe the developer-facing local wrapper and its failure-path helper.

| Script | Contract | What it is for |
| --- | --- | --- |
| `validation/run_all_kernel_local_checks.py` | `docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md` | Current wrapper behavior: helper order, child output preservation, final success signal, stop-on-first-failure behavior, and blocked runtime behaviors. |
| `validation/kernel_validation_wrapper_failure_path_checks.py` | `docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_OUTPUT_CONTRACT.md` | Wrapper failure-path behavior: non-zero child exit, missing helper path, later-helper suppression, and final success signal suppression. |

## Baseline, Reassessment, And Planning Notes

These documents explain how the validation surface evolved and what decisions have already been bounded.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_VALIDATION_BASELINE.md` | Current milestone snapshot for standalone helpers, local wrapper, failure-path helper, success-path meaning, failure-path meaning, and governed drift rules. |
| `docs/KERNEL_VALIDATION_WRAPPER_REASSESSMENT.md` | Reassessment note for whether wrapper orchestration is justified from the current standalone helper surface. |
| `docs/KERNEL_VALIDATION_WRAPPER_PLAN.md` | Planning note for the local validation wrapper before implementation. |
| `docs/KERNEL_VALIDATION_WRAPPER_OUTPUT_CONTRACT.md` | Earlier wrapper output contract snapshot retained for wrapper-contract history. |
| `docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md` | Current implemented wrapper scaffold output contract. Prefer this over older wrapper contract notes when checking current behavior. |
| `docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_PLAN.md` | Planning note for the wrapper failure-path helper before implementation. |
| `docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_OUTPUT_CONTRACT.md` | Current implemented wrapper failure-path output contract. |
| `docs/KERNEL_STATIC_META_LAYER_CONTRACT_CHECK_PLAN.md` | Planning note for static Meta-Layer contract checks. |
| `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_PLAN.md` | Planning note for static file-exchange fixture checks. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_SCAFFOLD_PLAN.md` | Planning note for adapter scaffold boundary validation. |

## Practical Reading Order

For current local validation behavior:

1. Read `docs/KERNEL_VALIDATION_BASELINE.md`.
2. Read `docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md`.
3. Read `docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_OUTPUT_CONTRACT.md`.
4. Read the specific standalone helper contract only when debugging that helper.

For planning or governance review:

1. Read `docs/KERNEL_VALIDATION_BASELINE.md`.
2. Read the relevant plan or reassessment note.
3. Compare proposed changes against the related output contract drift rules.
4. Treat runtime behavior, CI, fetching, scheduler, reporting, package migration, and handoff execution as out of scope unless a new governed pass explicitly changes that boundary.

## Current Local Commands

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

## Explicit Non-Goals

This documentation index must not silently introduce:

- runtime adapter invocation;
- P0-P10 runtime invocation;
- canonical task object generation from envelopes;
- kernel intake preparation;
- response artifact writing;
- failure artifact writing;
- runtime artifact reads or writes;
- live fetching;
- scheduler runtime;
- report composition;
- CI behavior;
- package migration;
- external service calls;
- validation auto-repair;
- repository structure redesign.

## Recommended Next Phase

Implement a `Kernel-Side Validation Docs Cross-Link Pass`.

That pass should add minimal cross-links from the baseline and output contracts back to this index if useful, while still avoiding runtime code, CI, scheduler behavior, live fetching, report composition, package migration, and actual handoff execution.
