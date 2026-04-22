# Kernel Input Envelope Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for the `daily_us_core` fixture kernel input envelope helper.

It exists to prevent silent output drift when future ai-meta-kernel runtime integration is introduced. It does not define ai-meta-kernel runtime handoff, canonical kernel task object generation, live fetching, scheduler execution, report composition, CI, package migration, external service calls, archive/export automation, or production bundle processing.

## Scope

This contract applies only to:

- script: `workflows/daily_us_core_fixture_kernel_input_envelope.py`
- upstream bundle assembler: `workflows/daily_us_core_fixture_bundle_assembler.py`
- upstream bundle contract: `FIXTURE_BUNDLE_OUTPUT_CONTRACT.md`
- handoff planning source: `BUNDLE_TO_KERNEL_HANDOFF_PLAN.md`
- kernel handoff contract: `../ai-meta-kernel/meta-layer/HANDOFF_CONTRACT.md`
- kernel task object schema: `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`

It covers the compact JSON object printed by the fixture kernel input envelope helper and the optional full in-memory envelope printed with `--show-envelope`.

## Required Output Fields

| Field | Current value / type | Meaning | Fixed for current slice? | Future expansion rule |
| --- | --- | --- | --- | --- |
| `kernel_input_envelope_status` | `"ok"` | Indicates deterministic envelope construction and validation completed. | Yes | Additional status variants require explicit contract update. |
| `envelope_type` | `"macro_fixture_bundle_kernel_input"` | Identifies this as a macro-agent-side kernel input envelope. | Yes | Changing this value requires explicit contract update. |
| `envelope_version` | `"0.1.0"` | Local envelope contract version. | Yes | Version must change when envelope shape changes. |
| `source_project` | `"macro-financial-intelligence-agent"` | Identifies the downstream validation project preparing the evidence package. | Yes | Must not imply ownership of the kernel. |
| `profile_id` | `"daily_us_core"` | Governed profile inherited from the fixture bundle path. | Yes | Do not broaden beyond this profile in this helper without approval. |
| `run_mode` | `"daily_brief_run"` | Run mode inherited from the fixture bundle. | Yes | Must remain aligned with `scheduler/run_profiles.yaml`. |
| `report_target` | `"daily_brief"` | Report target inherited from the fixture bundle. | Yes | Must remain aligned with bundle context and reporting templates. |
| `regions` | `["US"]` | Regions inherited from the fixture bundle. | Yes | Additional regions require explicit profile/config approval. |
| `evidence_bundle_id` | `"fixture_daily_us_core_bundle_2026_04_23_v0_1"` | Bundle ID of the evidence artifact wrapped for kernel input. | Yes | Must match the upstream fixture bundle output contract. |
| `evidence_item_count` | `3` | Number of evidence bundle items included in the envelope. | Derived | Must match `len(evidence_bundle.items)` when full envelope is shown. |
| `kernel_owned_field_count` | `15` | Number of canonical kernel task object required fields listed as kernel-owned expectations. | Derived | Must match `TASK_OBJECT_SCHEMA.json` required field list used by this helper. |
| `envelope_validation` | `"ok"` | Local envelope validation passed, including non-impersonation of kernel task object. | Yes | Additional states require explicit contract update. |
| `canonical_task_object_generated` | `false` | Confirms the macro agent did not generate a completed `TASK_OBJECT_SCHEMA.json` object. | Yes | Must remain false until a separate governed kernel runtime integration exists. |
| `deferred_runtime_behavior` | list of strings | Explicit marker of runtime behaviors not implemented in this helper. | Yes | May shrink only when a behavior is intentionally implemented and documented. |

## Optional Output Field

| Field | Trigger | Meaning | Constraints |
| --- | --- | --- | --- |
| `kernel_input_envelope` | Present only with `--show-envelope` | Full in-memory macro-side input envelope for future Meta-Layer processing. | Must not be a canonical kernel task object; must not include completed kernel-owned conclusions. |

## Current Fixed Compact Output

The current fixture envelope slice fixes these compact output values:

```json
{
  "kernel_input_envelope_status": "ok",
  "envelope_type": "macro_fixture_bundle_kernel_input",
  "envelope_version": "0.1.0",
  "source_project": "macro-financial-intelligence-agent",
  "profile_id": "daily_us_core",
  "run_mode": "daily_brief_run",
  "report_target": "daily_brief",
  "regions": ["US"],
  "evidence_bundle_id": "fixture_daily_us_core_bundle_2026_04_23_v0_1",
  "evidence_item_count": 3,
  "kernel_owned_field_count": 15,
  "envelope_validation": "ok",
  "canonical_task_object_generated": false
}
```

## Full Envelope Contract

When `--show-envelope` is used, the helper may include `kernel_input_envelope`.

The full envelope must contain:

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

## Envelope Field Meanings

| Envelope field | Meaning |
| --- | --- |
| `envelope_type` | Local contract marker for macro fixture bundle input to the kernel. |
| `envelope_version` | Version of the macro-side envelope structure. |
| `source_project` | The downstream project preparing evidence/context. |
| `profile_id` | Source profile for the bundle evidence. |
| `run_mode` | Run mode inherited from the bundle. |
| `report_target` | Intended downstream report target as evidence context, not a kernel decision. |
| `regions` | Region scope inherited from the bundle. |
| `operator_intent` | Deterministic request for the Meta-Layer to frame the evidence for downstream research reporting, not trading advice. |
| `evidence_bundle` | Full schema-valid ingestion bundle from the fixture bundle assembler. |
| `evidence_context` | Evidence-only context derived from bundle status, counts, priorities, and source IDs. |
| `kernel_task_object_expectation` | Lists required kernel-owned output fields without filling them as conclusions. |
| `deferred_runtime_behavior` | Explicit list of runtime behaviors still absent. |

## Evidence Context Contract

`evidence_context` currently contains:

| Field | Meaning |
| --- | --- |
| `bundle_status.fixture_bundle_status` | Status copied from fixture bundle assembler. |
| `bundle_status.schema_validation` | Bundle schema validation status. |
| `bundle_status.invariant_validation` | Bundle invariant validation status. |
| `counts.item_count_raw` | Raw fixture item count. |
| `counts.item_count_after_dedup` | Retained dedup item count. |
| `counts.bundle_item_count` | Bundle item count. |
| `counts.source_count` | Distinct source count. |
| `priority_counts` | Preliminary triage priority distribution, not kernel risk. |
| `source_ids` | Distinct source IDs represented in the bundle. |
| `evidence_only_note` | Explicit warning that bundle fields are evidence/context only. |

## Kernel Task Object Expectation Contract

`kernel_task_object_expectation` currently contains:

| Field | Meaning |
| --- | --- |
| `kernel_owned` | Must be `true`; confirms the kernel owns canonical task object generation. |
| `handoff_contract_path` | Path to the upstream kernel handoff contract. |
| `task_object_schema_path` | Path to the upstream kernel task object schema. |
| `required_output_fields` | Required canonical task object fields expected from the kernel. |
| `macro_agent_must_not_prefill_as_conclusions` | Kernel-owned conclusion fields that macro agent must not fill. |
| `notes` | Boundary statement explaining that the envelope is input material only. |

## Kernel-Owned Fields That Must Not Be Pre-Filled

The envelope must not include these as top-level completed conclusions:

- `raw_request`
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

These fields belong to ai-meta-kernel.

## Validation Requirements

The fixture kernel input envelope output is valid only if:

1. the upstream fixture bundle assembler produces a valid evidence bundle;
2. required envelope fields are present;
3. `operator_intent` is non-empty;
4. `evidence_bundle` is present;
5. `kernel_task_object_expectation.kernel_owned` is `true`;
6. `kernel_task_object_expectation.required_output_fields` matches the helper's required kernel field list;
7. no kernel-owned conclusion field appears as a top-level completed envelope field;
8. the envelope does not contain all canonical task object required fields as top-level fields;
9. `deferred_runtime_behavior` includes `kernel_runtime_execution`;
10. `deferred_runtime_behavior` includes `ai_meta_kernel_runtime_handoff`;
11. `canonical_task_object_generated` remains `false`.

## Deferred Runtime Behaviors

The following behaviors must remain absent from this fixture kernel input envelope helper until explicitly implemented in a later governed task:

- `ai_meta_kernel_runtime_handoff`
- `kernel_runtime_execution`
- `canonical_task_object_generation`
- `live_fetching`
- `scheduler_execution`
- `production_bundle_assembly`
- `report_composition`
- `archive_export`
- `event_clustering`
- `operator_override_persistence`

These markers are intentionally present in `deferred_runtime_behavior` so future expansion cannot silently change the helper's scope.

## Drift Control Rules

- Do not rename compact output fields without updating this contract.
- Do not remove `canonical_task_object_generated` while the macro agent is not invoking kernel runtime.
- Do not set `canonical_task_object_generated` to `true` in this helper.
- Do not add completed canonical kernel task object fields to the top-level envelope.
- Do not convert `preliminary_priority` into kernel `risk_profile`.
- Do not convert bundle tags into `triggered_habits`.
- Do not convert evidence source metadata into verified kernel facts.
- Do not add report prose, final analysis, investment advice, downstream recommendations, or kernel handoff output to this helper.
- Do not implement ai-meta-kernel runtime handoff while leaving `kernel_runtime_execution` or `ai_meta_kernel_runtime_handoff` listed under `deferred_runtime_behavior`.
- Do not change this helper from `daily_us_core` to a generic kernel input envelope runner without a new contract pass.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_kernel_input_envelope.py'
```

To inspect the full in-memory envelope:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_kernel_input_envelope.py' --show-envelope
```
