# Fixture Tagger Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for the `daily_us_core` fixture tagger.

It exists to prevent silent output drift as preprocessing expands. It does not define live fetching, scheduler execution, production tagging for live pages, open-ended tag generation, AI-assisted classification, priority scoring, triage, bundle assembly, report composition, CI, package migration, external service calls, or ai-meta-kernel runtime handoff.

## Scope

This contract applies only to:

- script: `workflows/daily_us_core_fixture_tagger.py`
- upstream fixture deduper: `workflows/daily_us_core_fixture_deduper.py`
- upstream fixture normalizer: `workflows/daily_us_core_fixture_normalizer.py`
- upstream fixture file: `fixtures/daily_us_core_raw_items.fixture.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`

It covers the JSON object printed by the fixture tagger.

## Required Output Fields

| Field | Current value / type | Meaning | Fixed for current slice? | Future expansion rule |
| --- | --- | --- | --- | --- |
| `fixture_tagging_status` | `"ok"` | Indicates deterministic fixture tagging completed and validation checks passed. | Yes | Additional status variants require explicit contract update. |
| `profile_id` | `"daily_us_core"` | Governed profile inherited from the fixture deduper path. | Yes | Do not broaden beyond this profile in this helper without approval. |
| `run_mode` | `"daily_brief_run"` | Run mode from the selected profile. | Yes | Must remain aligned with the selected profile. |
| `report_target` | `"daily_brief"` | Report target from the selected profile. | Yes | Must remain aligned with the selected profile and report templates. |
| `regions` | `["US"]` | Regions declared by the selected profile. | Yes | Additional regions require explicit profile/config approval. |
| `retained_item_count` | integer | Number of retained deterministic fixture items received from the deduper path. | Derived | Must equal `tagged_item_count` for this slice. |
| `tagged_item_count` | integer | Number of retained items assigned a deterministic `TagSet`. | Derived | Must equal `retained_item_count`. |
| `tagging_mode` | `"fixture_rule_based_v0_1"` | Identifier for the current fixture-only deterministic tagging rule set. | Yes | Any rule-set change requires explicit contract update. |
| `tag_vocabulary_version` | `"fixture_tags_v0_1"` | Identifier for the current controlled vocabulary. | Yes | Vocabulary changes require explicit contract update. |
| `vocabulary_validation` | `"ok"` | Every emitted tag belongs to the current controlled vocabulary. | Yes | Additional states require explicit contract update. |
| `dropped_items_tagged` | `0` | Confirms dedup-dropped items were not tagged. | Yes | Must remain zero unless this contract is intentionally revised. |
| `deferred_runtime_behavior` | list of strings | Explicit marker of runtime and preprocessing behaviors not implemented in this helper. | Yes | May shrink only when a behavior is intentionally implemented and documented. |

## Optional Output Field

| Field | Trigger | Meaning | Constraints |
| --- | --- | --- | --- |
| `tagged_item_summaries` | Present only with `--show-tags` | Compact summaries of deterministic tags assigned to retained items. | Must not include raw text, excerpts, triage scores, priority labels, report conclusions, or analysis. |

Current `tagged_item_summaries` entries contain:

| Field | Meaning |
| --- | --- |
| `item_id` | Retained normalized item identifier. |
| `source_id` | Source ID copied from the retained item. |
| `topic_tags` | Deterministic topic tags from the controlled vocabulary. |
| `market_tags` | Deterministic market-context tags from the controlled vocabulary. |
| `risk_tags` | Deterministic risk-context tags from the controlled vocabulary. |

## Current Fixed Values

The current fixture tagger slice fixes these values:

```json
{
  "fixture_tagging_status": "ok",
  "profile_id": "daily_us_core",
  "run_mode": "daily_brief_run",
  "report_target": "daily_brief",
  "regions": ["US"],
  "retained_item_count": 3,
  "tagged_item_count": 3,
  "tagging_mode": "fixture_rule_based_v0_1",
  "tag_vocabulary_version": "fixture_tags_v0_1",
  "vocabulary_validation": "ok",
  "dropped_items_tagged": 0
}
```

## Controlled Vocabulary

The current fixture tagger may emit only these tags.

| Tag field | Allowed values |
| --- | --- |
| `topic_tags` | `monetary_policy`, `labor_market`, `securities_regulation` |
| `market_tags` | `rates`, `macro_data`, `equities`, `credit` |
| `risk_tags` | `policy_path`, `inflation_growth`, `regulatory`, `market_structure` |

Unused vocabulary entries may exist to keep the first controlled set stable for nearby fixture expansion. They are not permission for open-ended tag generation.

## Deterministic Tagging Rules

The current tagger applies only these deterministic fixture-safe rules:

1. Load retained deterministic fixture `NormalizedItem` objects from the fixture deduper path.
2. Tag retained items only.
3. Fail visibly if a retained item has no approved source-specific fixture tag rule.
4. For `fed_fomc`, emit `topic_tags = ["monetary_policy"]`, `market_tags = ["rates"]`, and `risk_tags = ["policy_path"]`.
5. For `bls`, emit `topic_tags = ["labor_market"]`, `market_tags = ["macro_data"]`, and `risk_tags = ["inflation_growth"]`.
6. For `sec_press`, emit `topic_tags = ["securities_regulation"]`, `market_tags = ["equities"]`, and `risk_tags = ["regulatory"]`.
7. Preserve deterministic tag ordering.

The tagger does not perform open-ended tag generation, AI-assisted classification, priority scoring, triage, source confidence evaluation, or market analysis.

## Validation Requirements

The fixture tagger output is valid only if:

1. input retained items come from the deterministic fixture deduper path;
2. every retained item receives exactly one `TagSet`;
3. no dedup-dropped item receives tags;
4. `tagged_item_count == retained_item_count`;
5. `dropped_items_tagged == 0`;
6. every tag is drawn from the controlled vocabulary;
7. tag arrays are non-empty for current fixture items;
8. the output retains the explicit `deferred_runtime_behavior` markers.

## Deferred Runtime Behaviors

The following behaviors must remain absent from this fixture tagger until explicitly implemented in a later governed task:

- `live_fetching`
- `production_tagging`
- `open_ended_tag_generation`
- `ai_assisted_classification`
- `priority_scoring`
- `triage`
- `bundle_assembly`
- `report_composition`
- `ai_meta_kernel_runtime_handoff`

These markers are intentionally present in `deferred_runtime_behavior` so future expansion cannot silently change the helper's scope.

## Drift Control Rules

- Do not rename required output fields without updating this contract.
- Do not remove validation status fields without replacing them with equivalent explicit status.
- Do not change `tagging_mode` without documenting the rule-set change.
- Do not change `tag_vocabulary_version` without documenting vocabulary changes.
- Do not add production tagging, open-ended tag generation, AI-assisted classification, priority scoring, triage, bundle assembly, report composition, live fetching, or kernel handoff while leaving those behaviors listed under `deferred_runtime_behavior`.
- Do not include raw text, excerpts, triage scores, priority labels, report conclusions, or analysis in `tagged_item_summaries`.
- Do not treat `TagSet` output as an ingestion bundle item; bundle assembly remains deferred.
- Do not change this helper from `daily_us_core` to a generic tag runner without a new contract pass.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_tagger.py'
```

To inspect compact tagged item summaries:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_tagger.py' --show-tags
```
