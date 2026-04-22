# Bundle-to-Kernel Handoff Plan

## Purpose

This document defines the next narrow, governed path for moving from the current fixture-driven ingestion bundle artifact into a kernel-ready handoff input.

It is a planning document only. It does not implement ai-meta-kernel runtime handoff, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, archive/export automation, or production bundle processing.

## Authority Boundary

`ai-meta-kernel` remains the upstream reasoning authority.

The macro agent may prepare evidence and context for the kernel. It must not generate the canonical kernel task object itself.

The canonical kernel task object is governed by:

- `../ai-meta-kernel/meta-layer/HANDOFF_CONTRACT.md`
- `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`

The bundle-to-kernel slice should therefore emit a kernel input envelope, not a completed `TASK_OBJECT_SCHEMA.json` object.

## Chosen Slice

The first bundle-to-kernel handoff slice should remain scoped to:

- input artifact: in-memory fixture bundle from `workflows/daily_us_core_fixture_bundle_assembler.py`
- input contract: `FIXTURE_BUNDLE_OUTPUT_CONTRACT.md`
- bundle schema: `bundles/schemas/INGESTION_BUNDLE.schema.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`
- output shape: a deterministic, local, developer-facing kernel input envelope

The envelope should be suitable for a later kernel invocation, but it should not execute kernel runtime or claim that kernel framing has already occurred.

## Why This Is the Safest Next Step

This is the safest next step after schema-valid bundle assembly because it introduces the boundary between evidence packaging and kernel reasoning without crossing it.

The current bundle artifact is already:

1. built from local fixture data only;
2. validated against `INGESTION_BUNDLE.schema.json`;
3. checked for count, dedup, source, and priority invariants;
4. explicit about deferred live/runtime/reporting behavior.

A kernel input envelope can now test whether bundle evidence can be represented clearly enough for the Meta-Layer to frame, classify, calibrate risk, trigger habits, plan verification, and produce a canonical handoff object later.

## Existing Components to Use

| Component | Existing file | Role in handoff slice |
| --- | --- | --- |
| Fixture bundle assembler | `workflows/daily_us_core_fixture_bundle_assembler.py` | Provides the schema-valid in-memory fixture ingestion bundle. |
| Fixture bundle output contract | `FIXTURE_BUNDLE_OUTPUT_CONTRACT.md` | Defines current bundle output fields and deferred behavior markers. |
| Ingestion bundle schema | `bundles/schemas/INGESTION_BUNDLE.schema.json` | Authoritative schema for evidence bundle field names. |
| Bundle assembly plan | `FIXTURE_BUNDLE_ASSEMBLY_PLAN.md` | Defines how triaged fixture items enter the bundle. |
| Kernel handoff contract | `../ai-meta-kernel/meta-layer/HANDOFF_CONTRACT.md` | Defines what the kernel must eventually provide to downstream agents. |
| Kernel task object schema | `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json` | Defines the canonical task object that only the kernel should emit. |

## Proposed Kernel Input Envelope

The first implementation should use a small explicit envelope such as:

```json
{
  "envelope_type": "macro_fixture_bundle_kernel_input",
  "envelope_version": "0.1.0",
  "source_project": "macro-financial-intelligence-agent",
  "profile_id": "daily_us_core",
  "run_mode": "daily_brief_run",
  "report_target": "daily_brief",
  "regions": ["US"],
  "operator_intent": "Ask the Meta-Layer to frame this validated macro-financial evidence bundle for downstream research reporting.",
  "evidence_bundle": {},
  "evidence_context": {},
  "kernel_task_object_expectation": {},
  "deferred_runtime_behavior": []
}
```

This envelope is a macro-agent-side input package. It is not a replacement for the kernel task object schema.

## Bundle Content to Kernel Input Mapping

| Kernel input envelope field | Source | First-slice rule |
| --- | --- | --- |
| `envelope_type` | Fixed local contract | Use `macro_fixture_bundle_kernel_input`. |
| `envelope_version` | Fixed local contract | Use `0.1.0`. |
| `source_project` | Fixed local contract | Use `macro-financial-intelligence-agent`. |
| `profile_id` | Fixture bundle summary / profile | Copy `daily_us_core`. |
| `run_mode` | `bundle_metadata.run_mode` | Copy `daily_brief_run`. |
| `report_target` | `bundle_context.report_target` | Copy `daily_brief`. |
| `regions` | `bundle_metadata.regions` | Copy `["US"]`. |
| `operator_intent` | Local deterministic text | State that the kernel should frame the evidence for research reporting, not produce trading advice. |
| `evidence_bundle` | Full in-memory ingestion bundle | Embed or reference the schema-valid bundle artifact. First slice can embed in-memory output. |
| `evidence_context.bundle_status` | Fixture bundle compact output | Include `fixture_bundle_status`, `schema_validation`, and `invariant_validation`. |
| `evidence_context.counts` | Bundle metadata and compact summary | Include `item_count_raw`, `item_count_after_dedup`, `bundle_item_count`, and `source_count`. |
| `evidence_context.priority_counts` | Fixture bundle compact output | Copy priority counts as preliminary triage distribution only. |
| `evidence_context.source_ids` | Bundle item `source_id` values | Include distinct sorted source IDs for kernel framing context. |
| `kernel_task_object_expectation` | Kernel schema/contract | State expected kernel output fields without filling them locally. |
| `deferred_runtime_behavior` | Fixture bundle output | Preserve deferred markers and add `kernel_runtime_execution`. |

## Evidence-Only Fields

These fields may be passed as evidence or context only:

- `bundle_metadata`
- `bundle_context`
- item `title`
- item `source_id`
- item `authority_tier`
- item `official_status`
- item `published_at`
- item `retrieved_at`
- item `source_url`
- item `canonical_url`
- item `content_type`
- item `topic_tags`
- item `market_tags`
- item `risk_tags`
- item `preliminary_priority`
- item `summary_seed`
- item `raw_excerpt`
- item `dedup_group_id`
- item `priority_weight`
- item `trust_score`
- item `notes`

These are evidence package fields. They must not be treated as kernel conclusions.

## Fields That Must Not Pretend To Be Kernel Conclusions

The macro agent must not fill or imply final values for these canonical kernel fields:

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

The macro agent may provide suggestions or source context, but the kernel must own the final values.

Specific guardrails:

- `preliminary_priority` is a rule-based triage signal, not a kernel risk rating.
- `risk_tags` are descriptive evidence tags, not `risk_profile.categories`.
- `authority_tier` and `trust_score` are source metadata, not proof that claims are true.
- `summary_seed` is not a report summary.
- `operator_notes` are context, not kernel instructions that override the constitution.
- `watchlist_topics` are monitoring context, not triggered habits.

## Alignment With Kernel Handoff Contract

The kernel handoff contract requires the kernel to eventually emit:

- `raw_request`
- `framed_objective`
- `task_classification`
- `risk_profile`
- `triggered_habits`
- `structural_decomposition`
- `required_checks`
- `status_flags`
- `downstream_recommendation`

The bundle-to-kernel envelope should support these fields by providing clean evidence and context, but should not precompute them.

Expected kernel framing direction for the first slice:

| Kernel field | Envelope support | Kernel-owned decision |
| --- | --- | --- |
| `raw_request` | `operator_intent` plus evidence bundle context | Kernel converts this into canonical `raw_request.text` and `received_at`. |
| `framed_objective` | Bundle purpose and report target | Kernel decides surface request, core goal, scope, non-goals, and success criteria. |
| `task_classification` | Evidence bundle type and desired reporting path | Kernel classifies, likely as `analysis` with information/reporting support, but macro agent must not fix this. |
| `risk_profile` | Financial, time-sensitive, source-dependent context | Kernel calibrates overall level and categories. |
| `triggered_habits` | Source claims, inference needs, report output, ethics context | Kernel selects H1/H2/H7/H11 or other habits as appropriate. |
| `structural_decomposition` | Bundle item facts and explicit fixture assumptions | Kernel separates facts, assumptions, inferences, unknowns, constraints, stakeholders, and tradeoffs. |
| `required_checks` | Schema validation, source verification gaps, uncertainty markers | Kernel decides mandatory verification/challenge/alignment checks. |
| `status_flags` | Fixture-only and no-live-fetching limits | Kernel decides whether output is ready, restricted, or needs verification. |
| `downstream_recommendation` | Desired downstream report path | Kernel decides handoff mode, agent type, output format, rationale, and restrictions. |

## Alignment With `TASK_OBJECT_SCHEMA.json`

The first handoff slice should not emit a complete object conforming to `TASK_OBJECT_SCHEMA.json`.

Instead, it should make it easy for a future kernel runtime call to produce a valid task object with:

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

The first implementation should include a `kernel_task_object_expectation` section that lists these required output fields and states that they are kernel-owned.

## Minimal Validation Expectations

The future envelope should be considered valid only if:

1. the source bundle first validates against `INGESTION_BUNDLE.schema.json`;
2. the source bundle's fixture invariants pass;
3. the envelope does not include canonical kernel-owned fields as completed conclusions;
4. `evidence_bundle` is present or an explicit bundle reference is present;
5. `operator_intent` is present and non-empty;
6. deferred behavior markers include `ai_meta_kernel_runtime_handoff` or `kernel_runtime_execution`;
7. the envelope preserves authority order by naming `ai-meta-kernel` as the reasoning owner.

## In-Scope Next Steps

The next implementation pass should do only the following:

1. Add a fixture-only bundle-to-kernel input envelope helper.
2. Reuse the current fixture bundle assembler.
3. Build a deterministic envelope from the in-memory fixture bundle.
4. Include evidence context and kernel-owned field expectations.
5. Validate that the envelope does not pretend to be a kernel task object.
6. Print compact developer-facing summary output.
7. Optionally print the full envelope with an explicit flag.
8. Keep ai-meta-kernel runtime invocation absent.

## Explicitly Deferred

The bundle-to-kernel handoff slice must not implement:

- ai-meta-kernel runtime handoff;
- kernel task object generation inside the macro agent;
- live fetching;
- scheduler execution;
- production bundle assembly;
- report composition;
- archive/export automation;
- event clustering;
- operator override persistence;
- external service calls;
- CI;
- package migration.

## Guardrails

- Do not modify `../ai-meta-kernel/meta-layer/HANDOFF_CONTRACT.md`.
- Do not modify `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`.
- Do not invent a competing kernel task object schema inside the macro agent.
- Do not rename canonical kernel fields.
- Do not convert bundle `preliminary_priority` into kernel `risk_profile`.
- Do not convert bundle tags into `triggered_habits`.
- Do not treat fixture source metadata as verified truth.
- Do not produce downstream recommendations before kernel processing.
- Do not report final conclusions, investment advice, or policy interpretation in the handoff envelope.

## Recommended Next Phase

Implement `TASK 37 - Fixture Bundle-to-Kernel Input Envelope Scaffold`.

That pass should introduce the smallest local helper that converts the current in-memory fixture ingestion bundle into a deterministic kernel input envelope, without invoking ai-meta-kernel runtime, generating a kernel task object, composing reports, fetching live sources, or calling external services.
