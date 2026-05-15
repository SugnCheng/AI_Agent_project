"""Local checks for the minimal envelope-to-intake mapping contract surface.

This helper exercises only the current context-only mapping boundary. It does
not discover runtime queues, invoke kernel runtime, generate canonical task
objects, write response/failure artifacts, fetch sources, compose reports, run
scheduler behavior, or mutate fixtures.
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

EXPECTED_CONTEXT_KEYS = {
    "source_envelope",
    "operator_request",
    "source_context",
    "evidence_context",
    "expectation_context",
    "deferred_behavior_context",
    "mapping_stage",
}

FORBIDDEN_OUTPUT_KEYS = scaffold.CANONICAL_TASK_OBJECT_TOP_LEVEL_FIELDS.union(
    {
        "artifact_type",
        "artifact_version",
        "failure_stage",
        "failure_reason",
        "blocking",
        "response_artifact_path",
        "failure_artifact_path",
        "report_eligibility",
        "response_state",
        "kernel_conclusion",
        "kernel_conclusions",
        "p0_result",
        "p1_result",
        "p0_p10_runtime_result",
        "runtime_result",
        "canonical_task_object",
    }
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


def check_successful_mapping() -> dict[str, Any]:
    envelope = scaffold.read_envelope_artifact(ENVELOPE_FIXTURE)
    validated = scaffold.validate_envelope_intake(envelope)
    context = scaffold.prepare_kernel_intake(validated)

    if set(context) != EXPECTED_CONTEXT_KEYS:
        raise AssertionError(f"unexpected kernel_intake_context keys: {sorted(context)}")

    if context["source_envelope"] is validated:
        raise AssertionError("source_envelope should be an isolated copy")

    if context["source_envelope"] != validated:
        raise AssertionError("source_envelope should preserve the validated envelope")

    if context["operator_request"] != validated["operator_intent"]:
        raise AssertionError("operator_request should derive from operator_intent")

    expected_source_context = {
        "source_project": validated["source_project"],
        "profile_id": validated["profile_id"],
        "run_mode": validated["run_mode"],
        "report_target": validated["report_target"],
        "regions": validated["regions"],
    }
    if context["source_context"] != expected_source_context:
        raise AssertionError("source_context should preserve source/run metadata")

    expected_evidence_context = {
        "evidence_bundle": validated["evidence_bundle"],
        "evidence_context": validated["evidence_context"],
    }
    if context["evidence_context"] != expected_evidence_context:
        raise AssertionError("evidence_context should preserve evidence fields")

    if context["expectation_context"] != validated["kernel_task_object_expectation"]:
        raise AssertionError("expectation_context should preserve expectation metadata")

    if context["deferred_behavior_context"] != validated["deferred_runtime_behavior"]:
        raise AssertionError("deferred_behavior_context should preserve deferred behavior")

    if context["mapping_stage"] != "kernel_intake_context_pre_runtime":
        raise AssertionError("mapping_stage should stop before runtime")

    leaked = sorted(FORBIDDEN_OUTPUT_KEYS.intersection(context))
    if leaked:
        raise AssertionError(f"kernel_intake_context contains forbidden fields: {leaked}")

    return context


def check_mapping_failures() -> None:
    envelope = load_fixture_envelope()

    assert_scaffold_error(
        "non-object mapping input",
        lambda: scaffold.prepare_kernel_intake(["not", "an", "object"]),  # type: ignore[arg-type]
    )

    missing_field = dict(envelope)
    missing_field.pop("operator_intent")
    assert_scaffold_error(
        "missing required envelope field",
        lambda: scaffold.prepare_kernel_intake(missing_field),
    )

    response_artifact = dict(envelope)
    response_artifact["artifact_type"] = "kernel_response"
    assert_scaffold_error(
        "response artifact as mapping input",
        lambda: scaffold.prepare_kernel_intake(response_artifact),
    )

    failure_artifact = dict(envelope)
    failure_artifact["artifact_type"] = "kernel_exchange_failure"
    assert_scaffold_error(
        "failure artifact as mapping input",
        lambda: scaffold.prepare_kernel_intake(failure_artifact),
    )

    leaked_task_field = dict(envelope)
    leaked_task_field["framed_objective"] = {"summary": "not allowed"}
    assert_scaffold_error(
        "canonical task field leakage",
        lambda: scaffold.prepare_kernel_intake(leaked_task_field),
    )


def check_stop_before_runtime(context: dict[str, Any]) -> None:
    with mock.patch.object(scaffold, "invoke_kernel_runtime") as mocked_invoke:
        envelope = scaffold.read_envelope_artifact(ENVELOPE_FIXTURE)
        scaffold.prepare_kernel_intake(envelope)
        if mocked_invoke.called:
            raise AssertionError("prepare_kernel_intake must not invoke runtime")

    assert_not_implemented(
        "invoke_kernel_runtime",
        lambda: scaffold.invoke_kernel_runtime(context),
    )


def main() -> None:
    context = check_successful_mapping()
    check_mapping_failures()
    check_stop_before_runtime(context)

    print("kernel-intake-mapping-contract-checks-ok")


if __name__ == "__main__":
    main()
