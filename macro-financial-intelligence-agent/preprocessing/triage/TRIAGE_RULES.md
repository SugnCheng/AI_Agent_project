# TRIAGE_RULES

## Document Status
- version: 0.1
- owner: macro-financial-intelligence-agent
- purpose: rule-based preliminary triage before ai-meta-kernel analysis

---

## 1. Objective

The purpose of triage is not to produce final analysis.

The purpose of triage is to:
1. suppress low-value noise,
2. preserve high-value official signals,
3. package candidate items into a clean ingestion bundle for ai-meta-kernel.

This layer must remain conservative and auditable.

---

## 2. Triage Priority Levels

- `P1`: must include in ingestion bundle and report candidate set
- `P2`: include in ingestion bundle as secondary candidate
- `P3`: retain for reference only
- `DROP`: exclude from ingestion bundle

---

## 3. Core Principle

Triage is rule-based first.

Do not attempt deep interpretation in this layer.
Do not infer market impact beyond simple tagging logic.
Do not replace ai-meta-kernel reasoning.

---

## 4. Positive Signals

An item should receive a higher preliminary priority if one or more of the following conditions are met.

### 4.1 Source Authority
- Source is `TIER_1`
- Source official_status is `official`

### 4.2 Policy Relevance
- Mentions policy change
- Mentions regulatory change
- Mentions rule proposal / final rule
- Mentions central bank decision or communication
- Mentions fiscal action or treasury action

### 4.3 Macro / Market Relevance
- Related to rates
- Related to inflation
- Related to labor market
- Related to growth / GDP
- Related to liquidity
- Related to FX
- Related to tariffs / trade restrictions
- Related to banking / insurance regulation
- Related to credit conditions
- Related to exchange operations or market structure

### 4.4 Continuity / Follow-up Relevance
- Matches active watchlist topic
- Appears to be a continuation of an already tracked event chain
- Has significant scheduled follow-up potential within 72 hours

---

## 5. Negative Signals

An item should receive a lower preliminary priority if one or more of the following conditions are met.

- Duplicate of an already preserved official source item
- Routine announcement with no policy, macro, market, or regulatory relevance
- Purely promotional or institutional branding content
- Region outside active run scope
- Media repetition of an official statement without material added value
- Commentary piece with weak sourcing and no new facts

---

## 6. Suggested Scoring Logic

This is a simple reference model for v0.1.

### 6.1 Positive Weights
- TIER_1 official source: +4
- TIER_2 mainstream financial media: +2
- Policy / regulation relevance: +3
- Rates / inflation / labor / liquidity / credit / FX relevance: +3
- Trade / tariff / fiscal relevance: +2
- Watchlist topic match: +2
- Ongoing event-chain continuity: +2

### 6.2 Negative Weights
- Clear duplicate: -4
- Routine / administrative content only: -3
- Promotional / branding content: -3
- Out-of-scope region: -3
- Commentary without primary facts: -2

---

## 7. Priority Mapping

Suggested mapping for v0.1:

- total score >= 7 → `P1`
- total score between 4 and 6 → `P2`
- total score between 1 and 3 → `P3`
- total score <= 0 → `DROP`

This mapping is provisional and may be recalibrated after retro review.

---

## 8. Mandatory Escalation Rules

Regardless of raw score, the item should be escalated to at least `P1` if:

1. it is a central bank rate decision or equivalent policy statement,
2. it is a major treasury / finance ministry announcement with macro significance,
3. it is an official inflation, labor, GDP, or comparable macro release,
4. it is a major regulatory enforcement / rule action affecting banking, insurance, credit, or market structure,
5. it is explicitly requested by operator watchlist.

---

## 9. Mandatory Suppression Rules

Regardless of raw score, the item should be set to `DROP` if:

1. it is not from the approved whitelist during a whitelist-only run,
2. it is empty, broken, or missing minimum metadata,
3. it is a near-identical duplicate already preserved in a stronger source,
4. it is irrelevant to the active region scope and has no cross-market significance.

---

## 10. Required Minimum Metadata

An item must not proceed beyond triage unless all of the following fields are present:

- `item_id`
- `source_id`
- `region`
- `published_at`
- `title`
- `canonical_url`
- `content_type`

If one or more required fields are missing, the item should be dropped or quarantined for manual review.

---

## 11. Output Expectations

The triage layer must output:

- `preliminary_priority`
- `topic_tags`
- `market_tags`
- `risk_tags`
- `dedup_group_id`
- optional `event_cluster_id`

This layer must not generate full narrative analysis.

---

## 12. Human Review Notes

Operator review can override:
- `P2` to `P1`
- `P1` to `P2`
- `P3` to `DROP`
- `DROP` to `P2` in exceptional cases

Every override should be logged for retrospective review.

---

## 13. Retro Calibration

After a sufficient number of daily and weekly runs, review:
- false positives,
- false negatives,
- duplicated event chains,
- over-selected routine items,
- missed high-signal items.

Adjust weights only after pattern evidence is accumulated.

Do not overfit triage rules to one unusual week.