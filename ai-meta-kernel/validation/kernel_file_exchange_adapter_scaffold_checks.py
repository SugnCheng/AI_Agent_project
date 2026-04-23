"""Local checks for the kernel file exchange adapter scaffold.

This helper exercises only the current scaffold boundary against committed
fixtures. It does not invoke kernel runtime, generate canonical task objects,
write response/failure artifacts, fetch sources, compose reports, or run
scheduler behavior.
"""

from __future__ import annotations

from pathlib import Path
import sys


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


def assert_raises_not_implemented(label: str, callback) -> None:
    try:
        callback()
    except NotImplementedError:
        return
    raise AssertionError(f"{label} must remain fail-closed with NotImplementedError")


def check_envelope_boundary() -> dict:
    envelope = scaffold.read_envelope_artifact(ENVELOPE_FIXTURE)
    validated = scaffold.validate_envelope_intake(envelope)
    if validated is not envelope:
        raise AssertionError("validate_envelope_intake should return the original envelope object")
    return envelope


def check_response_boundary() -> dict:
    response = scaffold.read_json_object(RESPONSE_FIXTURE, "response fixture")
    validated = scaffold.validate_kernel_response(response)
    if validated is not response:
        raise AssertionError("validate_kernel_response should return the original response object")
    return response


def check_blocked_boundaries(envelope: dict, response: dict) -> None:
    failure = scaffold.read_json_object(FAILURE_FIXTURE, "failure fixture")

    assert_raises_not_implemented(
        "prepare_kernel_intake",
        lambda: scaffold.prepare_kernel_intake(envelope),
    )
    assert_raises_not_implemented(
        "invoke_kernel_runtime",
        lambda: scaffold.invoke_kernel_runtime({"placeholder": "kernel_intake"}),
    )
    assert_raises_not_implemented(
        "write_response_artifact",
        lambda: scaffold.write_response_artifact(response, "unused_kernel_response.json"),
    )
    assert_raises_not_implemented(
        "write_failure_artifact",
        lambda: scaffold.write_failure_artifact(failure, "unused_kernel_failure.json"),
    )


def main() -> None:
    envelope = check_envelope_boundary()
    response = check_response_boundary()
    check_blocked_boundaries(envelope, response)
    print("kernel-file-exchange-adapter-scaffold-checks-ok")


if __name__ == "__main__":
    main()
