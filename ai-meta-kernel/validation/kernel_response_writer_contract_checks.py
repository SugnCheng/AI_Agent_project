"""Local checks for the minimal response writer contract surface.

This helper exercises only the current R14 response writer boundary. It keeps
the helper standalone, does not include itself in the main wrapper, does not
write failure artifacts, and does not unlock CLI, macro reporting, scheduler
behavior, queue discovery, polling, retry, cleanup, or actual handoff.
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
FIXTURE_ROOT = KERNEL_ROOT / "examples" / "file-exchange"

sys.path.insert(0, str(KERNEL_ROOT))

import file_exchange_adapter_scaffold as scaffold  # noqa: E402


ENVELOPE_FIXTURE = (
    FIXTURE_ROOT
    / "envelopes"
    / "daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.example.json"
)

FORBIDDEN_WRITTEN_ARTIFACT_FIELDS = {
    "failure_artifact_path",
    "report_eligibility",
    "macro_report_eligibility",
    "downstream_reporting_allowed",
    "cli_success_signal",
    "external_service_result",
    "scheduler_result",
}


class NonClosingStringIO(StringIO):
    def close(self) -> None:
        pass


def build_validated_pre_writer_response() -> dict[str, Any]:
    envelope = scaffold.read_envelope_artifact(ENVELOPE_FIXTURE)
    intake = scaffold.prepare_kernel_intake(scaffold.validate_envelope_intake(envelope))
    candidate = scaffold.invoke_kernel_runtime(intake)
    return scaffold.validate_candidate_response(candidate)


def assert_scaffold_error(label: str, callback: Callable[[], object]) -> None:
    try:
        callback()
    except scaffold.KernelFileExchangeAdapterScaffoldError:
        return
    raise AssertionError(f"{label} must fail closed with scaffold error")


def assert_no_forbidden_artifact_fields(artifact: dict[str, Any]) -> None:
    leaked = sorted(FORBIDDEN_WRITTEN_ARTIFACT_FIELDS.intersection(artifact))
    if leaked:
        raise AssertionError(f"response artifact contains forbidden fields: {leaked}")


def capture_response_write(validated: dict[str, Any], destination: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    buffer = NonClosingStringIO()

    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=True):
            with mock.patch.object(Path, "open", return_value=buffer) as mocked_open:
                artifact = scaffold.write_response_artifact(validated, destination)

    if mocked_open.call_count != 1:
        raise AssertionError("response writer should open exactly one destination for writing")

    written = json.loads(buffer.getvalue())
    return artifact, written


def check_successful_response_write() -> None:
    validated = build_validated_pre_writer_response()

    destination = Path("local") / "kernel_response.example.json"
    artifact, written = capture_response_write(validated, destination)

    if not isinstance(written, dict):
        raise AssertionError("written response artifact must be a JSON object")

    if written != artifact:
        raise AssertionError("returned artifact should match the written JSON artifact")

    expected_markers = {
        "artifact_type": "kernel_response",
        "artifact_state": "written_response_artifact",
        "terminal_artifact_written": True,
        "response_writer_called": True,
        "failure_writer_called": False,
        "macro_report_unlock": False,
        "writer_stage": "response_writer_minimal_local_artifact",
    }
    for field, expected in expected_markers.items():
        if written.get(field) != expected:
            raise AssertionError(f"written artifact {field} should be {expected!r}")

    if written.get("source_validated_response") != validated:
        raise AssertionError("written artifact should preserve the validated response")

    if written.get("source_validated_response") is validated:
        raise AssertionError("written artifact should isolate the validated response copy")

    if written["source_validated_response"].get("failure_writer_allowed") is not False:
        raise AssertionError("source validated response must keep failure writer blocked")

    assert_no_forbidden_artifact_fields(written)


def check_writer_failures() -> None:
    validated = build_validated_pre_writer_response()

    with mock.patch.object(Path, "exists", return_value=True):
        with mock.patch.object(Path, "is_dir", return_value=False):
            destination = Path("local") / "kernel_response.example.json"
            assert_scaffold_error(
                "existing destination path",
                lambda: scaffold.write_response_artifact(validated, destination),
            )

    with mock.patch.object(Path, "exists", return_value=True):
        with mock.patch.object(Path, "is_dir", return_value=True):
            assert_scaffold_error(
                "destination directory as file path",
                lambda: scaffold.write_response_artifact(validated, Path("local")),
            )

    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=False):
            missing_parent = Path("missing") / "kernel_response.example.json"
            assert_scaffold_error(
                "missing destination parent",
                lambda: scaffold.write_response_artifact(validated, missing_parent),
            )

    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=True):
            with mock.patch.object(Path, "open") as mocked_open:
                mocked_open.side_effect = AssertionError("writer should reject invalid input before opening destination")

                assert_scaffold_error(
                    "non-object response writer input",
                    lambda: scaffold.write_response_artifact(["not", "an", "object"], REPO_ROOT / "unused.json"),  # type: ignore[arg-type]
                )

    malformed = dict(validated)
    malformed.pop("validated_response_type")
    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=True):
            with mock.patch.object(Path, "open") as mocked_open:
                mocked_open.side_effect = AssertionError("writer should reject malformed input before opening destination")
                assert_scaffold_error(
                    "malformed validated response",
                    lambda: scaffold.write_response_artifact(malformed, REPO_ROOT / "unused.json"),
                )

    writer_enabled = dict(validated)
    writer_enabled["response_writer_allowed"] = True
    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=True):
            with mock.patch.object(Path, "open") as mocked_open:
                mocked_open.side_effect = AssertionError("writer should reject writer-enabled input before opening destination")
                assert_scaffold_error(
                    "response_writer_allowed true",
                    lambda: scaffold.write_response_artifact(writer_enabled, REPO_ROOT / "unused.json"),
                )

    failure_enabled = dict(validated)
    failure_enabled["failure_writer_allowed"] = True
    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=True):
            with mock.patch.object(Path, "open") as mocked_open:
                mocked_open.side_effect = AssertionError("writer should reject failure-writer input before opening destination")
                assert_scaffold_error(
                    "failure_writer_allowed true",
                    lambda: scaffold.write_response_artifact(failure_enabled, REPO_ROOT / "unused.json"),
                )

    response_artifact_input = dict(validated)
    response_artifact_input["artifact_type"] = "kernel_response"
    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=True):
            with mock.patch.object(Path, "open") as mocked_open:
                mocked_open.side_effect = AssertionError("writer should reject response artifact input before opening destination")
                assert_scaffold_error(
                    "response artifact as writer input",
                    lambda: scaffold.write_response_artifact(response_artifact_input, REPO_ROOT / "unused.json"),
                )

    failure_artifact_input = dict(validated)
    failure_artifact_input["artifact_type"] = "kernel_exchange_failure"
    with mock.patch.object(Path, "exists", return_value=False):
        with mock.patch.object(Path, "is_dir", return_value=True):
            with mock.patch.object(Path, "open") as mocked_open:
                mocked_open.side_effect = AssertionError("writer should reject failure artifact input before opening destination")
                assert_scaffold_error(
                    "failure artifact as writer input",
                    lambda: scaffold.write_response_artifact(failure_artifact_input, REPO_ROOT / "unused.json"),
                )


def check_failure_writer_remains_blocked() -> None:
    validated = build_validated_pre_writer_response()

    with mock.patch.object(scaffold, "write_failure_artifact") as mocked_failure_writer:
        capture_response_write(validated, Path("local") / "kernel_response.example.json")

    if mocked_failure_writer.called:
        raise AssertionError("write_response_artifact must not call failure writer")

    assert_scaffold_error(
        "reader still rejects directory input",
        lambda: scaffold.read_envelope_artifact(KERNEL_ROOT),
    )

    wrapper_path = KERNEL_ROOT / "validation" / "run_all_kernel_local_checks.py"
    wrapper_text = wrapper_path.read_text(encoding="utf-8")
    if "kernel_response_writer_contract_checks.py" in wrapper_text:
        raise AssertionError("response writer helper must remain outside wrapper")


def check_real_writer_function_is_not_mock_only() -> None:
    if not callable(scaffold.write_response_artifact):
        raise AssertionError("write_response_artifact must remain callable")

    with mock.patch.object(Path, "exists", return_value=True):
        with mock.patch.object(Path, "is_dir", return_value=True):
            assert_scaffold_error(
                "real writer rejects destination directory",
                lambda: scaffold.write_response_artifact(build_validated_pre_writer_response(), Path("local")),
            )


def main() -> None:
    check_successful_response_write()
    check_writer_failures()
    check_failure_writer_remains_blocked()
    check_real_writer_function_is_not_mock_only()

    print("kernel-response-writer-contract-checks-ok")


if __name__ == "__main__":
    main()
