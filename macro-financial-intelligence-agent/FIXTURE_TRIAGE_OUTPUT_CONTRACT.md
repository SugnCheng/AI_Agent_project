# Fixture Triage Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for the `daily_us_core` fixture triage helper.

It exists to prevent silent output drift as preprocessing expands. It does not define live fetching, scheduler execution, production triage, advanced negative scoring, watchlist matching, event-chain continuity detection, operator override persistence, bundle assembly, report composition, CI, package migration, external service calls, or ai-meta-kernel runtime handoff.

## Scope

This contract applies only to:

- script: `workflows/daily_us_core_fixture_triage.py`
- upstream fixture tagger: `workflows/daily_us_core_fixture_tagger.py`
- upstream fixture deduper: `workflows/daily_us_core_fixture_deduper.py`
- upstream fixture file: `fixtures/daily_us_core_raw_items.fixture.json`
- rule authority: `preprocessing/triage/TRIAGE_RULES.md`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`

It covers the JSON object printed by the fixture triage helper.

## Required Output Fields

| Field | Current value / type | Meaning | Fixed for current slice? | Future expansion rule |
| --- | --- | --- | --- | --- |
| `fixture_triage_status` | `"ok"` | Indicates deterministic fixture triage completed and validation checks passed. | Yes | Additional status variants require explicit contract update. |
| `profile_id` | `"daily_us_core"` | Governed profile inherited from the fixture tagger path. | Yes | Do not broaden beyond this profile in this helper without approval. |
| `run_mode` | `"daily_brief_run"` | Run mode from the selected profile. | Yes | Must remain aligned with the selected profile. |
| `report_target` | `"daily_brief"` | Report target from the selected profile. | Yes | Must remain aligned with the selected profile and report templates. |
| `regions` | `["US"]` | Regions declared by the selected profile. | Yes | Additional regions require explicit profile/config approval. |
| `tagged_item_count` | integer | Number of retained tagged fixture items received from the tagger path. | Derived | Must equal `triaged_item_count`. |
| `triaged_item_count` | integer | Number of retained tagged items assigned a deterministic `TriageDecision`. | Derived | Must equal `tagged_item_count`. |
| `triage_mode` | `"fixture_rule_based_v0_1"` | Identifier for the current fixture-only deterministic triage rule set. | Yes | Any rule-set change requires explicit contract update. |
| `triage_rules_version` | `"TRIAGE_RULES_v0_1"` | Identifier for the governed rule source used by this helper. | Yes | Rule version changes require explicit contract update. |
| `priority_counts` | object | Counts of `P1`, `P2`, `P3`, and `DROP` decisions. | Derived | Must sum to `triaged_item_count`. |
| `reason_code_validation` | `"ok"` | Every emitted reason code belongs to the approved fixture triage reason set. | Yes | Additional states require explicit contract update. |
| `dropped_items_triaged` | `0` | Confirms dedup-dropped items were not triaged. | Yes | Must remain zero unless this contract is intentionally revised. |
| `deferred_runtime_behavior` | list of strings | Explicit marker of runtime and preprocessing behaviors not implemented in this helper. | Yes | May shrink only when a behavior is intentionally implemented and documented. |

## Optional Output Field

| Field | Trigger | Meaning | Constraints |
| --- | --- | --- | --- |
| `triage_decision_summaries` | Present only with `--show-decisions` | Compact summaries of deterministic preliminary triage decisions. | Must not include narrative analysis, report conclusions, recommendation language, full raw text, or bundle artifacts. |

Current `triage_decision_summaries` entries contain:

| Field | Meaning |
| --- | --- |
| `item_id` | Retained normalized item identifier. |
| `source_id` | Source ID copied from the retained item. |
| `preliminary_priority` | Deterministic preliminary priority from `P1`, `P2`, `P3`, or `DROP`. |
| `reason_codes` | Deterministic rule codes supporting the preliminary priority. |
| `topic_tags` | Existing topic tags passed through for review context. |
| `market_tags` | Existing market tags passed through for review context. |
| `risk_tags` | Existing risk tags passed through for review context. |

## Current Fixed Values

The current fixture triage slice fixes these values:

```json
{
  "fixture_triage_status": "ok",
  "profile_id": "daily_us_core",
  "run_mode": "daily_brief_run",
  "report_target": "daily_brief",
  "regions": ["US"],
  "tagged_item_count": 3,
  "triaged_item_count": 3,
  "triage_mode": "fixture_rule_based_v0_1",
  "triage_rules_version": "TRIAGE_RULES_v0_1",
  "priority_counts": {
    "P1": 3,
    "P2": 0,
    "P3": 0,
    "DROP": 0
  },
  "reason_code_validation": "ok",
  "dropped_items_triaged": 0
}
```

## Approved Reason Codes

The current fixture triage helper may emit only these reason codes:

- `TIER_1_OFFICIAL`
- `POLICY_RELEVANCE`
- `REGULATORY_RELEVANCE`
- `RATES_RELEVANCE`
- `MACRO_MARKET_RELEVANCE`
- `LABOR_RELEVANCE`
- `MARKET_STRUCTURE_RELEVANCE`
- `MANDATORY_CENTRAL_BANK_COMMUNICATION`
- `MANDATORY_OFFICIAL_MACRO_RELEASE`
- `MANDATORY_REGULATORY_ACTION_CANDIDATE`

These reason codes are reviewable rule markers only. They are not final analysis or investment recommendations.

## Deterministic Triage Rules

The current triage helper applies only these deterministic fixture-safe rules:

1. Load retained tagged fixture items from the fixture tagger path.
2. Load source authority and official status from `config/source_registry.yaml`.
3. Require `item_id`, `source_id`, `region`, `published_at`, `title`, `canonical_url`, and `content_type`.
4. Add source-authority and tag-based reason codes from the approved fixture rule set.
5. Map score to `P1`, `P2`, `P3`, or `DROP` using `TRIAGE_RULES.md`.
6. Apply fixture mandatory escalation for `fed_fomc`, `bls`, and `sec_press`.
7. Emit `TriageDecision` objects with `preliminary_priority`, `reason_codes`, and non-analytical `notes`.
8. Preserve deterministic ordering for summary output.

The triage helper does not perform deep interpretation, narrative analysis, final importance judgment, watchlist matching, event-chain continuity detection, operator override persistence, bundle assembly, or ai-meta-kernel reasoning.

## Validation Requirements

The fixture triage output is valid only if:

1. input tagged items come from the deterministic fixture tagger path;
2. every tagged retained item receives exactly one `TriageDecision`;
3. no dedup-dropped item receives triage;
4. `triaged_item_count == tagged_item_count`;
5. every `preliminary_priority` is one of `P1`, `P2`, `P3`, or `DROP`;
6. every reason code comes from the approved fixture triage reason set;
7. `priority_counts` sums to `triaged_item_count`;
8. required minimum metadata is present for every triaged item;
9. the output retains the explicit `deferred_runtime_behavior` markers.

## Deferred Runtime Behaviors

The following behaviors must remain absent from this fixture triage helper until explicitly implemented in a later governed task:

- `live_fetching`
- `production_triage`
- `advanced_negative_scoring`
- `watchlist_matching`
- `event_chain_continuity`
- `operator_override_persistence`
- `bundle_assembly`
- `report_composition`
- `ai_meta_kernel_runtime_handoff`

These markers are intentionally present in `deferred_runtime_behavior` so future expansion cannot silently change the helper's scope.

## Drift Control Rules

- Do not rename required output fields without updating this contract.
- Do not remove validation status fields without replacing them with equivalent explicit status.
- Do not change `triage_mode` without documenting the rule-set change.
- Do not change `triage_rules_version` without documenting rule source changes.
- Do not add production triage, advanced negative scoring, watchlist matching, event-chain continuity, operator override persistence, bundle assembly, report composition, live fetching, or kernel handoff while leaving those behaviors listed under `deferred_runtime_behavior`.
- Do not include narrative analysis, report conclusions, recommendation language, full raw text, or bundle artifacts in `triage_decision_summaries`.
- Do not treat `TriageDecision` output as an ingestion bundle item; bundle assembly remains deferred.
- Do not change this helper from `daily_us_core` to a generic triage runner without a new contract pass.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_triage.py'
```

To inspect compact triage decision summaries:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_triage.py' --show-decisions
```
