# Sample Kernel Inputs

These are simplified handoff snippets that the Macro-Financial Intelligence Agent should be able to consume or reject.

## K01: Acceptable Restricted Handoff

```json
{
  "framed_objective": {
    "core_goal": "Produce a source-aware macro-financial risk brief.",
    "scope": ["Taiwan", "Japan", "United States", "Europe"],
    "non_goals": ["direct trading advice"]
  },
  "task_classification": {
    "primary_type": "analysis",
    "secondary_types": ["information"]
  },
  "risk_profile": {
    "overall_level": "high",
    "categories": ["financial", "time_sensitive"],
    "confidence_ceiling": "medium"
  },
  "triggered_habits": [
    {"habit_id": "H1", "role": "primary", "reason": "External current claims.", "required": true},
    {"habit_id": "H2", "role": "support", "reason": "Competing interpretations possible.", "required": true}
  ],
  "required_checks": {
    "must_verify": ["source timestamp", "official policy source"],
    "must_challenge": ["alternative_explanation_check", "overconfidence_check"],
    "must_disclose_uncertainty": ["market implications are provisional"],
    "must_align_with_user": []
  },
  "status_flags": ["ready_for_handoff", "needs_verification"],
  "downstream_recommendation": {
    "agent_type": "macro-financial-intelligence",
    "mode": "restricted_handoff",
    "output_format": "research_brief"
  }
}
```

Expected agent behavior:

- accept as restricted handoff;
- verify sources before strong claims;
- produce research brief outline, not trading advice.

## K02: Return-To-Kernel Handoff

```json
{
  "framed_objective": {
    "core_goal": "",
    "scope": [],
    "non_goals": []
  },
  "status_flags": ["needs_user_clarification"],
  "downstream_recommendation": {
    "agent_type": "macro-financial-intelligence",
    "mode": "do_not_handoff",
    "output_format": "none"
  }
}
```

Expected agent behavior:

- reject handoff;
- request kernel reframe or user clarification.
