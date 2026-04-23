# Kernel Runtime Integration Readiness Note

## Purpose

This note refreshes the current readiness state for future `ai-meta-kernel` runtime integration from `macro-financial-intelligence-agent`.

It is a developer-facing milestone note only. It does not implement kernel runtime handoff, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, production archive/export, artifact polling, or local canonical task object generation.

## Current Readiness Summary

The macro agent is now ready for a kernel-side file exchange integration planning pass, but it is still not ready for actual kernel runtime invocation.

The current governed local path is:

```text
fixture raw items
-> normalized items
-> deduped retained items
-> tagged items
-> triage decisions
-> schema-valid ingestion bundle
-> kernel input envelope
-> file-based envelope artifact writer
-> file-based response / failure artifact reader
-> kernel response fixture validation
-> kernel exchange fixture regression validation
-> unified local validation wrapper
```

The path remains local, deterministic, fixture-driven, and validation-first. It prepares the macro side of the boundary; it does not invoke `ai-meta-kernel`.

## Already In Place

### Evidence Preparation

- Local fixture raw item loading exists for `daily_us_core`.
- Deterministic fixture normalization, dedup, tagging, and triage scaffolds exist.
- Fixture bundle assembly produces an in-memory ingestion bundle.
- The fixture bundle is validated against `bundles/schemas/INGESTION_BUNDLE.schema.json`.
- Bundle invariants are checked before kernel input envelope construction.

### Kernel Input Envelope

- `workflows/daily_us_core_fixture_kernel_input_envelope.py` builds a deterministic macro-side input envelope.
- `KERNEL_INPUT_ENVELOPE_OUTPUT_CONTRACT.md` defines the envelope output contract.
- The envelope remains evidence/context only.
- The envelope does not pre-fill kernel-owned conclusions.
- The macro agent does not generate a completed canonical kernel task object.

### File-Based Exchange Contract

- `FILE_BASED_KERNEL_EXCHANGE_CONTRACT.md` defines the v0.1 file-based envelope / response exchange.
- Runtime exchange directories are prepared under `runtime/kernel_exchange/`.
- Generated runtime exchange JSON artifacts are ignored by default.
- The selected v0.1 interface is file-based exchange, not CLI invocation, Python module invocation, service invocation, or direct in-process kernel calls.
- The macro agent may write kernel input envelope artifacts.
- The macro agent must not produce kernel response artifacts.

### Envelope Artifact Writer

- `workflows/daily_us_core_write_kernel_envelope_artifact.py` writes a local kernel input envelope artifact for `daily_us_core`.
- `FILE_BASED_KERNEL_EXCHANGE_OUTPUT_CONTRACT.md` snapshots its compact output fields, artifact naming semantics, and generated-artifact drift rules.
- The writer does not invoke `ai-meta-kernel`.
- The writer does not read or write kernel response artifacts.
- The writer does not compose reports.

### Response / Failure Artifact Reader

- `workflows/daily_us_core_read_kernel_response_artifact.py` reads explicit or derived local response / failure artifacts.
- `FILE_BASED_KERNEL_RESPONSE_READ_OUTPUT_CONTRACT.md` snapshots compact decision fields, artifact match semantics, blocked / restricted / standard drift rules, and downstream unlock guardrails.
- The reader can classify:
  - standard response;
  - restricted response;
  - blocked response;
  - failure artifact;
  - missing artifact;
  - ambiguous response/failure pair.
- Failure artifacts are always blocking in v0.1.
- Missing or ambiguous artifacts are always blocking.

### Kernel Response Validation

- `KERNEL_RESPONSE_VALIDATION_OUTPUT_CONTRACT.md` snapshots future kernel response validation fields and blocked / restricted / standard semantics.
- Static fixture kernel responses exist for:
  - standard handoff;
  - restricted handoff;
  - blocked handoff.
- Static failure fixture exists for the blocking file-exchange failure path.
- Kernel response fixtures validate against `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`.

### Local Regression Validation

- `validation/kernel_response_fixture_checks.py` validates the three static kernel response fixtures.
- `validation/kernel_exchange_fixture_regression_checks.py` validates the file-based exchange response/failure branches:
  - standard response -> `standard`;
  - restricted response -> `restricted`;
  - blocked response -> `blocked`;
  - failure artifact -> `blocked`.
- `validation/run_all_local_checks.py` now includes the kernel exchange fixture regression helper.
- `VALIDATION_BASELINE_SNAPSHOT.md` fixes the current unified validation layer scope.
- `VALIDATION_WRAPPER_OUTPUT_CONTRACT.md` fixes wrapper execution order, success signal, failure behavior, and drift rules.

## Locally Validated

The current local validation baseline is:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\validation\run_all_local_checks.py'
```

Expected final output:

```text
all-local-validation-checks-ok
```

When this passes, it confirms:

1. scaffold contract checks pass;
2. dependency-backed YAML/schema checks pass;
3. semantic config and bundle checks pass;
4. file-based kernel exchange fixture regression checks pass;
5. standard / restricted / blocked / failure exchange branches classify as expected.

It does not confirm that live acquisition, scheduler execution, report composition, or actual kernel runtime handoff exists.

## Ready Areas

The following areas are ready as local governed scaffolds or contracts:

| Area | Current readiness |
| --- | --- |
| Evidence packaging | Fixture-driven path can produce deterministic triaged items and a schema-valid ingestion bundle. |
| Kernel input preparation | Macro agent can produce an evidence/context envelope without pretending to be the kernel. |
| File exchange interface choice | v0.1 uses file-based envelope / response exchange. |
| Envelope artifact writing | Macro agent can write a governed local envelope artifact. |
| Response artifact reading | Macro agent can read and classify governed response artifacts. |
| Failure artifact handling | Macro agent can read a static blocking failure artifact and keep reporting blocked. |
| Response state semantics | Standard, restricted, and blocked states are locally validated with fixtures. |
| Unified validation | Local wrapper now includes kernel exchange regression validation. |

## Still Blocked

The following must remain blocked until governed implementation work explicitly addresses them:

- Actual `ai-meta-kernel` runtime invocation.
- Kernel-side file reader implementation.
- Kernel-side response artifact writer implementation.
- Kernel-side failure artifact writer implementation.
- Any macro-agent code path that generates a completed `TASK_OBJECT_SCHEMA.json` object.
- Report composition based only on envelope validation.
- Report composition from a missing, ambiguous, failed, or blocked kernel exchange result.
- Unrestricted reporting from a restricted kernel response.
- Live fetching.
- Scheduler execution.
- Archive/export automation.
- External service calls.
- CI integration.
- Package migration.
- Generic multi-profile runtime exchange.

## Missing Decisions / Implementations Before Actual Invocation

The file-based interface choice is decided, but real runtime invocation still needs these concrete implementation decisions:

| Missing item | Required decision or implementation |
| --- | --- |
| Kernel-side envelope intake | Define how `ai-meta-kernel` reads the file-based envelope and maps it into P0/P1 intake without weakening `RUNTIME_PIPELINE.md`. |
| Kernel-owned task object production | Implement kernel-owned construction of the canonical task object; macro agent must not synthesize it. |
| Kernel response artifact writer | Define and implement where the kernel writes schema-valid response artifacts. |
| Kernel failure artifact writer | Define and implement how invocation, parse, schema, or state failures write blocking failure artifacts. |
| Response/failure ownership | Confirm whether the kernel itself or a thin boundary wrapper owns failure artifact creation. |
| Operator review checkpoint | Define how restricted and blocked responses are surfaced for human review before reporting. |
| Reporting unlock interface | Define how future report composition consumes `standard` versus `restricted` decisions without bypassing review hooks. |
| Runtime artifact retention | Decide whether generated artifacts remain local-only, are archived, or are promoted to fixtures through governed review. |

## Minimum Conditions For Future Runtime Handoff

A future implementation pass should not proceed unless it preserves these conditions:

1. `ai-meta-kernel` owns P0-P10 of the runtime pipeline.
2. The macro agent submits evidence/context only.
3. The macro agent never fabricates kernel conclusions.
4. The macro agent never writes kernel response artifacts.
5. Returned kernel responses validate against `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`.
6. Failure artifacts block downstream reporting.
7. Blocked responses block downstream reporting.
8. Restricted responses preserve restrictions and do not silently promote to standard.
9. Human review checkpoints remain intact.
10. `validation/run_all_local_checks.py` continues to pass after integration changes.

## Recommended Next Phase

Implement a `Kernel-Side File Exchange Adapter Planning Pass`.

That pass should define the smallest governed `ai-meta-kernel`-side file reader / response writer boundary for v0.1. It should still avoid live fetching, scheduler runtime, report composition, CI, package migration, external service calls, and broad production automation.
