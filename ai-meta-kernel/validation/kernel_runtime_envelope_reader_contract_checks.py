"""Local checks for the future runtime envelope reader contract surface.

This helper exercises only the current scaffold reader and intake guardrails.
It does not create runtime artifacts, discover runtime queues, invoke kernel
runtime, prepare intake, write artifacts, fetch sources, compose reports, or
run scheduler behavior.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Callable
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
KERNEL_ROOT = REPO_ROOT / "ai-meta-kernel"
FIXTURE_ROOT = KERNEL_ROOT / "examples" / "file-exchange"

sys.path.insert(0, str(KERNEL_ROOT))

import file_exchange_adapter_scaffold as scaffold  # noqa: E402


ENVELOPE_FIXTURE = (
    FIXTURE_ROOT
    / "envelopes"
    / "daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.example.json"
)


def load_fixture_envelope() -> dict[str, Any]:
    with ENVELOPE_FIXTURE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise AssertionError("envelope fixture must be a JSON object")
    return data


def assert_scaffold_error(label: str, callback: Callable[[], object]) -> None:
    try:
        callback()
    except scaffold.KernelFileExchangeAdapterScaffoldError:
        return
    raise AssertionError(f"{label} must fail closed with scaffold error")


def assert_not_implemented(label: str, callback: Callable[[], object]) -> None:
    try:
        callback()
    except NotImplementedError:
        return
    raise AssertionError(f"{label} must remain blocked with NotImplementedError")


def check_successful_reader_output() -> dict[str, Any]:
    read_envelope = scaffold.read_envelope_artifact(ENVELOPE_FIXTURE)
    validated = scaffold.validate_envelope_intake(read_envelope)

    if validated is not read_envelope:
        raise AssertionError("reader validation should return the original envelope object")

    forbidden_fields = scaffold.CANONICAL_TASK_OBJECT_TOP_LEVEL_FIELDS.intersection(validated)
    if forbidden_fields:
        raise AssertionError(
            "reader output must not contain canonical task object fields: "
            f"{sorted(forbidden_fields)}"
        )

    return validated


def check_reader_failures() -> None:
    envelope = load_fixture_envelope()

    missing_path = KERNEL_ROOT / "validation" / ".missing-runtime-envelope-reader-input.json"
    assert_scaffold_error(
        "missing envelope path",
        lambda: scaffold.read_envelope_artifact(missing_path),
    )

    assert_scaffold_error(
        "directory envelope path",
        lambda: scaffold.read_envelope_artifact(KERNEL_ROOT),
    )

    assert_scaffold_error(
        "invalid JSON envelope",
        lambda: scaffold.read_envelope_artifact(KERNEL_ROOT / "AGENTS.md"),
    )

    assert_scaffold_error(
        "non-object envelope",
        lambda: read_envelope_with_mocked_json(["not", "an", "object"]),
    )

    missing_field = dict(envelope)
    missing_field.pop("operator_intent")
    assert_scaffold_error(
        "missing required envelope field",
        lambda: scaffold.validate_envelope_intake(missing_field),
    )

    wrong_type = dict(envelope)
    wrong_type["envelope_type"] = "kernel_response"
    assert_scaffold_error(
        "wrong artifact type",
        lambda: scaffold.validate_envelope_intake(wrong_type),
    )

    response_artifact = dict(envelope)
    response_artifact["artifact_type"] = "kernel_response"
    assert_scaffold_error(
        "response artifact as envelope input",
        lambda: scaffold.validate_envelope_intake(response_artifact),
    )

    failure_artifact = dict(envelope)
    failure_artifact["artifact_type"] = "kernel_exchange_failure"
    assert_scaffold_error(
        "failure artifact as envelope input",
        lambda: scaffold.validate_envelope_intake(failure_artifact),
    )

    leaked_task_field = dict(envelope)
    leaked_task_field["framed_objective"] = {"summary": "not allowed"}
    assert_scaffold_error(
        "canonical task field leakage",
        lambda: scaffold.validate_envelope_intake(leaked_task_field),
    )


def read_envelope_with_mocked_json(value: Any) -> dict[str, Any]:
    with mock.patch.object(scaffold.json, "load", return_value=value):
        return scaffold.read_envelope_artifact(ENVELOPE_FIXTURE)


def check_stop_before_intake(envelope: dict[str, Any]) -> None:
    assert_not_implemented(
        "prepare_kernel_intake",
        lambda: scaffold.prepare_kernel_intake(envelope),
    )
    assert_not_implemented(
        "invoke_kernel_runtime",
        lambda: scaffold.invoke_kernel_runtime({"placeholder": "kernel_intake"}),
    )


def main() -> None:
    envelope = check_successful_reader_output()
    check_reader_failures()
    check_stop_before_intake(envelope)

    print("kernel-runtime-envelope-reader-contract-checks-ok")


if __name__ == "__main__":
    main()
