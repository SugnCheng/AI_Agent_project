"""Standalone checks for the local terminal writer dry-run contract surface.

This helper exercises only the minimal local dry-run boundary. It remains
outside the main wrapper and does not add CLI, queue discovery, polling, retry,
cleanup, macro reporting, actual handoff, scheduler behavior, or live fetching.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any, Callable
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
KERNEL_ROOT = REPO_ROOT / "ai-meta-kernel"

sys.path.insert(0, str(KERNEL_ROOT))

import file_exchange_adapter_scaffold as scaffold  # noqa: E402


FORBIDDEN_RESULT_MARKERS = {
    "queue_discovery",
    "polling_behavior",
    "watcher_behavior",
    "retry_behavior",
    "backoff_behavior",
    "cleanup_behavior",
    "report_eligibility",
    "macro_report_eligibility",
    "downstream_reporting_allowed",
    "actual_handoff",
    "handoff_marker",
}


def build_validated_pre_writer_response() -> dict[str, Any]:
    candidate = {
        "candidate_type": "kernel_runtime_candidate_response",
        "candidate_version": "0.1.0",
        "candidate_state": "pre_writer_non_terminal",
        "invocation_stage": "kernel_runtime_invocation_candidate_only",
        "source_context": {
            "source_project": "macro-financial-intelligence-agent",
            "profile_id": "daily_us_core",
            "run_mode": "dry_run",
            "report_target": "daily_brief",
            "regions": ["US"],
        },
        "operator_request": "Prepare a local dry-run response candidate.",
        "evidence_context": {
            "evidence_bundle": {},
            "evidence_context": {},
        },
        "expectation_context": {},
        "deferred_behavior_context": [],
        "source_mapping_stage": "kernel_intake_context_pre_runtime",
        "terminal_artifact_written": False,
        "response_writer_called": False,
        "failure_writer_called": False,
        "macro_report_unlock": False,
    }
    return scaffold.validate_candidate_response(candidate)


def build_classified_failure() -> dict[str, Any]:
    source = {
        "source_boundary": "response_validation_boundary",
        "failure_stage": "response_validation",
        "failure_code": "dry_run_validation_blocked",
        "failure_message": "dry-run failure branch remains pre-writer",
    }
    return scaffold.classify_blocking_failure(source)


def assert_scaffold_error(label: str, callback: Callable[[], object]) -> None:
    try:
        callback()
    except scaffold.KernelFileExchangeAdapterScaffoldError:
        return
    raise AssertionError(f"{label} must fail closed with scaffold error")


def iter_nested_items(value: Any) -> Any:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key, nested
            yield from iter_nested_items(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_nested_items(nested)


def assert_no_forbidden_result_markers(result: dict[str, Any]) -> None:
    leaked = sorted(
        {
            key
            for key, _ in iter_nested_items(result)
            if key in FORBIDDEN_RESULT_MARKERS
        }
    )
    if leaked:
        raise AssertionError(f"dry-run result contains forbidden markers: {leaked}")


def check_successful_dry_run() -> None:
    response = build_validated_pre_writer_response()
    failure = build_classified_failure()

    with mock.patch.object(scaffold, "write_response_artifact") as mocked_response_writer:
        with mock.patch.object(scaffold, "write_failure_artifact") as mocked_failure_writer:
            result = scaffold.dry_run_terminal_writers(response, failure)

    if mocked_response_writer.called:
        raise AssertionError("dry-run must not call the real response writer")
    if mocked_failure_writer.called:
        raise AssertionError("dry-run must not call the real failure writer")

    if not isinstance(result, dict):
        raise AssertionError("dry-run result must be a JSON object")

    expected_markers = {
        "dry_run_type": "local_terminal_writer_dry_run",
        "dry_run_state": "completed_pre_orchestration",
        "response_path_checked": True,
        "failure_path_checked": True,
        "mutual_exclusivity_required": True,
        "dual_write_for_single_invocation_allowed": False,
        "macro_report_unlock": False,
        "cli_behavior_added": False,
        "actual_handoff_executed": False,
        "dry_run_stage": "terminal_writer_dry_run_minimal_local",
        "terminal_artifact_written": False,
    }
    for field, expected in expected_markers.items():
        if result.get(field) != expected:
            raise AssertionError(f"dry-run result {field} should be {expected!r}")

    response_candidate = result.get("response_artifact_candidate")
    failure_candidate = result.get("failure_artifact_candidate")
    if not isinstance(response_candidate, dict):
        raise AssertionError("response artifact candidate must be a JSON object")
    if not isinstance(failure_candidate, dict):
        raise AssertionError("failure artifact candidate must be a JSON object")

    if response_candidate.get("artifact_type") != "kernel_response":
        raise AssertionError("response artifact candidate must be marked kernel_response")
    if failure_candidate.get("artifact_type") != "kernel_exchange_failure":
        raise AssertionError("failure artifact candidate must be marked kernel_exchange_failure")

    if response_candidate.get("terminal_artifact_written") is not False:
        raise AssertionError("response candidate must remain unwritten in dry-run")
    if failure_candidate.get("terminal_artifact_written") is not False:
        raise AssertionError("failure candidate must remain unwritten in dry-run")

    if response_candidate.get("dry_run_branch_id") == failure_candidate.get("dry_run_branch_id"):
        raise AssertionError("response and failure dry-run branches must not share one invocation id")

    if "single_invocation_id" in response_candidate or "single_invocation_id" in failure_candidate:
        raise AssertionError("dry-run candidates must not bind both terminal artifacts to one invocation id")

    assert_no_forbidden_result_markers(result)


def check_fail_closed_inputs() -> None:
    response = build_validated_pre_writer_response()
    failure = build_classified_failure()

    assert_scaffold_error(
        "non-object response input",
        lambda: scaffold.dry_run_terminal_writers(["not", "an", "object"], failure),  # type: ignore[arg-type]
    )
    assert_scaffold_error(
        "non-object failure input",
        lambda: scaffold.dry_run_terminal_writers(response, ["not", "an", "object"]),  # type: ignore[arg-type]
    )

    malformed_response = dict(response)
    malformed_response.pop("validated_response_type")
    assert_scaffold_error(
        "malformed response input",
        lambda: scaffold.dry_run_terminal_writers(malformed_response, failure),
    )

    malformed_failure = dict(failure)
    malformed_failure.pop("classified_failure_type")
    assert_scaffold_error(
        "malformed failure input",
        lambda: scaffold.dry_run_terminal_writers(response, malformed_failure),
    )

    response_artifact = dict(response)
    response_artifact["artifact_type"] = "kernel_response"
    assert_scaffold_error(
        "response artifact input",
        lambda: scaffold.dry_run_terminal_writers(response_artifact, failure),
    )

    failure_artifact = dict(failure)
    failure_artifact["artifact_type"] = "kernel_exchange_failure"
    assert_scaffold_error(
        "failure artifact input",
        lambda: scaffold.dry_run_terminal_writers(response, failure_artifact),
    )

    macro_unlocked = dict(response)
    macro_unlocked["macro_report_unlock"] = True
    assert_scaffold_error(
        "macro_report_unlock true",
        lambda: scaffold.dry_run_terminal_writers(macro_unlocked, failure),
    )

    terminal_written = dict(response)
    terminal_written["terminal_artifact_written"] = True
    assert_scaffold_error(
        "terminal_artifact_written true",
        lambda: scaffold.dry_run_terminal_writers(terminal_written, failure),
    )

    cli_marker = dict(response)
    cli_marker["cli_success_signal"] = "not-allowed"
    assert_scaffold_error(
        "CLI marker",
        lambda: scaffold.dry_run_terminal_writers(cli_marker, failure),
    )

    handoff_marker = dict(failure)
    handoff_marker["actual_handoff_executed"] = True
    assert_scaffold_error(
        "actual handoff marker",
        lambda: scaffold.dry_run_terminal_writers(response, handoff_marker),
    )

    report_marker = dict(failure)
    report_marker["report_eligibility"] = True
    assert_scaffold_error(
        "report eligibility marker",
        lambda: scaffold.dry_run_terminal_writers(response, report_marker),
    )


def check_wrapper_remains_unchanged() -> None:
    wrapper_path = KERNEL_ROOT / "validation" / "run_all_kernel_local_checks.py"
    wrapper_text = wrapper_path.read_text(encoding="utf-8")
    helper_name = "kernel_terminal_writer_dry_run_contract_checks.py"
    if helper_name in wrapper_text:
        raise AssertionError("terminal writer dry-run helper must remain outside wrapper")


def main() -> None:
    check_successful_dry_run()
    check_fail_closed_inputs()
    check_wrapper_remains_unchanged()

    print("kernel-terminal-writer-dry-run-contract-checks-ok")


if __name__ == "__main__":
    main()
