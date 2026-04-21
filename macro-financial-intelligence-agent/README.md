# Macro-Financial Intelligence Agent

This is the first reference implementation for validating the Meta-Layer.

Kernel dependency: `../ai-meta-kernel/`.

It monitors and synthesizes macro-financial, policy, and market-risk information across Hong Kong, Macau, Taiwan, Japan, the United States, and Europe.

It is not primarily a trading recommender. It should produce evidence synthesis, policy-risk monitoring, research reports, and archival outputs.

## v0.1 Status

This project is currently in a governed scaffold state.

Completed layers:

- Governance docs define boundaries, source discipline, reporting discipline, review checkpoints, and validation purpose.
- Config and contracts define approved sources, run profiles, ingestion bundle structure, and report templates.
- Governed examples show valid daily, weekly, and no-new-items ingestion bundles.
- Minimal scaffolds define raw item, normalization, dedup, tagging, triage, source registry loading, and bundle builder boundaries.
- Approved dependencies are declared for minimal structured YAML loading and ingestion bundle schema validation.
- Local scaffold contract checks cover selected contract expectations without running production behavior.
- Dependency-backed checks now validate structured config loading and example bundle JSON Schema compliance when dependencies are installed.

Not implemented yet:

- live fetching,
- open-web crawling,
- real scheduler execution,
- production YAML parsing beyond minimal governed config loading,
- full normalization / dedup / tagging / triage logic,
- production ingestion bundle assembly,
- report composition,
- archive/export automation,
- ai-meta-kernel runtime handoff execution.

## Authority Order

Repository-level authority:

1. `../AGENTS.md`
2. `../ai-meta-kernel/AGENTS.md`
3. `AGENTS.md`

Kernel contracts remain upstream. This project must not weaken or redefine them.

Operational macro-agent contracts:

| Area | Operational contract | Supporting / overview docs |
| --- | --- | --- |
| Approved sources | `config/source_registry.yaml` | `SOURCE_POLICY.md`, `acquisition/FETCH_POLICY.md` |
| Run profiles | `scheduler/run_profiles.yaml` | `AGENTS.md` scheduler rule |
| Ingestion bundle | `bundles/schemas/INGESTION_BUNDLE.schema.json` | `INGESTION_WORKFLOW.md` |
| Report structure | `reporting/templates/` | `REPORTING_WORKFLOW.md` |
| Validation execution | `validation/TEST_PLAN.md` | `VALIDATION_HOOKS.md`, `bundles/examples/VALIDATION_NOTES.md` |

## Current Scaffold Map

| File | Role |
| --- | --- |
| `acquisition/raw_item.py` | Raw source item shape and minimum field check. |
| `acquisition/source_registry_loader.py` | Source registry loading boundary with minimal PyYAML-backed structured loading. |
| `scheduler/run_profiles_loader.py` | Run profile loading boundary; does not run schedules. |
| `preprocessing/normalize/normalizer.py` | Normalized item shape and normalization boundary. |
| `preprocessing/dedup/deduper.py` | Dedup result shape and dedup boundary. |
| `preprocessing/tagging/tagger.py` | Tag shape and tagging boundary. |
| `preprocessing/triage/triage_scaffold.py` | Triage priority shape and preliminary triage boundary. |
| `bundles/bundle_builder.py` | Bundle build request shape and enum guard. |
| `bundles/bundle_schema_validator.py` | JSON Schema validation helper for ingestion bundle files. |

These files are scaffolds. Most methods intentionally raise `NotImplementedError`.

## Approved Dependencies

Approved dependencies are declared in `requirements.txt`:

- `PyYAML` for minimal structured loading of governed YAML config files.
- `jsonschema` for validating ingestion bundle artifacts against `bundles/schemas/INGESTION_BUNDLE.schema.json`.

Install only when dependency-backed validation or structured config loading is needed:

```powershell
python -m pip install -r 'macro-financial-intelligence-agent\requirements.txt'
```

Dependency approval does not authorize live fetching, scheduler runtime, report composition, CI setup, or package layout migration.

## Governed Examples

Example ingestion bundles live in `bundles/examples/`.

- `daily_us_core.example.json`
- `weekly_us_core.example.json`
- `daily_us_core_empty.example.json`
- `VALIDATION_NOTES.md`

They are static contract artifacts, not generated runtime output.

## Local Scaffold Contract Checks

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\validation\scaffold_contract_checks.py'
```

Expected output:

```text
scaffold-contract-checks-ok
```

The check file uses Python standard library only. It validates:

- `RawItem.validate_minimum_fields()`
- `IngestionBundleBuilder.validate_request_enums()`
- governed example bundle alignment with source IDs, run modes, report targets, authority tiers, priority labels, and item fields.

It does not validate full JSON Schema Draft 2020-12 behavior, YAML parsing, live data retrieval, scheduling, report generation, or kernel execution.

## Dependency-Backed Contract Checks

After installing approved dependencies:

```powershell
python -m pip install -r 'macro-financial-intelligence-agent\requirements.txt'
```

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\validation\dependency_backed_contract_checks.py'
```

Expected output:

```text
dependency-backed-contract-checks-ok
```

This validates:

- PyYAML-backed loading for `config/source_registry.yaml`.
- PyYAML-backed loading for `scheduler/run_profiles.yaml`.
- jsonschema-backed validation of governed example bundles.

It still does not fetch live sources, execute schedules, compose reports, add CI, migrate package layout, or execute ai-meta-kernel handoff.

## Semantic Contract Checks

Run after dependency-backed checks:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\validation\semantic_contract_checks.py'
```

Expected output:

```text
semantic-contract-checks-ok
```

This validates the currently in-scope cross-file semantic rules from `SEMANTIC_VALIDATION_PLAN.md`: source references, disabled-source selection, run mode/report target alignment, bundle date/count invariants, item source/tier consistency, and existing region-code consistency.

It still does not validate deferred rules such as fetcher capability, cron semantics, tag vocabularies, triage scoring, or kernel handoff compatibility.

## Unified Local Validation

Run the consolidated local validation wrapper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\validation\run_all_local_checks.py'
```

Expected final output:

```text
all-local-validation-checks-ok
```

The wrapper runs these existing validation layers in order:

1. `validation/scaffold_contract_checks.py`
2. `validation/dependency_backed_contract_checks.py`
3. `validation/semantic_contract_checks.py`

It is a local developer helper only. It does not add CI, fetch live sources, execute schedules, compose reports, migrate package layout, or replace the individual validation scripts.

## Daily US Core Dry-Run

Run the first governed local dry-run slice from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_dry_run.py'
```

This dry-run loads the governed source registry and run profiles, selects `daily_us_core`, resolves its whitelisted source IDs, constructs an in-memory no-new-items bundle-compatible artifact, and validates it against the ingestion bundle schema.

Output fields are governed by `DRY_RUN_OUTPUT_CONTRACT.md`.

Optional flags:

- `--show-artifact` prints the in-memory dry-run bundle artifact.
- `--run-local-checks` runs `validation/run_all_local_checks.py` after the dry-run.

It does not fetch live sources, execute cron, compose reports, archive outputs, or call ai-meta-kernel.

## Daily US Core Raw Fixture Loader

Run the first local fixture-bearing path from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_loader.py'
```

This loads `fixtures/daily_us_core_raw_items.fixture.json`, converts fixture records into `RawItem` objects, and validates minimum fields, selected source IDs, and profile region scope.

Output fields are governed by `FIXTURE_LOADER_OUTPUT_CONTRACT.md`.

Optional flag:

- `--show-items` prints compact validated `RawItem` summaries.

It does not normalize, deduplicate, tag, triage, build bundles, fetch live sources, compose reports, or call ai-meta-kernel.

## Daily US Core Fixture Normalizer

Run the first fixture-driven normalization helper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_normalizer.py'
```

This reuses validated fixture `RawItem` objects and converts them into deterministic `NormalizedItem` objects with title trimming, URL/timestamp fallback, stable item IDs, and fixed-length raw excerpts.

Output fields are governed by `FIXTURE_NORMALIZER_OUTPUT_CONTRACT.md`.

Optional flag:

- `--show-items` prints compact `NormalizedItem` summaries.

It does not deduplicate, tag, triage, build bundles, fetch live sources, compose reports, or call ai-meta-kernel.

## Daily US Core Fixture Deduper

Run the first fixture-driven dedup helper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_deduper.py'
```

This reuses deterministic fixture `NormalizedItem` objects and groups them with the current exact canonical URL strategy. Singleton groups are retained. Multi-item groups retain the lexicographically lowest `item_id` until governed source-precedence rules are defined.

Output fields are governed by `FIXTURE_DEDUPER_OUTPUT_CONTRACT.md`.

Optional flag:

- `--show-groups` prints compact dedup group summaries.

It does not perform production deduplication, fuzzy matching, source-precedence ranking, tagging, triage, build bundles, fetch live sources, compose reports, or call ai-meta-kernel.

## Daily US Core Fixture Tagger

Run the first fixture-driven tagging helper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_tagger.py'
```

This reuses retained deterministic fixture `NormalizedItem` objects and assigns controlled-vocabulary `TagSet` outputs using the current fixture rule set.

Optional flag:

- `--show-tags` prints compact tagged item summaries.

It does not perform production tagging, open-ended tag generation, priority scoring, triage, build bundles, fetch live sources, compose reports, or call ai-meta-kernel.

## Development Rules

- Keep `ai-meta-kernel/` and this project as parallel projects.
- Do not add uncontrolled open-web crawling.
- Do not auto-expand `config/source_registry.yaml`.
- Do not turn this agent into a direct trading recommender.
- Preserve `INGESTION_BUNDLE.schema.json` field names.
- Use explicit TODOs when runtime behavior is intentionally deferred.
