"""Local checks for the minimal runtime invocation contract surface.

This helper exercises only the current candidate-only invocation boundary. It
does not broaden reader behavior, broaden intake mapping, validate terminal
responses, write response/failure artifacts, fetch sources, compose reports,
run scheduler behavior, or mutate fixtures.
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

FORBIDDEN_CANDIDATE_FIELDS = {
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


def load_fixture_envelope() -> dict[str, Any]:
    with ENVELOPE_FIXTURE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise AssertionError("envelope fixture must be a JSON object")
    return data


def build_valid_intake_context() -> dict[str, Any]:
    envelope = scaffold.read_envelope_artifact(ENVELOPE_FIXTURE)
    validated = scaffold.validate_envelope_intake(envelope)
    return scaffold.prepare_kernel_intake(validated)


def assert_scaffold_error(label: str, callback: Callable[[], object]) -> None:
    try:
        callback()
    except scaffold.KernelFileExchangeAdapterScaffoldError:
        return
    raise AssertionError(f"{label} must fail closed with scaffold error")


def check_successful_invocation() -> dict[str, Any]:
    context = build_valid_intake_context()
    candidate = scaffold.invoke_kernel_runtime(context)

    if not isinstance(candidate, dict):
        raise AssertionError("candidate response must be a JSON object")

    expected_markers = {
        "candidate_type": "kernel_runtime_candidate_response",
        "candidate_state": "pre_writer_non_terminal",
        "terminal_artifact_written": False,
        "response_writer_called": False,
        "failure_writer_called": False,
        "macro_report_unlock": False,
    }
    for field, expected in expected_markers.items():
        if candidate.get(field) != expected:
            raise AssertionError(f"candidate {field} should be {expected!r}")

    leaked = sorted(FORBIDDEN_CANDIDATE_FIELDS.intersection(candidate))
    if leaked:
        raise AssertionError(f"candidate contains forbidden terminal fields: {leaked}")

    if candidate.get("source_context") != context["source_context"]:
        raise AssertionError("candidate should preserve source_context")

    if candidate.get("operator_request") != context["operator_request"]:
        raise AssertionError("candidate should preserve operator_request")

    if candidate.get("evidence_context") != context["evidence_context"]:
        raise AssertionError("candidate should preserve evidence_context")

    if candidate.get("source_mapping_stage") != "kernel_intake_context_pre_runtime":
        raise AssertionError("candidate should preserve pre-runtime mapping stage")

    return candidate


def check_invocation_failures() -> None:
    envelope = load_fixture_envelope()
    context = build_valid_intake_context()

    assert_scaffold_error(
        "non-object invocation input",
        lambda: scaffold.invoke_kernel_runtime(["not", "an", "object"]),  # type: ignore[arg-type]
    )

    malformed = dict(context)
    malformed.pop("operator_request")
    assert_scaffold_error(
        "malformed intake context",
        lambda: scaffold.invoke_kernel_runtime(malformed),
    )

    assert_scaffold_error(
        "raw envelope as invocation input",
        lambda: scaffold.invoke_kernel_runtime(envelope),
    )

    canonical_task = dict(context)
    canonical_task["framed_objective"] = {"summary": "not allowed"}
    assert_scaffold_error(
        "canonical task object as invocation input",
        lambda: scaffold.invoke_kernel_runtime(canonical_task),
    )

    response_artifact = dict(context)
    response_artifact["artifact_type"] = "kernel_response"
    assert_scaffold_error(
        "response artifact as invocation input",
        lambda: scaffold.invoke_kernel_runtime(response_artifact),
    )

    failure_artifact = dict(context)
    failure_artifact["artifact_type"] = "kernel_exchange_failure"
    assert_scaffold_error(
        "failure artifact as invocation input",
        lambda: scaffold.invoke_kernel_runtime(failure_artifact),
    )


def check_stop_before_writers() -> None:
    context = build_valid_intake_context()
    with mock.patch.object(scaffold, "write_response_artifact") as mocked_response_writer:
        with mock.patch.object(scaffold, "write_failure_artifact") as mocked_failure_writer:
            scaffold.invoke_kernel_runtime(context)

    if mocked_response_writer.called:
        raise AssertionError("invoke_kernel_runtime must not call response writer")

    if mocked_failure_writer.called:
        raise AssertionError("invoke_kernel_runtime must not call failure writer")


def check_reader_and_mapper_not_broadened() -> None:
    envelope = scaffold.read_envelope_artifact(ENVELOPE_FIXTURE)
    context = scaffold.prepare_kernel_intake(envelope)

    if set(context) != scaffold.KERNEL_INTAKE_CONTEXT_REQUIRED_FIELDS:
        raise AssertionError("prepare_kernel_intake should remain context-only")

    assert_scaffold_error(
        "reader still rejects directory input",
        lambda: scaffold.read_envelope_artifact(KERNEL_ROOT),
    )


def main() -> None:
    check_successful_invocation()
    check_invocation_failures()
    check_stop_before_writers()
    check_reader_and_mapper_not_broadened()

    print("kernel-runtime-invocation-contract-checks-ok")


if __name__ == "__main__":
    main()
