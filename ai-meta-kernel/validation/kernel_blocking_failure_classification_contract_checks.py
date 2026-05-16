"""Standalone checks for blocking failure classification.

This helper exercises only the local pre-writer blocking failure classification
boundary. It is intentionally outside the main wrapper and does not implement
failure writing, write artifacts, unlock macro reporting, emit CLI behavior, or
execute handoff.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parents[2]
KERNEL_ROOT = REPO_ROOT / "ai-meta-kernel"

sys.path.insert(0, str(KERNEL_ROOT))

import file_exchange_adapter_scaffold as scaffold  # noqa: E402


ALLOWED_FAILURE_STAGES = [
    "reader",
    "envelope_validation",
    "intake_mapping",
    "runtime_invocation",
    "response_validation",
    "response_writer",
]

FORBIDDEN_CLASSIFIED_OUTPUT_FIELDS = {
    "failure_artifact_path",
    "response_artifact_path",
    "cli_success_signal",
    "report_eligibility",
    "macro_report_eligibility",
    "downstream_reporting_allowed",
    "actual_handoff",
    "handoff_marker",
}


def build_failure_source(stage: str) -> dict[str, Any]:
    return {
        "source_boundary": f"{stage}_boundary",
        "failure_stage": stage,
        "failure_code": f"{stage}_failed",
        "failure_message": f"{stage} failed before terminal writing",
    }


def assert_scaffold_error(label: str, callback: Callable[[], object]) -> None:
    try:
        callback()
    except scaffold.KernelFileExchangeAdapterScaffoldError:
        return
    raise AssertionError(f"{label} must fail closed with scaffold error")


def assert_classified_output(stage: str, classified: dict[str, Any]) -> None:
    expected_markers = {
        "failure_type": "kernel_blocking_failure",
        "classified_failure_type": "kernel_blocking_failure",
        "classified_failure_state": "classified_blocking_failure_pre_writer",
        "failure_stage": stage,
        "failure_code": f"{stage}_failed",
        "failure_message": f"{stage} failed before terminal writing",
        "source_boundary": f"{stage}_boundary",
        "is_blocking": True,
        "terminal_artifact_written": False,
        "response_artifact_written": False,
        "failure_artifact_written": False,
        "macro_report_unlock": False,
        "classification_stage": "blocking_failure_classified_pre_writer",
    }
    for field, expected in expected_markers.items():
        if classified.get(field) != expected:
            raise AssertionError(f"classified failure {field} should be {expected!r}")

    leaked = sorted(FORBIDDEN_CLASSIFIED_OUTPUT_FIELDS.intersection(classified))
    if leaked:
        raise AssertionError(f"classified failure contains forbidden fields: {leaked}")


def check_valid_stage_classification() -> None:
    for stage in ALLOWED_FAILURE_STAGES:
        classified = scaffold.classify_blocking_failure(build_failure_source(stage))
        if not isinstance(classified, dict):
            raise AssertionError("classified blocking failure must be a JSON object")
        assert_classified_output(stage, classified)


def check_fail_closed_inputs() -> None:
    assert_scaffold_error(
        "non-object failure source",
        lambda: scaffold.classify_blocking_failure(["not", "an", "object"]),  # type: ignore[arg-type]
    )

    missing_required = build_failure_source("reader")
    missing_required.pop("failure_code")
    assert_scaffold_error(
        "missing required failure source field",
        lambda: scaffold.classify_blocking_failure(missing_required),
    )

    unknown_stage = build_failure_source("reader")
    unknown_stage["failure_stage"] = "unknown_stage"
    assert_scaffold_error(
        "unknown failure_stage",
        lambda: scaffold.classify_blocking_failure(unknown_stage),
    )

    response_artifact_input = build_failure_source("reader")
    response_artifact_input["artifact_type"] = "kernel_response"
    assert_scaffold_error(
        "response artifact input",
        lambda: scaffold.classify_blocking_failure(response_artifact_input),
    )

    failure_artifact_input = build_failure_source("reader")
    failure_artifact_input["artifact_type"] = "kernel_exchange_failure"
    assert_scaffold_error(
        "failure artifact input",
        lambda: scaffold.classify_blocking_failure(failure_artifact_input),
    )

    for marker in (
        "terminal_artifact_written",
        "response_artifact_written",
        "failure_artifact_written",
        "macro_report_unlock",
    ):
        marked = build_failure_source("reader")
        marked[marker] = True
        assert_scaffold_error(
            f"{marker} true",
            lambda marked=marked: scaffold.classify_blocking_failure(marked),
        )


def check_failure_writer_remains_blocked() -> None:
    classified = scaffold.classify_blocking_failure(build_failure_source("reader"))

    try:
        scaffold.write_failure_artifact(classified, Path("local") / "kernel_failure.example.json")
    except NotImplementedError:
        pass
    else:
        raise AssertionError("failure writer must remain blocked")


def check_wrapper_remains_unchanged() -> None:
    wrapper_path = KERNEL_ROOT / "validation" / "run_all_kernel_local_checks.py"
    wrapper_text = wrapper_path.read_text(encoding="utf-8")
    helper_name = "kernel_blocking_failure_classification_contract_checks.py"
    if helper_name in wrapper_text:
        raise AssertionError("blocking failure classification helper must remain outside wrapper")


def main() -> None:
    check_valid_stage_classification()
    check_fail_closed_inputs()
    check_failure_writer_remains_blocked()
    check_wrapper_remains_unchanged()

    print("kernel-blocking-failure-classification-contract-checks-ok")


if __name__ == "__main__":
    main()
