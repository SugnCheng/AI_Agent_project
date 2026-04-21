# Ingestion Workflow

## Document Role

This is a high-level ingestion workflow overview.

The operational bundle contract for v0.1 is:
- `bundles/schemas/INGESTION_BUNDLE.schema.json`

If this workflow summary conflicts with the schema, the schema takes precedence for field names, required fields, and bundle structure.

## Purpose

Collect source material under the constraints emitted by the Meta-Layer handoff.

## Steps

1. Read the kernel handoff.
2. Confirm jurisdiction, time window, topics, and verification requirements.
3. Collect sources using the source policy.
4. Capture source metadata: title, publisher, timestamp, URL/path, jurisdiction, and source tier.
5. Separate raw facts from commentary.
6. Return to kernel if scope or verification requirements are not executable.
