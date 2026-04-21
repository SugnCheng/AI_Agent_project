# REVIEW_WORKFLOW

## Document Status
- version: 0.1
- owner: macro-financial-intelligence-agent
- purpose: define operator review and revision workflow

---

## 1. Objective

The review layer ensures that macro-financial-intelligence-agent remains a human-supervised intelligence system rather than an unsupervised summarization engine.

Review serves five purposes:
1. validate signal quality,
2. suppress weak or noisy outputs,
3. upgrade important outputs,
4. capture operator preferences,
5. improve future triage and reporting quality.

---

## 2. Review Scope

The operator may review:

- ingestion bundle outputs,
- daily briefs,
- weekly intelligence reports,
- special event memos,
- source registry adjustments,
- triage priority overrides.

---

## 3. Review Principles

### 3.1 Human Override Is Explicit
The operator may override automated triage and report prioritization.

### 3.2 Review Must Be Logged
Material review actions must be recorded for retrospective analysis.

### 3.3 Review Does Not Rewrite Source Facts
Operator review may change priority, focus, and follow-up direction, but should not overwrite raw source traceability.

### 3.4 Review Should Improve the System
Review is not only for correction.
It is also for preference capture and future governance.

---

## 4. Review Actions

Supported review actions for v0.1:

- `keep`
- `drop`
- `upgrade`
- `downgrade`
- `request_follow_up`
- `increase_topic_weight`
- `decrease_topic_weight`
- `approve_source`
- `disable_source`
- `annotate`

---

## 5. Review Targets

### 5.1 Item-Level Review
Examples:
- upgrade a `P2` item to `P1`
- drop a repetitive media item
- annotate an item as requiring future tracking

### 5.2 Report-Level Review
Examples:
- mark a daily brief as acceptable
- request stronger synthesis in weekly report
- escalate a daily item into a special event memo

### 5.3 Source-Level Review
Examples:
- temporarily suppress a noisy source
- add an approved new whitelist source
- reduce or increase source priority

---

## 6. Suggested Workflow

### Step 1: Read the Output
Operator reads the generated daily / weekly / event output.

### Step 2: Identify Weak or Strong Signals
Operator marks:
- which items should stay,
- which items should drop,
- which items deserve more emphasis.

### Step 3: Record Structured Actions
Operator records structured review actions rather than only free-form comments.

### Step 4: Update Review Queue
Items requiring follow-up or escalation are inserted into the review queue.

### Step 5: Feed Retro Notes
Important recurring issues are logged for triage or reporting recalibration.

---

## 7. Review Output Contract

Suggested review object:

```json
{
  "review_id": "review_2026_04_15_daily_us_core",
  "report_id": "daily_brief_2026_04_15_us",
  "reviewed_at": "2026-04-15T10:30:00+08:00",
  "review_actions": [
    {
      "target_type": "item",
      "target_id": "item_001",
      "action": "upgrade",
      "notes": "Official item should be emphasized more strongly."
    },
    {
      "target_type": "topic",
      "target_id": "tariffs",
      "action": "increase_topic_weight",
      "notes": "This topic likely remains active next week."
    }
  ],
  "operator_notes": "Need tighter signal-vs-noise separation tomorrow."
}
```

---

## 8. Upgrade Paths

### 8.1 Daily → Special Event Memo
A daily brief item may be upgraded to a special event memo if:
- the event has unusually high macro significance,
- the event has multi-asset transmission relevance,
- the event remains highly uncertain and needs scenario framing.

### 8.2 Weekly → Follow-Up Memo
A weekly report section may trigger a follow-up memo if:
- an ongoing event chain becomes central,
- a policy narrative is evolving rapidly,
- cross-market transmission becomes non-trivial.

---

## 9. Source Governance Hooks

Review may trigger:
- source enable / disable changes,
- source priority adjustments,
- requests for whitelist expansion,
- temporary suspension of weak sources.

All such changes should be implemented through configuration changes, not ad hoc hidden logic.

---

## 10. Retro and Calibration

Review findings should be linked to:
- `validation/RETRO_LOG.md`
- triage false positives,
- triage false negatives,
- over-selected routine announcements,
- under-explained high-signal items.

Do not recalibrate the whole system based on one noisy day.

---

## 11. v0.1 Non-goals

Out of scope for v0.1:
- fully automated self-learning from review without explicit governance,
- hidden weight adaptation,
- operator-free approval chains,
- auto-expansion of sources from review comments alone.

This remains a governed human-in-the-loop system.