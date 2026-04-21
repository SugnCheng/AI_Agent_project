# AGENTS.md

## Repository Purpose

This repository contains two parallel but related projects:

1. `ai-meta-kernel/`
2. `macro-financial-intelligence-agent/`

They are not the same thing.

`ai-meta-kernel/` is the core meta-cognitive kernel intended to serve as a shared reasoning layer for future downstream agents.

`macro-financial-intelligence-agent/` is the first real application / validation agent built around that kernel.

---

## Primary Repository Rule

Do not collapse the two projects into one.

Do not treat `macro-financial-intelligence-agent/` as the owner of the kernel.
Do not move the kernel under the macro agent.
Do not redefine the macro agent as the master specification for the repository.

The repository hierarchy is intentional:

- `ai-meta-kernel/` = platform / shared core / upstream authority
- `macro-financial-intelligence-agent/` = parallel application / validation project

---

## Current Strategic Priority

Current priority is not broad feature expansion.

Current priority is:
1. protect meta-layer fidelity,
2. preserve canonical contracts,
3. build a controlled macro-financial intelligence pipeline around the kernel,
4. avoid terminology drift across specs, schemas, templates, and handoff contracts.

If there is any conflict between convenience and contract consistency, prefer contract consistency.

---

## Project-Specific Guidance

### A. ai-meta-kernel

This project is the canonical reasoning core.

Its responsibilities include:
- problem framing,
- task classification,
- risk calibration,
- habit triggering,
- separation of facts / assumptions / inferences / unknowns,
- verification logic,
- challenge loop,
- status flags,
- downstream handoff.

When modifying files in `ai-meta-kernel/`:
- preserve canonical naming,
- avoid introducing alternate field names,
- prefer master-spec alignment over local convenience,
- do not add decorative placeholders.

If there is ambiguity, treat the master specification as the source of truth.

### B. macro-financial-intelligence-agent

This project is the first real application and reference validation pipeline.

Its responsibilities include:
- scheduler / automation,
- whitelist-based acquisition,
- preprocessing / normalization / dedup / tagging,
- preliminary triage,
- ingestion bundle creation,
- report composition,
- review workflow,
- archive packaging.

It must use `ai-meta-kernel` as its reasoning core.
It must not invent a competing reasoning framework.

---

## Acquisition Philosophy for macro-financial-intelligence-agent

This project is whitelist-first.

Do not implement uncontrolled open-web crawling as a default behavior.
Do not autonomously expand the source universe.
Do not scrape arbitrary internet sources without explicit approval.

v0.1 acquisition should remain restricted to approved sources defined in:
- `macro-financial-intelligence-agent/config/source_registry.yaml`

---

## Reporting Philosophy

Reports are not free-form essays.

They should follow structured templates:
- daily brief
- weekly intelligence report
- special event memo

Required qualities:
- traceable sources,
- explicit importance framing,
- transmission logic,
- unknowns / uncertainties,
- watch points,
- review hooks.

---

## Human-in-the-loop Rule

This system is intended to collaborate with a human operator.

Do not remove operator review checkpoints.
Do not silently replace operator decisions with hidden heuristics.
Do not introduce self-modifying source governance without explicit approval.

---

## Validation and Change Discipline

When making meaningful changes:
1. explain what changed,
2. identify affected files,
3. preserve JSON / YAML validity,
4. avoid naming drift,
5. note any unresolved human decisions.

If a change risks breaking alignment between:
- master spec,
- schema,
- output template,
- handoff contract,
- adapter layer,

call it out explicitly.

---

## Preferred Work Order for Codex

When asked to extend the repo, prefer this order:

1. validate contracts and naming consistency
2. extend configuration files
3. add schemas and templates
4. add workflow documents
5. add minimal implementation scaffolds
6. add validation examples
7. only then add broader automation features

Do not jump straight to large implementation if the contract layer is unstable.

---

## What to Avoid

Avoid the following unless explicitly requested:
- open-web autonomous exploration
- hidden runtime behaviors
- schema drift
- duplicate master specifications
- mixing kernel governance with macro-agent local shortcuts
- replacing structured outputs with loose prose
- speculative features that bypass current architecture

---

## Expected Output Style for Changes

When proposing repository changes:
- be explicit,
- be conservative with naming,
- keep outputs structured,
- prefer files that are directly usable,
- flag any place where human choice is still required.

This repository values governed architecture over flashy expansion.