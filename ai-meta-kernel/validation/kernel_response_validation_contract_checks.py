"""Local checks for the minimal response validation contract surface.

This helper exercises only the current candidate-response validation boundary.
It does not validate terminal TASK_OBJECT_SCHEMA output, write artifacts,
include itself in the main wrapper, fetch sources, compose reports, run
scheduler behavior, or mutate fixtures.
"""

from __future__ import annotations

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

FORBIDDEN_VALIDATED_OUTPUT_FIELDS = {
    "response_artifact_path",
    "failure_artifact_path",
    "report_eligibility",
    "macro_report_eligibility",
    "downstream_reporting_allowed",
    "written_response_artifact",
    "written_failure_artifact",
    "cli_success_signal",
    "external_service_result",
}


def build_valid_candidate_response() -> dict[str, Any]:
    envelope = scaffold.read_envelope_artifact(ENVELOPE_FIXTURE)
    validated_envelope = scaffold.validate_envelope_intake(envelope)
    intake = scaffold.prepare_kernel_intake(validated_envelope)
    return scaffold.invoke_kernel_runtime(intake)


def assert_scaffold_error(label: str, callback: Callable[[], object]) -> None:
    try:
        callback()
    except scaffold.KernelFileExchangeAdapterScaffoldError:
        return
    raise AssertionError(f"{label} must fail closed with scaffold error")


def assert_no_forbidden_fields(label: str, value: dict[str, Any]) -> None:
    leaked = sorted(FORBIDDEN_VALIDATED_OUTPUT_FIELDS.intersection(value))
    if leaked:
        raise AssertionError(f"{label} contains forbidden terminal fields: {leaked}")


def check_successful_response_validation() -> dict[str, Any]:
    candidate = build_valid_candidate_response()
    validated = scaffold.validate_candidate_response(candidate)

    if not isinstance(validated, dict):
        raise AssertionError("validated response must be a JSON object")

    expected_markers = {
        "validated_response_type": "kernel_candidate_response_validation",
        "validated_response_state": "validated_pre_writer_non_terminal",
        "response_writer_allowed": False,
        "failure_writer_allowed": False,
        "macro_report_unlock": False,
        "validation_stage": "candidate_response_validated_pre_writer",
    }
    for field, expected in expected_markers.items():
        if validated.get(field) != expected:
            raise AssertionError(f"validated response {field} should be {expected!r}")

    if validated.get("source_candidate") != candidate:
        raise AssertionError("validated response should preserve the source candidate")

    if validated["source_candidate"] is candidate:
        raise AssertionError("validated response should copy the source candidate")

    assert_no_forbidden_fields("validated response", validated)
    assert_no_forbidden_fields("source candidate", validated["source_candidate"])

    return validated


def check_validation_failures() -> None:
    candidate = build_valid_candidate_response()

    assert_scaffold_error(
        "non-object response validation input",
        lambda: scaffold.validate_candidate_response(["not", "an", "object"]),  # type: ignore[arg-type]
    )

    malformed = dict(candidate)
    malformed.pop("candidate_type")
    assert_scaffold_error(
        "malformed candidate response",
        lambda: scaffold.validate_candidate_response(malformed),
    )

    response_artifact = dict(candidate)
    response_artifact["artifact_type"] = "kernel_response"
    assert_scaffold_error(
        "terminal response artifact as validation input",
        lambda: scaffold.validate_candidate_response(response_artifact),
    )

    failure_artifact = dict(candidate)
    failure_artifact["artifact_type"] = "kernel_exchange_failure"
    assert_scaffold_error(
        "failure artifact as validation input",
        lambda: scaffold.validate_candidate_response(failure_artifact),
    )

    terminal_candidate = dict(candidate)
    terminal_candidate["terminal_artifact_written"] = True
    assert_scaffold_error(
        "terminal_artifact_written true",
        lambda: scaffold.validate_candidate_response(terminal_candidate),
    )

    response_writer_candidate = dict(candidate)
    response_writer_candidate["response_writer_called"] = True
    assert_scaffold_error(
        "response_writer_called true",
        lambda: scaffold.validate_candidate_response(response_writer_candidate),
    )

    failure_writer_candidate = dict(candidate)
    failure_writer_candidate["failure_writer_called"] = True
    assert_scaffold_error(
        "failure_writer_called true",
        lambda: scaffold.validate_candidate_response(failure_writer_candidate),
    )

    report_unlock_candidate = dict(candidate)
    report_unlock_candidate["macro_report_unlock"] = True
    assert_scaffold_error(
        "macro_report_unlock true",
        lambda: scaffold.validate_candidate_response(report_unlock_candidate),
    )

    for field in sorted(FORBIDDEN_VALIDATED_OUTPUT_FIELDS):
        candidate_with_forbidden_field = dict(candidate)
        candidate_with_forbidden_field[field] = "not allowed"
        assert_scaffold_error(
            f"candidate with forbidden field {field}",
            lambda candidate_with_forbidden_field=candidate_with_forbidden_field: scaffold.validate_candidate_response(
                candidate_with_forbidden_field
            ),
        )


def check_stop_before_writers() -> None:
    candidate = build_valid_candidate_response()
    with mock.patch.object(scaffold, "write_response_artifact") as mocked_response_writer:
        with mock.patch.object(scaffold, "write_failure_artifact") as mocked_failure_writer:
            scaffold.validate_candidate_response(candidate)

    if mocked_response_writer.called:
        raise AssertionError("validate_candidate_response must not call response writer")

    if mocked_failure_writer.called:
        raise AssertionError("validate_candidate_response must not call failure writer")


def check_reader_mapper_invocation_and_wrapper_not_broadened() -> None:
    envelope = scaffold.read_envelope_artifact(ENVELOPE_FIXTURE)
    intake = scaffold.prepare_kernel_intake(envelope)
    candidate = scaffold.invoke_kernel_runtime(intake)

    if set(intake) != scaffold.KERNEL_INTAKE_CONTEXT_REQUIRED_FIELDS:
        raise AssertionError("prepare_kernel_intake should remain context-only")

    if candidate.get("candidate_state") != "pre_writer_non_terminal":
        raise AssertionError("invoke_kernel_runtime should remain candidate-only")

    assert_scaffold_error(
        "reader still rejects directory input",
        lambda: scaffold.read_envelope_artifact(KERNEL_ROOT),
    )

    wrapper_path = KERNEL_ROOT / "validation" / "run_all_kernel_local_checks.py"
    wrapper_text = wrapper_path.read_text(encoding="utf-8")
    if "kernel_response_validation_contract_checks.py" in wrapper_text:
        raise AssertionError("response validation helper must remain outside wrapper")


def main() -> None:
    check_successful_response_validation()
    check_validation_failures()
    check_stop_before_writers()
    check_reader_mapper_invocation_and_wrapper_not_broadened()

    print("kernel-response-validation-contract-checks-ok")


if __name__ == "__main__":
    main()
