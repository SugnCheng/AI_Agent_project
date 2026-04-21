# Dependency and Structure Decisions

## Purpose

This document records conservative v0.1 decisions for dependencies and project structure before the next implementation stage.

It is developer-facing. PyYAML and jsonschema have been approved, declared in `requirements.txt`, and integrated into dependency-backed local validation. This does not authorize live fetching, scheduling, report composition, package migration, CI, or kernel contract changes.

## Decision 1: YAML Parsing

### Current Status

The project uses YAML for:

- `config/source_registry.yaml`
- `scheduler/run_profiles.yaml`

The current scaffold can load governed YAML config files with PyYAML when dependencies are installed. Production config semantics remain intentionally limited.

### Options Considered

1. Use PyYAML.
2. Use `ruamel.yaml`.
3. Avoid YAML parsing temporarily and keep manual / regex-level checks.
4. Convert configs to JSON.

### Recommended Conservative Path for v0.1

Use **PyYAML** for minimal structured loading of governed config files.

Rationale:

- It is widely used and low-friction.
- The config files are simple mappings/lists and do not need round-trip formatting preservation.
- It is sufficient for validation and controlled loading.

Do not expand this into production scheduling or source selection behavior.

### Explicitly Deferred

- Adding `pyproject.toml` dependency declarations.
- Implementing production source selection.
- Supporting advanced YAML features.

## Decision 2: JSON Schema Validation

### Current Status

`bundles/schemas/INGESTION_BUNDLE.schema.json` is the operational ingestion bundle contract.

Current local checks include both lightweight standard-library assertions and dependency-backed JSON Schema validation for governed example bundles.

### Options Considered

1. Use `jsonschema`.
2. Use a faster validator such as `fastjsonschema`.
3. Keep standard-library-only checks for now.
4. Write a custom schema validator.

### Recommended Conservative Path for v0.1

Use **jsonschema** when full schema validation becomes necessary.

Rationale:

- It supports standard JSON Schema behavior.
- It is more appropriate than custom validation for schema correctness.
- The current project benefits more from clarity than from validator speed.

For the current scaffold state, keep the lightweight local checks as a dependency-free guard and use the minimal jsonschema-backed helper for dependency-backed validation.

### Explicitly Deferred

- Enforcing full Draft 2020-12 validation in CI.
- Replacing existing lightweight scaffold checks.
- Writing a custom schema validator.

## Decision 3: Schemas for YAML Config Files

### Current Status

The project has an ingestion bundle JSON Schema, but does not yet have formal schemas for:

- `config/source_registry.yaml`
- `scheduler/run_profiles.yaml`

The files include validation comments and are checked indirectly through local scaffold checks.

### Options Considered

1. Add JSON Schema files for YAML config shape.
2. Add informal Markdown specs only.
3. Use Python dataclasses / typed config objects as the source of validation.
4. Defer formal config schemas.

### Recommended Conservative Path for v0.1

Create formal config schemas **after** the first minimal structured YAML loader exists.

Rationale:

- The loader will clarify which fields are actually consumed.
- Adding schemas too early risks freezing fields that are still governed but not operationally exercised.
- The current comments and examples are sufficient for scaffold-level work.

### Explicitly Deferred

- `source_registry.schema.json`
- `run_profiles.schema.json`
- Cross-file semantic validation such as source eligibility and enabled-source selection.
- Schema-driven generation of config docs.

## Decision 4: Project Layout

### Current Status

The project directory name is `macro-financial-intelligence-agent`, which is suitable as a repository folder but not as a Python import package name.

Scaffold files currently live directly under domain folders:

- `acquisition/`
- `preprocessing/`
- `bundles/`
- `validation/`

Local checks use file-path loading via `importlib` to avoid forcing a package layout decision.

### Options Considered

1. Keep the current flat scaffold layout.
2. Add a formal package such as `macro_financial_intelligence_agent/`.
3. Rename the project directory.
4. Add package markers to the current hyphenated directory.

### Recommended Conservative Path for v0.1

Keep the current flat scaffold layout for now.

Introduce a formal import package only when multiple modules need stable imports beyond local checks.

Likely future package name:

- `macro_financial_intelligence_agent`

Rationale:

- Avoids a premature restructure.
- Preserves the current parallel repo structure.
- Keeps the scaffold readable while contracts are still settling.

### Explicitly Deferred

- Creating a package directory.
- Adding `__init__.py` files.
- Moving existing scaffold modules.
- Renaming the project folder.

## Decision 5: Local Checks and CI

### Current Status

Local scaffold checks live at:

- `validation/scaffold_contract_checks.py`
- `validation/dependency_backed_contract_checks.py`

The first script runs with Python standard library only. The second script uses approved dependencies for structured YAML loading and bundle schema validation. Both are documented in `README.md`.

### Options Considered

1. Keep checks manual-only.
2. Add GitHub Actions now.
3. Add a script wrapper without CI.
4. Add CI after dependency decisions are settled.

### Recommended Conservative Path for v0.1

Keep checks manual-only for the current scaffold phase.

Promote them to CI after:

1. dependency choices are approved,
2. config schema direction is settled,
3. package layout is stable enough to avoid brittle path loading.

Rationale:

- Manual checks are sufficient for current scaffold confidence.
- CI too early may harden temporary path-loading assumptions.
- The next implementation stage should still prioritize contract stability.

### Explicitly Deferred

- GitHub Actions workflow.
- Test framework adoption.
- Dependency installation.
- Coverage or quality gates.

## Summary of Recommended v0.1 Path

| Topic | Recommendation |
| --- | --- |
| YAML parsing | PyYAML approved for minimal structured config loading. |
| JSON Schema validation | `jsonschema` approved for ingestion bundle schema validation helper. |
| YAML config schemas | Defer until structured config loading exists. |
| Project layout | Keep flat scaffold layout now; consider `macro_financial_intelligence_agent` package later. |
| CI | Keep manual checks now; revisit after dependencies and layout stabilize. |

## Next Implementation Gate

Before adding real runtime behavior, decide whether to approve:

1. production source selection semantics,
2. semantic validation rules beyond JSON Schema,
3. a small package layout migration.

Until then, implementation should remain scaffold-level and governed by the current contracts.
