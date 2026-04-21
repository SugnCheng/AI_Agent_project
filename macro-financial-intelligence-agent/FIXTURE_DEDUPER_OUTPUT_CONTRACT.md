# Fixture Deduper Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for the `daily_us_core` fixture deduper.

It exists to prevent silent output drift as preprocessing expands. It does not define live fetching, scheduler execution, production deduplication for live pages, fuzzy matching, source-precedence ranking, tagging, triage, bundle assembly, report composition, CI, package migration, external service calls, or ai-meta-kernel runtime handoff.

## Scope

This contract applies only to:

- script: `workflows/daily_us_core_fixture_deduper.py`
- upstream fixture normalizer: `workflows/daily_us_core_fixture_normalizer.py`
- upstream fixture file: `fixtures/daily_us_core_raw_items.fixture.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`

It covers the JSON object printed by the fixture deduper.

## Required Output Fields

| Field | Current value / type | Meaning | Fixed for current slice? | Future expansion rule |
| --- | --- | --- | --- | --- |
| `fixture_dedup_status` | `"ok"` | Indicates deterministic fixture dedup completed and invariant checks passed. | Yes | Additional status variants require explicit contract update. |
| `profile_id` | `"daily_us_core"` | Governed profile inherited from the fixture normalizer path. | Yes | Do not broaden beyond this profile in this helper without approval. |
| `run_mode` | `"daily_brief_run"` | Run mode from the selected profile. | Yes | Must remain aligned with the selected profile. |
| `report_target` | `"daily_brief"` | Report target from the selected profile. | Yes | Must remain aligned with the selected profile and report templates. |
| `regions` | `["US"]` | Regions declared by the selected profile. | Yes | Additional regions require explicit profile/config approval. |
| `normalized_item_count` | integer | Number of deterministic fixture `NormalizedItem` inputs received from the normalizer path. | Derived | Must equal retained plus dropped item counts. |
| `retained_item_count` | integer | Number of normalized items retained after exact deterministic grouping. | Derived | Must be at least one for the current non-empty fixture set. |
| `dropped_item_count` | integer | Number of normalized items dropped as duplicates. | Derived | May be zero when no duplicate groups are present. |
| `dedup_group_count` | integer | Number of deterministic dedup groups emitted. | Derived | Must equal the number of exact canonical URL groups. |
| `dedup_mode` | `"fixture_exact_url_v0_1"` | Identifier for the current fixture-only exact dedup rule set. | Yes | Any rule-set change requires explicit contract update. |
| `dedup_key_strategy` | `"canonical_url_key"` | Exact key strategy used for grouping. | Yes | Changes require explicit contract update and fixture review. |
| `invariant_validation` | `"ok"` | Main retained/dropped/group membership invariants passed. | Yes | Additional states require explicit contract update. |
| `deferred_runtime_behavior` | list of strings | Explicit marker of runtime and preprocessing behaviors not implemented in this helper. | Yes | May shrink only when a behavior is intentionally implemented and documented. |

## Optional Output Field

| Field | Trigger | Meaning | Constraints |
| --- | --- | --- | --- |
| `dedup_group_summaries` | Present only with `--show-groups` | Compact summaries of deterministic dedup groups. | Must contain item IDs only, not full item bodies, raw text, excerpts, tags, triage, or analysis. |

Current `dedup_group_summaries` entries contain:

| Field | Meaning |
| --- | --- |
| `dedup_group_id` | Deterministic non-semantic ID derived from the exact dedup key. |
| `item_ids` | Ordered item IDs assigned to this group. |
| `retained_item_id` | Item ID retained for the group. |
| `dropped_item_ids` | Item IDs dropped as duplicates. Empty for singleton groups. |

## Current Fixed Values

The current fixture deduper slice fixes these values:

```json
{
  "fixture_dedup_status": "ok",
  "profile_id": "daily_us_core",
  "run_mode": "daily_brief_run",
  "report_target": "daily_brief",
  "regions": ["US"],
  "normalized_item_count": 3,
  "retained_item_count": 3,
  "dropped_item_count": 0,
  "dedup_group_count": 3,
  "dedup_mode": "fixture_exact_url_v0_1",
  "dedup_key_strategy": "canonical_url_key",
  "invariant_validation": "ok"
}
```

The current fixture set has no duplicate canonical URLs, so `dropped_item_count` is currently `0`. A future fixture revision may add duplicates, but that must be documented as a fixture change rather than silently changing this contract.

## Deterministic Dedup Rules

The current deduper applies only these deterministic fixture-safe rules:

1. Load deterministic fixture `NormalizedItem` objects from the fixture normalizer path.
2. Require each input item to have `item_id` and `canonical_url`.
3. Build `canonical_url_key` by trimming, lowercasing, and removing a trailing slash from `canonical_url`.
4. Group items by exact `canonical_url_key`.
5. Generate `dedup_group_id` deterministically from the exact key.
6. Retain singleton groups.
7. For multi-item groups, retain the lexicographically lowest `item_id`.
8. Mark remaining group members as dropped.
9. Store dedup groups as item IDs only.

The deduper does not perform fuzzy matching, source-precedence ranking, semantic equivalence detection, tagging, triage, or market analysis.

## Validation Requirements

The fixture deduper output is valid only if:

1. input `NormalizedItem` objects come from the deterministic fixture normalizer path;
2. every input item appears in exactly one dedup group;
3. no item ID appears in more than one dedup group;
4. retained and dropped item sets do not overlap;
5. `retained_item_count + dropped_item_count == normalized_item_count`;
6. dropped items only come from groups with more than one item;
7. `dedup_groups` stores item IDs only, not full item bodies;
8. the output retains the explicit `deferred_runtime_behavior` markers.

## Deferred Runtime Behaviors

The following behaviors must remain absent from this fixture deduper until explicitly implemented in a later governed task:

- `live_fetching`
- `production_deduplication`
- `fuzzy_matching`
- `source_precedence`
- `tagging`
- `triage`
- `bundle_assembly`
- `report_composition`
- `ai_meta_kernel_runtime_handoff`

These markers are intentionally present in `deferred_runtime_behavior` so future expansion cannot silently change the helper's scope.

## Drift Control Rules

- Do not rename required output fields without updating this contract.
- Do not remove validation status fields without replacing them with equivalent explicit status.
- Do not change `dedup_mode` without documenting the rule-set change.
- Do not change `dedup_key_strategy` without reviewing fixture output stability.
- Do not add production deduplication, fuzzy matching, source precedence, tagging, triage, bundle assembly, report composition, live fetching, or kernel handoff while leaving those behaviors listed under `deferred_runtime_behavior`.
- Do not include full item bodies, raw text, excerpts, or analysis in `dedup_group_summaries`.
- Do not treat `DedupResult` output as an ingestion bundle item; bundle assembly remains deferred.
- Do not change this helper from `daily_us_core` to a generic dedup runner without a new contract pass.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_deduper.py'
```

To inspect compact dedup group summaries:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_deduper.py' --show-groups
```
