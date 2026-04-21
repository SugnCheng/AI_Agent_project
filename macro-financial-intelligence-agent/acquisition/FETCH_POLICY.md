# FETCH_POLICY

## Document Status
- version: 0.1
- owner: macro-financial-intelligence-agent
- purpose: acquisition policy for whitelist-based controlled retrieval

## Authority

This file is the operational acquisition policy for v0.1.

It must be read together with:
- `../config/source_registry.yaml` as the approved source inventory.
- `../SOURCE_POLICY.md` as the high-level source quality overview.

If there is a conflict about fetch eligibility, whitelist behavior, or approved fetch methods, this file and `../config/source_registry.yaml` take precedence over the high-level overview.

---

## 1. Objective

The acquisition layer is responsible for retrieving source material from approved sources only.

Its purpose is to:
1. collect source material reliably,
2. preserve source traceability,
3. avoid uncontrolled information expansion,
4. prepare clean inputs for preprocessing and triage.

This layer is not responsible for final analysis.

---

## 2. Acquisition Philosophy

v0.1 follows a whitelist-first acquisition model.

The system must not perform open-web exploration as a default behavior.
The system must not autonomously expand its source universe.
The system must not treat all internet content as equally eligible.

All acquisition must start from explicitly approved sources listed in:
- `config/source_registry.yaml`

---

## 3. Approved Fetch Methods for v0.1

Allowed fetch methods:

- `rss`
- `official_html`
- `official_pdf_index`
- `manual_feed_stub`

Disallowed by default in v0.1:

- unrestricted crawling
- autonomous search-engine expansion
- social media scraping
- forum scraping
- unofficial mirrors when official source is available

---

## 4. Source Governance Rules

A source is eligible only if all of the following are true:

1. it has a valid `source_id`,
2. it exists in `source_registry.yaml`,
3. `enabled` is `true`,
4. it matches the active run scope or is explicitly included,
5. its fetch method is supported by the current runtime.

If any of the above conditions fail, the source must not be fetched.

---

## 5. Retrieval Rules

### 5.1 Scope Control
Acquisition must respect:
- active run mode,
- active region scope,
- source inclusion / exclusion rules,
- authority tier filters.

### 5.2 Time Window Control
Acquisition must respect the execution window defined by the active run profile.

Example:
- daily run → last 24 hours
- weekly run → last 7 days
- custom range run → operator-defined interval

### 5.3 Traceability
Every retrieved item must preserve:
- `source_id`
- `source_url`
- `canonical_url` when available
- `retrieved_at`
- `published_at` when available
- `title`
- raw or minimally cleaned source text

### 5.4 Non-destructive Capture
Acquisition should preserve source meaning.
Do not rewrite source content during retrieval.
Do not summarize during retrieval.
Do not classify narrative implications during retrieval.

---

## 6. Minimum Raw Item Contract

Each fetcher should output a raw item with the following minimum fields:

- `source_id`
- `retrieved_at`
- `source_url`
- `title`
- `published_at` if available
- `raw_text`
- `content_type`
- `language`
- `region`

Items missing `source_id`, `retrieved_at`, `source_url`, `title`, or `raw_text` should be quarantined or dropped.

---

## 7. Preferred Source Ordering

When functionally similar items exist, preserve priority by source authority:

1. official Tier 1 source
2. official statistics / exchange / regulator source
3. approved mainstream financial media
4. research institute / think tank
5. secondary commentary

If a media article only repeats an available official source, the official source should be preserved as primary.

---

## 8. PDF Handling

For `official_pdf_index` sources:

1. preserve the index page URL,
2. preserve the resolved document URL,
3. capture document title if available,
4. capture publication date if available,
5. store extracted text separately from metadata.

Do not discard metadata even when text extraction is partial.

---

## 9. Error Handling

Possible fetch outcomes:

- `success`
- `partial_success`
- `no_new_items`
- `temporary_failure`
- `blocked`
- `invalid_source_config`

Failures must be logged with:
- `source_id`
- timestamp
- fetch method
- error class
- short error note

Do not silently swallow acquisition failures.

---

## 10. Rate and Stability Discipline

Acquisition should be stable and polite.

Rules:
- avoid excessive request bursts,
- use predictable source-specific intervals,
- prefer official structured endpoints when available,
- avoid fragile scraping when a cleaner official path exists.

v0.1 prioritizes reliability over breadth.

---

## 11. Change Control

No new source should be fetched in production unless one of the following occurs:

1. operator manually adds it to `source_registry.yaml`,
2. a reviewed governance update explicitly enables it.

No runtime component may self-append new sources.

---

## 12. Human-in-the-loop Controls

The operator must be able to:
- enable or disable a source,
- change region scope,
- raise or lower source priority,
- approve a new source,
- temporarily suppress a noisy source.

These controls should be implemented through configuration, not hidden runtime behavior.

---

## 13. Logging Expectations

Each run should produce an acquisition log containing:

- `run_id`
- `profile_id`
- `source_id`
- fetch status
- item count retrieved
- item count accepted
- item count quarantined
- item count dropped
- notes

This log should remain reviewable and archivable.

---

## 14. v0.1 Non-goals

The following are out of scope for v0.1:

- open-web autonomous discovery
- generalized internet crawling
- social sentiment collection
- real-time market tick ingestion
- unsupervised source expansion
- multi-hop source discovery
- fully autonomous event-driven routing

These may be considered only after whitelist acquisition is stable.
