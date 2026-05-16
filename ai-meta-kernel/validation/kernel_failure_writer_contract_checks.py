"""Standalone checks for the minimal failure writer contract surface.

This helper exercises only the current minimal failure writer boundary. It
keeps the helper standalone, does not include itself in the main wrapper, does
not write response artifacts, and does not unlock CLI, macro reporting,
scheduler behavior, queue discovery, polling, retry, cleanup, or handoff.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from io import StringIO
from typing import Any, Callable
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
KERNEL_ROOT = REPO_ROOT / "ai-meta-kernel"

sys.path.insert(0, str(KERNEL_ROOT))

import file_exchange_adapter_scaffold as scaffold  # noqa: E402


FORBIDDEN_WRITTEN_ARTIFACT_FIELDS = {
    "response_artifact_path",
    "failure_artifact_path",
    "report_eligibility",
    "macro_report_eligibility",
    "downstream_reporting_allowed",
    "cli_success_signal",
    "external_service_result",
    "scheduler_result",
    "actual_handoff",
    "handoff_marker",
}


class NonClosingStringIO(StringIO):
    def close(self) -> None:
        pass


def build_classified_failure() -> dict[str, Any]:
    source = {
        "source_boundary": "reader_boundary",
        "failure_stage": "reader",
        "failure_code": "reader_failed",
        "failure_message": "reader failed before terminal writing",
    }
    return scaffold.classify_blocking_failure(source)


def assert_scaffold_error(label: str, callback: Callable[[], object]) -> None:
    try:
        callback()
    except scaffold.KernelFileExchangeAdapterScaffoldError:
        return
    raise AssertionError(f"{label} must fail closed with scaffold error")


def assert_no_forbidden_artifact_fields(artifact: dict[str, Any]) -> None:
    leaked = sorted(FORBIDDEN_WRITTEN_ARTIFACT_FIELDS.intersection(artifact))
    if leaked:
        raise AssertionError(f"failure artifact contains forbidden fields: {leaked}")


def capture_failure_write(classified: dict[str, Any], destination: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    buffer = NonClosingStringIO()

    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=True):
            with mock.patch.object(Path, "open", return_value=buffer) as mocked_open:
                artifact = scaffold.write_failure_artifact(classified, destination)

    if mocked_open.call_count != 1:
        raise AssertionError("failure writer should open exactly one destination for writing")

    written = json.loads(buffer.getvalue())
    return artifact, written


def check_successful_failure_write() -> None:
    classified = build_classified_failure()

    destination = Path("local") / "kernel_failure.example.json"
    artifact, written = capture_failure_write(classified, destination)

    if not isinstance(written, dict):
        raise AssertionError("written failure artifact must be a JSON object")

    if written != artifact:
        raise AssertionError("returned artifact should match the written JSON artifact")

    expected_markers = {
        "artifact_type": "kernel_exchange_failure",
        "artifact_state": "written_failure_artifact",
        "blocking": True,
        "terminal_artifact_written": True,
        "response_writer_called": False,
        "failure_writer_called": True,
        "macro_report_unlock": False,
        "writer_stage": "failure_writer_minimal_local_artifact",
    }
    for field, expected in expected_markers.items():
        if written.get(field) != expected:
            raise AssertionError(f"written artifact {field} should be {expected!r}")

    if written.get("artifact_type") == "kernel_response":
        raise AssertionError("failure artifact must not carry a response artifact marker")

    if written.get("source_classified_failure") != classified:
        raise AssertionError("written artifact should preserve the classified failure")

    if written.get("source_classified_failure") is classified:
        raise AssertionError("written artifact should isolate the classified failure copy")

    source = written["source_classified_failure"]
    if source.get("failure_artifact_written") is not False:
        raise AssertionError("source classified failure must remain pre-writer")

    if source.get("macro_report_unlock") is not False:
        raise AssertionError("source classified failure must keep macro reporting locked")

    assert_no_forbidden_artifact_fields(written)


def check_writer_failures() -> None:
    classified = build_classified_failure()

    assert_scaffold_error(
        "non-object failure writer input",
        lambda: scaffold.write_failure_artifact(["not", "an", "object"], REPO_ROOT / "unused.json"),  # type: ignore[arg-type]
    )

    malformed = dict(classified)
    malformed.pop("classified_failure_type")
    assert_scaffold_error(
        "malformed classified failure",
        lambda: scaffold.write_failure_artifact(malformed, REPO_ROOT / "unused.json"),
    )

    response_artifact_input = dict(classified)
    response_artifact_input["artifact_type"] = "kernel_response"
    assert_scaffold_error(
        "response artifact as failure writer input",
        lambda: scaffold.write_failure_artifact(response_artifact_input, REPO_ROOT / "unused.json"),
    )

    failure_artifact_input = dict(classified)
    failure_artifact_input["artifact_type"] = "kernel_exchange_failure"
    assert_scaffold_error(
        "failure artifact as failure writer input",
        lambda: scaffold.write_failure_artifact(failure_artifact_input, REPO_ROOT / "unused.json"),
    )

    for marker in (
        "terminal_artifact_written",
        "response_artifact_written",
        "failure_artifact_written",
        "macro_report_unlock",
    ):
        marked = dict(classified)
        marked[marker] = True
        assert_scaffold_error(
            f"{marker} true",
            lambda marked=marked: scaffold.write_failure_artifact(marked, REPO_ROOT / "unused.json"),
        )

    with mock.patch.object(Path, "exists", return_value=True):
        with mock.patch.object(Path, "is_dir", return_value=False):
            destination = Path("local") / "kernel_failure.example.json"
            assert_scaffold_error(
                "existing destination path",
                lambda: scaffold.write_failure_artifact(classified, destination),
            )

    with mock.patch.object(Path, "exists", return_value=True):
        with mock.patch.object(Path, "is_dir", return_value=True):
            assert_scaffold_error(
                "destination directory as file path",
                lambda: scaffold.write_failure_artifact(classified, Path("local")),
            )

    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=False):
            missing_parent = Path("missing") / "kernel_failure.example.json"
            assert_scaffold_error(
                "missing destination parent",
                lambda: scaffold.write_failure_artifact(classified, missing_parent),
            )


def check_writer_does_not_call_response_writer() -> None:
    classified = build_classified_failure()

    with mock.patch.object(scaffold, "write_response_artifact") as mocked_response_writer:
        capture_failure_write(classified, Path("local") / "kernel_failure.example.json")

    if mocked_response_writer.called:
        raise AssertionError("write_failure_artifact must not call response writer")


def check_response_writer_and_wrapper_remain_unchanged() -> None:
    if not callable(scaffold.write_response_artifact):
        raise AssertionError("response writer must remain callable")

    wrapper_path = KERNEL_ROOT / "validation" / "run_all_kernel_local_checks.py"
    wrapper_text = wrapper_path.read_text(encoding="utf-8")
    helper_name = "kernel_failure_writer_contract_checks.py"
    if helper_name in wrapper_text:
        raise AssertionError("failure writer helper must remain outside wrapper")


def main() -> None:
    check_successful_failure_write()
    check_writer_failures()
    check_writer_does_not_call_response_writer()
    check_response_writer_and_wrapper_remain_unchanged()

    print("kernel-failure-writer-contract-checks-ok")


if __name__ == "__main__":
    main()
