# Kernel Static Meta-Layer Contract Check Output Contract

## Purpose

This document snapshots the current developer-facing output contract for:

```text
ai-meta-kernel/validation/static_meta_layer_contract_checks.py
```

It fixes the helper's execution scope, success signal, expected failure behavior, and drift rules. It does not add wrapper code, runtime behavior, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Scope

This contract applies only to the standalone static Meta-Layer contract helper:

```text
ai-meta-kernel/validation/static_meta_layer_contract_checks.py
```

The helper checks local static contract artifacts only.

Current artifact scope:

- `META_LAYER_MASTER_SPEC.md`
- `meta-layer/RUNTIME_PIPELINE.md`
- `meta-layer/HANDOFF_CONTRACT.md`
- `meta-layer/TASK_OBJECT_SCHEMA.json`

The helper is standalone. It is not part of a kernel validation wrapper yet.

## Current Execution Scope

The helper currently performs these checks:

| Order | Check | Expected behavior |
| --- | --- | --- |
| 1 | Required file presence | Confirms the four core contract artifacts exist at their canonical paths. |
| 2 | Schema JSON parseability | Confirms `TASK_OBJECT_SCHEMA.json` parses as a JSON object. |
| 3 | Schema draft metadata | Confirms `TASK_OBJECT_SCHEMA.json` declares draft 2020-12 metadata. |
| 4 | Canonical top-level fields | Confirms required and properties include canonical task object fields. |
| 5 | Canonical field names | Confirms key names such as `structural_decomposition`, `tradeoffs`, `risk_profile.overall_level`, `risk_profile.categories`, `downstream_recommendation.agent_type`, and `downstream_recommendation.output_format` remain present. |
| 6 | Handoff modes | Confirms `standard_handoff`, `restricted_handoff`, and `do_not_handoff` remain present in schema handoff mode enum. |
| 7 | Primary habit guardrail | Confirms `triggered_habits` still requires at least one primary habit. |
| 8 | Master spec sections | Confirms major canonical sections remain present in `META_LAYER_MASTER_SPEC.md`. |
| 9 | Runtime pipeline stages | Confirms `RUNTIME_PIPELINE.md` references P0 through P10. |
| 10 | Handoff contract terms | Confirms `HANDOFF_CONTRACT.md` references required handoff fields and handoff modes. |

This helper does not check full semantic equivalence between the master spec and split files.

## Success Signal

When all checks pass, the helper must print exactly:

```text
kernel-static-meta-layer-contract-checks-ok
```

This success signal means only that the current static core contract artifacts still satisfy the helper's minimum local contract checks.

It does not mean:

- runtime invocation exists;
- P0-P10 is executable;
- task object generation exists;
- wrapper orchestration exists;
- split files are semantically equivalent to the full master spec;
- downstream agent validation is complete.

## Expected Failure Behavior

If validation fails, the helper should:

1. raise an error with a specific failure reason;
2. exit non-zero;
3. not print `kernel-static-meta-layer-contract-checks-ok`;
4. not write, modify, delete, or repair any contract file.

Typical failure categories:

- missing required contract file;
- invalid `TASK_OBJECT_SCHEMA.json`;
- schema root is not a JSON object;
- missing canonical top-level required field;
- missing canonical top-level property;
- missing canonical field name;
- missing handoff mode;
- missing primary habit guardrail;
- missing master spec canonical section;
- missing P0-P10 runtime stage reference;
- missing handoff contract field or handoff mode reference.

## Current Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\static_meta_layer_contract_checks.py'
```

Expected output:

```text
kernel-static-meta-layer-contract-checks-ok
```

## Dependency Assumptions

The helper currently uses only Python standard library modules:

- `json`
- `pathlib`
- `typing`

It does not require `jsonschema`.

Adding non-standard dependencies requires a governed pass.

## Changes Requiring A Governed Pass

The following changes require a governed pass before implementation:

- changing the helper path;
- changing the success signal;
- changing execution order;
- adding or removing core artifact inputs;
- changing canonical file paths;
- changing canonical top-level field expectations;
- changing canonical field-name expectations;
- changing handoff mode expectations;
- changing master spec section expectations;
- changing runtime pipeline stage expectations;
- changing handoff contract term expectations;
- broadening from static contract checks to semantic equivalence checks;
- adding auto-repair behavior;
- adding task object generation;
- adding wrapper orchestration;
- connecting this helper to CI;
- adding runtime invocation;
- adding file-exchange artifact reads or writes;
- adding live fetching, scheduler runtime, report composition, package migration, or external service calls.

## Explicitly Absent Runtime Behaviors

The helper must not silently introduce:

- actual kernel runtime;
- P0-P10 execution;
- task object generation;
- file-exchange runtime artifact reads;
- file-exchange runtime artifact writes;
- response artifact writing;
- failure artifact writing;
- wrapper orchestration;
- CI behavior;
- live fetching;
- scheduler runtime;
- report composition;
- external service calls;
- package migration;
- contract auto-repair.

## Recommended Next Phase

Implement a `Kernel-Side Validation Wrapper Reassessment Pass`.

That pass should reassess wrapper readiness now that the kernel has three standalone validation helpers:

- `validation/static_meta_layer_contract_checks.py`
- `validation/kernel_file_exchange_fixture_checks.py`
- `validation/kernel_file_exchange_adapter_scaffold_checks.py`

It should still avoid wrapper code unless the governed decision explicitly changes from standalone to wrapper planning.
