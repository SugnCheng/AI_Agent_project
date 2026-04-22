# Kernel Runtime Integration Readiness Note

## Purpose

This note summarizes the current readiness state for future ai-meta-kernel runtime integration from the macro-financial-intelligence-agent.

It is a developer-facing milestone note only. It does not implement kernel runtime handoff, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, production archive/export, or local canonical task object generation.

## Current Readiness Summary

The macro agent is ready for a future kernel runtime boundary design pass, but not ready for actual kernel invocation.

The current path is:

```text
fixture raw items
-> normalized items
-> deduped retained items
-> tagged items
-> triage decisions
-> schema-valid ingestion bundle
-> kernel input envelope
-> local kernel runtime boundary scaffold
-> static kernel response fixture validation
```

The path remains local, deterministic, fixture-only, and validation-first.

## Already In Place

### Evidence Preparation

- Local fixture raw item loading exists for `daily_us_core`.
- Deterministic fixture normalization, dedup, tagging, and triage scaffolds exist.
- Fixture bundle assembly produces an in-memory ingestion bundle.
- The fixture bundle is validated against the governed ingestion bundle schema.
- Bundle invariants are checked before kernel input envelope construction.

### Kernel Input Envelope

- `workflows/daily_us_core_fixture_kernel_input_envelope.py` builds a deterministic macro-side input envelope.
- `KERNEL_INPUT_ENVELOPE_OUTPUT_CONTRACT.md` defines the envelope output contract.
- The envelope explicitly remains evidence/context only.
- The envelope does not pre-fill kernel-owned conclusions.
- `canonical_task_object_generated` remains `false`.

### Runtime Boundary Scaffold

- `workflows/daily_us_core_kernel_runtime_boundary.py` defines the future invocation boundary.
- `invoke_kernel_runtime(envelope)` intentionally raises `NotImplementedError`.
- The boundary scaffold confirms:
  - `kernel_invocation_implemented == false`
  - `canonical_task_object_generated_locally == false`
  - `downstream_reporting_blocked == true`
- The scaffold can validate future kernel-produced response objects without invoking runtime.

### Kernel Response Validation

- `KERNEL_RESPONSE_VALIDATION_OUTPUT_CONTRACT.md` snapshots validation output fields and blocked / restricted / standard semantics.
- Static fixture kernel responses exist for:
  - standard handoff
  - restricted handoff
  - blocked handoff
- `validation/kernel_response_fixture_checks.py` confirms the three fixture responses classify as expected.
- Fixture responses validate against `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`.

## Locally Validated

The following local checks currently pass:

- `validation/run_all_local_checks.py`
- `validation/kernel_response_fixture_checks.py`

The current validation coverage confirms:

1. Existing macro config and ingestion examples remain valid.
2. Fixture bundle construction remains schema-valid.
3. Kernel input envelope construction does not impersonate a kernel task object.
4. The runtime boundary scaffold remains non-executing.
5. Static kernel response fixtures pass schema validation.
6. The validation helper correctly detects:
   - `standard`
   - `restricted`
   - `blocked`

## Interface Decisions Still Missing

Actual kernel runtime integration requires explicit decisions that are not yet made:

| Decision | Why it matters |
| --- | --- |
| Kernel invocation interface | The repo does not yet define whether kernel runtime will be called as a CLI, Python module, service boundary, file exchange, or another mechanism. |
| Envelope-to-kernel intake mapping | The kernel must decide how the macro envelope maps into `raw_request`, `source_context`, and P0/P1 intake fields. |
| Runtime ownership boundary | The macro agent must not construct canonical task objects, but a concrete interface must define where kernel-owned construction begins. |
| Response transport format | The handoff path must define whether the kernel returns JSON on stdout, writes a file, returns an object, or uses another interface. |
| Failure signaling | Runtime errors, validation failures, refused handoff, and clarification/reframe states need a stable transport-level convention. |
| Artifact persistence | The project has not decided whether envelopes and kernel responses should be stored as files during runtime. |
| Human review checkpoint | The exact point where an operator reviews restricted or blocked responses is not yet implemented. |
| Reporting unlock rule | Downstream reporting must define exactly how it consumes `standard_handoff` versus `restricted_handoff` once report composition exists. |

## Explicit Blockers Before Real Runtime Handoff

The following must remain blocked until a governed integration task addresses them:

- Actual ai-meta-kernel runtime invocation.
- Any macro-agent code path that generates a completed `TASK_OBJECT_SCHEMA.json` object.
- Report composition based only on envelope validation.
- Report composition based on a blocked kernel response.
- Unrestricted reporting from a restricted kernel response.
- Live fetching before the runtime boundary is intentionally updated.
- Scheduler execution.
- Archive/export automation.
- External service calls.
- CI integration.
- Package migration.
- Generic multi-profile runtime integration.

## Minimum Conditions For Future Implementation

A future implementation pass should not proceed unless it can preserve these conditions:

1. `ai-meta-kernel` owns P0-P10 of the runtime pipeline.
2. The macro agent submits evidence/context only.
3. The macro agent never fabricates kernel conclusions.
4. Returned kernel responses validate against `TASK_OBJECT_SCHEMA.json`.
5. Blocked and restricted states are enforced before downstream reporting.
6. The current fixture regression checks continue to pass.
7. Any new invocation interface is documented before broadening behavior.

## Recommended Next Phase

Implement a `Kernel Invocation Interface Decision Pass`.

That pass should choose the smallest acceptable integration interface for v0.1, such as:

- local CLI boundary;
- local Python function boundary;
- file-based envelope/response exchange.

It should not implement live fetching, scheduler runtime, report composition, or generic production automation.
