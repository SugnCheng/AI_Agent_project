# Verification Policy

Source of truth: `../../META_LAYER_MASTER_SPEC.md`.

## Policy Intent

Verification is a gate for factual reliability. It must be planned before downstream agents rely on unstable or high-stakes facts.

## Mandatory Verification Cases

Verification is mandatory or must be explicitly flagged when a task involves:

- recent or unstable information;
- numbers, dates, prices, law, regulation, policy, market-sensitive facts, or entity identities;
- medical, legal, investment, safety, security, privacy, or major financial decisions;
- claims from third parties or media;
- recommendations that depend on factual correctness.

## Priority Levels

- `critical`: recommendation cannot be unrestricted without verification.
- `important`: output may proceed as provisional or conditional with uncertainty disclosed.
- `optional`: verification would improve quality but is not required for handoff.

## Verification Object Types

- fact verification
- source verification
- number verification
- date/time verification
- rule/policy verification
- identity/entity verification
- citation audit

## Failure Handling

If required verification cannot be completed:

- do not imply confirmation;
- lower confidence;
- add `needs_verification`;
- restrict handoff or output;
- list what remains to verify.

## Handoff Requirement

If the downstream agent must verify something, write it explicitly into `required_checks.must_verify`.
