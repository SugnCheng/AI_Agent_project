"""Static checks for kernel-side file exchange fixtures.

This helper validates only committed fixture files. It does not invoke kernel
runtime, read generated exchange artifacts, write artifacts, fetch sources,
compose reports, or run scheduler behavior.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover - developer environment guard.
    raise SystemExit(
        "jsonschema is required for TASK_OBJECT_SCHEMA validation. "
        "Install the approved project dependencies before running this check."
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[2]
KERNEL_ROOT = REPO_ROOT / "ai-meta-kernel"
FIXTURE_ROOT = KERNEL_ROOT / "examples" / "file-exchange"

ENVELOPE_FIXTURE = (
    FIXTURE_ROOT
    / "envelopes"
    / "daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.example.json"
)
RESPONSE_FIXTURE = (
    FIXTURE_ROOT
    / "responses"
    / "daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_response.example.json"
)
FAILURE_FIXTURE = (
    FIXTURE_ROOT
    / "failures"
    / "daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_failure.example.json"
)
TASK_OBJECT_SCHEMA = KERNEL_ROOT / "meta-layer" / "TASK_OBJECT_SCHEMA.json"

ENVELOPE_REQUIRED_FIELDS = {
    "envelope_type",
    "envelope_version",
    "source_project",
    "profile_id",
    "run_mode",
    "report_target",
    "regions",
    "operator_intent",
    "evidence_bundle",
    "evidence_context",
    "kernel_task_object_expectation",
    "deferred_runtime_behavior",
}

CANONICAL_TASK_OBJECT_TOP_LEVEL_FIELDS = {
    "schema_version",
    "task_id",
    "raw_request",
    "kernel_stage",
    "framed_objective",
    "task_classification",
    "risk_profile",
    "triggered_habits",
    "structural_decomposition",
    "required_checks",
    "status_flags",
    "verification_plan",
    "challenge_loop",
    "downstream_recommendation",
    "handoff",
}

RESPONSE_REQUIRED_TOP_LEVEL_FIELDS = {
    "raw_request",
    "framed_objective",
    "task_classification",
    "risk_profile",
    "triggered_habits",
    "structural_decomposition",
    "required_checks",
    "status_flags",
    "verification_plan",
    "challenge_loop",
    "downstream_recommendation",
    "handoff",
}

FAILURE_REQUIRED_FIELDS = {
    "artifact_type",
    "artifact_version",
    "source_project",
    "profile_id",
    "run_mode",
    "report_target",
    "regions",
    "envelope_artifact_path",
    "failure_stage",
    "failure_reason",
    "blocking",
    "created_at",
}

ALLOWED_FAILURE_STAGES = {
    "pre_invoke",
    "invoke",
    "response_parse",
    "response_schema_validation",
    "response_state_validation",
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"missing fixture: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise AssertionError(f"fixture must be a JSON object: {path}")

    return data


def require_fields(data: dict[str, Any], required: set[str], label: str) -> None:
    missing = sorted(required.difference(data))
    if missing:
        raise AssertionError(f"{label} missing required fields: {missing}")


def validate_envelope_fixture() -> None:
    envelope = load_json(ENVELOPE_FIXTURE)
    require_fields(envelope, ENVELOPE_REQUIRED_FIELDS, "envelope fixture")

    expected_values = {
        "envelope_type": "kernel_input_envelope",
        "source_project": "macro-financial-intelligence-agent",
        "profile_id": "daily_us_core",
        "run_mode": "daily_brief_run",
        "report_target": "daily_brief",
    }
    for field, expected in expected_values.items():
        actual = envelope.get(field)
        if actual != expected:
            raise AssertionError(f"envelope fixture {field} expected {expected!r}, got {actual!r}")

    if envelope.get("regions") != ["US"]:
        raise AssertionError("envelope fixture regions must be ['US']")

    if not envelope.get("operator_intent"):
        raise AssertionError("envelope fixture operator_intent must be non-empty")

    leaked_fields = sorted(CANONICAL_TASK_OBJECT_TOP_LEVEL_FIELDS.intersection(envelope))
    if leaked_fields:
        raise AssertionError(
            "envelope fixture must not contain canonical task object fields: "
            f"{leaked_fields}"
        )

    expectation = envelope.get("kernel_task_object_expectation")
    if not isinstance(expectation, dict):
        raise AssertionError("envelope fixture kernel_task_object_expectation must be an object")


def validate_response_fixture() -> None:
    schema = load_json(TASK_OBJECT_SCHEMA)
    response = load_json(RESPONSE_FIXTURE)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(response), key=lambda error: list(error.path))
    if errors:
        details = [
            f"{list(error.path) or '<root>'}: {error.message}"
            for error in errors
        ]
        raise AssertionError("response fixture schema validation failed: " + "; ".join(details))

    if response.get("schema_version") != "0.2.0":
        raise AssertionError("response fixture schema_version must be '0.2.0'")

    require_fields(response, RESPONSE_REQUIRED_TOP_LEVEL_FIELDS, "response fixture")

    triggered_habits = response.get("triggered_habits")
    if not isinstance(triggered_habits, list) or not any(
        habit.get("role") == "primary" for habit in triggered_habits if isinstance(habit, dict)
    ):
        raise AssertionError("response fixture must include at least one primary triggered habit")

    mode = response.get("downstream_recommendation", {}).get("mode")
    allowed_modes = {"standard_handoff", "restricted_handoff", "do_not_handoff"}
    if mode not in allowed_modes:
        raise AssertionError(f"response fixture downstream mode is invalid: {mode!r}")


def validate_failure_fixture() -> None:
    failure = load_json(FAILURE_FIXTURE)
    require_fields(failure, FAILURE_REQUIRED_FIELDS, "failure fixture")

    expected_values = {
        "artifact_type": "kernel_exchange_failure",
        "artifact_version": "0.1.0",
        "source_project": "ai-meta-kernel",
        "profile_id": "daily_us_core",
        "run_mode": "daily_brief_run",
        "report_target": "daily_brief",
    }
    for field, expected in expected_values.items():
        actual = failure.get(field)
        if actual != expected:
            raise AssertionError(f"failure fixture {field} expected {expected!r}, got {actual!r}")

    if failure.get("regions") != ["US"]:
        raise AssertionError("failure fixture regions must be ['US']")

    if failure.get("blocking") is not True:
        raise AssertionError("failure fixture blocking must be true")

    if not failure.get("failure_reason"):
        raise AssertionError("failure fixture failure_reason must be non-empty")

    failure_stage = failure.get("failure_stage")
    if failure_stage not in ALLOWED_FAILURE_STAGES:
        raise AssertionError(f"failure fixture failure_stage is invalid: {failure_stage!r}")

    leaked_fields = sorted(CANONICAL_TASK_OBJECT_TOP_LEVEL_FIELDS.intersection(failure))
    if leaked_fields:
        raise AssertionError(
            "failure fixture must not contain canonical task object fields: "
            f"{leaked_fields}"
        )


def main() -> None:
    validate_envelope_fixture()
    validate_response_fixture()
    validate_failure_fixture()
    print("kernel-file-exchange-fixture-checks-ok")


if __name__ == "__main__":
    main()
