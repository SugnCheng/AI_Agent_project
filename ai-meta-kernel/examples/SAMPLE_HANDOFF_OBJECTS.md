# Sample Handoff Objects

## Macro-Financial Restricted Handoff

```json
{
  "downstream_recommendation": {
    "agent_type": "macro-financial-intelligence",
    "mode": "restricted_handoff",
    "output_format": "research_brief"
  },
  "required_checks": {
    "must_verify": ["publication time", "official policy source"],
    "must_challenge": ["alternative_explanation_check", "overconfidence_check"],
    "must_disclose_uncertainty": ["market implication is provisional"],
    "must_align_with_user": []
  }
}
```
