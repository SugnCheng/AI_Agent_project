# AGENTS.md

## Project Identity

This directory contains the `macro-financial-intelligence-agent`, which is the first downstream application / reference validation agent built around `ai-meta-kernel`.

It is not the owner of the repository.
It is not the canonical source of truth for Meta-Layer design.
It must operate as a governed downstream implementation.

The upstream reasoning authority remains:
- `../ai-meta-kernel/`
- and the repository root `../AGENTS.md`

If there is any conflict between local convenience and kernel / repository governance, prefer the upstream governance.

---

## Mission

The purpose of this project is to build a controlled macro-financial intelligence pipeline that can:

- run on schedule,
- retrieve source material from approved sources,
- preprocess and triage retrieved items,
- build structured ingestion bundles,
- pass structured material into the kernel,
- produce structured reports,
- support operator review and archive workflows.

This project is a research-intelligence pipeline, not a direct trading engine.

---

## Core Boundary

This project may perform:

- macro-financial information collection from approved sources,
- policy / regulatory monitoring,
- evidence packaging,
- report drafting,
- structured review and archive preparation.

This project must not perform by default:

- uncontrolled open-web crawling,
- autonomous source universe expansion,
- hidden reasoning bypass around the kernel,
- direct personalized investment recommendations,
- unsupported certainty claims.

---

## Acquisition Rule

This project is whitelist-first.

Only retrieve from approved sources defined in:
- `config/source_registry.yaml`

Do not implement uncontrolled exploration as the default behavior.
Do not auto-add new sources at runtime.
Do not treat arbitrary public internet content as approved input.

Related governance documents:
- `acquisition/FETCH_POLICY.md`
- `SOURCE_POLICY.md`

---

## Reporting Rule

Reports must remain structured.

Required report types:
- daily brief
- weekly intelligence report
- special event memo

Use the templates in:
- `reporting/templates/`

Do not replace structured reporting with loose prose output.

Required qualities:
- source traceability,
- explicit importance framing,
- transmission logic,
- uncertainty / unknowns,
- watch points,
- review hooks.

---

## Review Rule

Human-in-the-loop is mandatory.

Do not remove review checkpoints.
Do not silently override operator intent.
Do not implement hidden adaptive governance.

Review behavior must remain compatible with:
- `review/REVIEW_WORKFLOW.md`

---

## Triage Rule

Preliminary triage is rule-based first.

Do not treat triage as final analysis.
Do not let triage replace kernel reasoning.
Do not silently promote assumptions into facts.

Triage behavior must remain compatible with:
- `preprocessing/triage/TRIAGE_RULES.md`

---

## Bundle Contract Rule

The ingestion bundle is a formal contract artifact.

Use:
- `bundles/schemas/INGESTION_BUNDLE.schema.json`

Do not introduce ad hoc bundle field names.
Do not add silent field drift.
Do not rename fields casually for local convenience.

---

## Scheduler Rule

Run configuration must remain explicit and reviewable.

Use:
- `scheduler/run_profiles.yaml`

Do not hide scheduling assumptions in code when they belong in configuration.

---

## Relationship to ai-meta-kernel

This project must use `ai-meta-kernel` as its reasoning core.

It must not:
- invent a competing reasoning framework,
- bypass required kernel checks,
- reconstruct missing handoff fields silently,
- weaken verification or challenge requirements imposed by the kernel.

If kernel inputs are materially incomplete, return for clarification / reframe rather than improvising.

---

## Preferred Work Order

When extending this project, prefer this order:

1. validate path and naming alignment
2. preserve contract consistency
3. extend config and policy files
4. extend schemas and templates
5. add minimal scaffolds
6. add validation examples
7. only then add broader implementation logic

Do not jump directly to large implementation if the governance layer is unstable.

---

## What to Avoid

Avoid the following unless explicitly requested:

- open-web autonomous discovery
- source expansion without approval
- hidden runtime behaviors
- schema drift
- duplicate local master specs
- report outputs that lose traceability
- speculative implementation that outruns governance

---

## Expected Change Style

When proposing or applying changes in this directory:

- be explicit,
- keep names conservative,
- preserve compatibility with upstream governance,
- note affected files,
- identify unresolved human decisions,
- prefer directly usable files over vague suggestions.

This directory exists to validate a governed intelligence pipeline, not to maximize flashy autonomy.