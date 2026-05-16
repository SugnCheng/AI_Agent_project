"""Standalone checks for the minimal local invocation contract surface.

This helper exercises only the bounded local invocation boundary. It remains
outside the main wrapper and does not add CLI, queue discovery, polling, retry,
cleanup, macro reporting, actual handoff, scheduler behavior, live fetching,
or report composition.
"""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path
import sys
from typing import Any, Callable
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
KERNEL_ROOT = REPO_ROOT / "ai-meta-kernel"
FIXTURE_ROOT = KERNEL_ROOT / "examples" / "file-exchange"
ENVELOPE_FIXTURE = (
    FIXTURE_ROOT
    / "envelopes"
    / "daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.example.json"
)

sys.path.insert(0, str(KERNEL_ROOT))

import file_exchange_adapter_scaffold as scaffold  # noqa: E402


REQUIRED_RESULT_FIELDS = {
    "invocation_type",
    "invocation_state",
    "invocation_stage",
    "source_envelope_path",
    "selected_terminal_path",
    "response_artifact_path",
    "failure_artifact_path",
    "terminal_artifact_written",
    "response_writer_called",
    "failure_writer_called",
    "macro_report_unlock",
    "actual_handoff_executed",
    "cli_behavior_added",
}

FORBIDDEN_OPERATIONAL_MARKERS = {
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
    "cli_success_signal",
    "external_service_result",
}


class NonClosingStringIO(StringIO):
    def close(self) -> None:
        pass


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


def assert_result_shape(result: dict[str, Any]) -> None:
    if not isinstance(result, dict):
        raise AssertionError("local invocation result must be a JSON object")

    missing = sorted(REQUIRED_RESULT_FIELDS.difference(result))
    if missing:
        raise AssertionError(f"local invocation result missing fields: {missing}")

    if result["selected_terminal_path"] not in {"response", "failure"}:
        raise AssertionError("selected_terminal_path must be response or failure")

    locked = {
        "macro_report_unlock": False,
        "actual_handoff_executed": False,
        "cli_behavior_added": False,
    }
    for field, expected in locked.items():
        if result.get(field) is not expected:
            raise AssertionError(f"{field} must remain {expected!r}")

    leaked = sorted(
        {
            key
            for key, _ in iter_nested_items(result)
            if key in FORBIDDEN_OPERATIONAL_MARKERS
        }
    )
    if leaked:
        raise AssertionError(f"local invocation result contains forbidden markers: {leaked}")


def assert_response_result(result: dict[str, Any], response_path: Path) -> None:
    assert_result_shape(result)

    expected = {
        "invocation_type": "kernel_local_invocation",
        "invocation_state": "completed_terminal_artifact_written",
        "invocation_stage": "local_invocation_minimal_kernel_boundary",
        "selected_terminal_path": "response",
        "response_artifact_path": str(response_path),
        "failure_artifact_path": None,
        "terminal_artifact_written": True,
        "response_writer_called": True,
        "failure_writer_called": False,
        "macro_report_unlock": False,
        "actual_handoff_executed": False,
        "cli_behavior_added": False,
    }
    for field, expected_value in expected.items():
        if result.get(field) != expected_value:
            raise AssertionError(f"response result {field} should be {expected_value!r}")


def assert_failure_result(result: dict[str, Any], failure_path: Path) -> None:
    assert_result_shape(result)

    expected = {
        "invocation_type": "kernel_local_invocation",
        "invocation_state": "completed_terminal_artifact_written",
        "invocation_stage": "local_invocation_minimal_kernel_boundary",
        "selected_terminal_path": "failure",
        "response_artifact_path": None,
        "failure_artifact_path": str(failure_path),
        "terminal_artifact_written": True,
        "response_writer_called": False,
        "failure_writer_called": True,
        "macro_report_unlock": False,
        "actual_handoff_executed": False,
        "cli_behavior_added": False,
    }
    for field, expected_value in expected.items():
        if result.get(field) != expected_value:
            raise AssertionError(f"failure result {field} should be {expected_value!r}")


def capture_response_write(validated: dict[str, Any], destination: Path) -> dict[str, Any]:
    buffer = NonClosingStringIO()
    real_writer = capture_response_write.real_writer

    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=True):
            with mock.patch.object(Path, "open", return_value=buffer):
                artifact = real_writer(validated, destination)

    written = json.loads(buffer.getvalue())
    if written != artifact:
        raise AssertionError("response writer should return the written artifact")
    if written.get("artifact_type") != "kernel_response":
        raise AssertionError("response terminal artifact must be a kernel_response")
    return artifact


def capture_failure_write(classified: dict[str, Any], destination: Path) -> dict[str, Any]:
    buffer = NonClosingStringIO()
    real_writer = capture_failure_write.real_writer

    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=True):
            with mock.patch.object(Path, "open", return_value=buffer):
                artifact = real_writer(classified, destination)

    written = json.loads(buffer.getvalue())
    if written != artifact:
        raise AssertionError("failure writer should return the written artifact")
    if written.get("artifact_type") != "kernel_exchange_failure":
        raise AssertionError("failure terminal artifact must be a kernel_exchange_failure")
    return artifact


capture_response_write.real_writer = scaffold.write_response_artifact  # type: ignore[attr-defined]
capture_failure_write.real_writer = scaffold.write_failure_artifact  # type: ignore[attr-defined]


def check_response_path() -> None:
    response_path = Path("local") / "kernel_response.json"
    failure_path = Path("local") / "kernel_failure.json"

    with mock.patch.object(scaffold, "write_response_artifact", side_effect=capture_response_write) as response_writer:
        with mock.patch.object(scaffold, "write_failure_artifact", side_effect=capture_failure_write) as failure_writer:
            result = scaffold.invoke_local_adapter(
                ENVELOPE_FIXTURE,
                {
                    "response_artifact_path": response_path,
                    "failure_artifact_path": failure_path,
                },
            )

    if response_writer.call_count != 1:
        raise AssertionError("response path must call response writer exactly once")
    if failure_writer.called:
        raise AssertionError("response path must not call failure writer")
    assert_response_result(result, response_path)


def check_failure_path() -> None:
    response_path = Path("local") / "kernel_response.json"
    failure_path = Path("local") / "kernel_failure.json"
    malformed = scaffold.read_envelope_artifact(ENVELOPE_FIXTURE)
    malformed.pop("operator_intent")

    with mock.patch.object(scaffold, "read_envelope_artifact", return_value=malformed):
        with mock.patch.object(scaffold, "write_response_artifact", side_effect=capture_response_write) as response_writer:
            with mock.patch.object(scaffold, "write_failure_artifact", side_effect=capture_failure_write) as failure_writer:
                result = scaffold.invoke_local_adapter(
                    ENVELOPE_FIXTURE,
                    {
                        "response_artifact_path": response_path,
                        "failure_artifact_path": failure_path,
                    },
                )

    if response_writer.called:
        raise AssertionError("pre-response failure must not call response writer")
    if failure_writer.call_count != 1:
        raise AssertionError("failure path must call failure writer exactly once")
    assert_failure_result(result, failure_path)


def check_fail_closed_policy_inputs() -> None:
    response_path = Path("local") / "kernel_response.json"
    failure_path = Path("local") / "kernel_failure.json"
    valid_policy = {
        "response_artifact_path": response_path,
        "failure_artifact_path": failure_path,
    }

    assert_scaffold_error(
        "non-explicit envelope input",
        lambda: scaffold.invoke_local_adapter(["not", "a", "path"], valid_policy),  # type: ignore[arg-type]
    )
    assert_scaffold_error(
        "glob envelope input",
        lambda: scaffold.invoke_local_adapter("*.json", valid_policy),
    )
    assert_scaffold_error(
        "missing output policy",
        lambda: scaffold.invoke_local_adapter(ENVELOPE_FIXTURE, None),  # type: ignore[arg-type]
    )
    assert_scaffold_error(
        "missing response artifact path",
        lambda: scaffold.invoke_local_adapter(ENVELOPE_FIXTURE, {"failure_artifact_path": failure_path}),
    )
    assert_scaffold_error(
        "missing failure artifact path",
        lambda: scaffold.invoke_local_adapter(ENVELOPE_FIXTURE, {"response_artifact_path": response_path}),
    )
    assert_scaffold_error(
        "same response and failure artifact path",
        lambda: scaffold.invoke_local_adapter(
            ENVELOPE_FIXTURE,
            {
                "response_artifact_path": response_path,
                "failure_artifact_path": response_path,
            },
        ),
    )
    assert_scaffold_error(
        "queue-like policy fields",
        lambda: scaffold.invoke_local_adapter(
            ENVELOPE_FIXTURE,
            {
                "response_artifact_path": response_path,
                "failure_artifact_path": failure_path,
                "queue_path": Path("queue"),
            },
        ),
    )
    assert_scaffold_error(
        "macro_report_unlock true",
        lambda: scaffold.invoke_local_adapter(
            ENVELOPE_FIXTURE,
            {
                "response_artifact_path": response_path,
                "failure_artifact_path": failure_path,
                "macro_report_unlock": True,
            },
        ),
    )
    assert_scaffold_error(
        "actual_handoff_executed true",
        lambda: scaffold.invoke_local_adapter(
            ENVELOPE_FIXTURE,
            {
                "response_artifact_path": response_path,
                "failure_artifact_path": failure_path,
                "actual_handoff_executed": True,
            },
        ),
    )
    assert_scaffold_error(
        "cli_behavior_added true",
        lambda: scaffold.invoke_local_adapter(
            ENVELOPE_FIXTURE,
            {
                "response_artifact_path": response_path,
                "failure_artifact_path": failure_path,
                "cli_behavior_added": True,
            },
        ),
    )


def check_response_writer_failure_routes_to_failure() -> None:
    response_path = Path("local") / "kernel_response.json"
    failure_path = Path("local") / "kernel_failure.json"

    def fail_response_writer(validated: dict[str, Any], destination: Path) -> dict[str, Any]:
        raise scaffold.KernelFileExchangeAdapterScaffoldError("forced response writer failure")

    with mock.patch.object(scaffold, "write_response_artifact", side_effect=fail_response_writer) as response_writer:
        with mock.patch.object(scaffold, "write_failure_artifact", side_effect=capture_failure_write) as failure_writer:
            result = scaffold.invoke_local_adapter(
                ENVELOPE_FIXTURE,
                {
                    "response_artifact_path": response_path,
                    "failure_artifact_path": failure_path,
                },
            )

    if response_writer.call_count != 1:
        raise AssertionError("response writer failure check must call response writer once")
    if failure_writer.call_count != 1:
        raise AssertionError("response writer failure must route to failure writer once")
    assert_failure_result(result, failure_path)


def check_wrapper_remains_unchanged() -> None:
    wrapper_path = KERNEL_ROOT / "validation" / "run_all_kernel_local_checks.py"
    wrapper_text = wrapper_path.read_text(encoding="utf-8")
    helper_name = "kernel_local_invocation_contract_checks.py"
    if helper_name in wrapper_text:
        raise AssertionError("local invocation helper must remain outside wrapper")


def check_no_runtime_broadening_markers() -> None:
    source = scaffold.invoke_local_adapter.__code__.co_names
    forbidden_names = {
        "argparse",
        "subprocess",
        "sleep",
        "requests",
        "urllib",
    }
    leaked = sorted(forbidden_names.intersection(source))
    if leaked:
        raise AssertionError(f"local invocation function references forbidden runtime names: {leaked}")


def main() -> None:
    check_response_path()
    check_failure_path()
    check_fail_closed_policy_inputs()
    check_response_writer_failure_routes_to_failure()
    check_wrapper_remains_unchanged()
    check_no_runtime_broadening_markers()

    print("kernel-local-invocation-contract-checks-ok")


if __name__ == "__main__":
    main()
