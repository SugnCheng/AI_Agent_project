"""Fail-closed scaffold for future kernel-side file exchange adapter boundaries.

This module is intentionally narrow. It may read and validate one local kernel
input envelope, produce one local candidate response from a validated intake
context, validate that candidate as local pre-writer output, and write one
local response artifact from that validated output, but it does not execute the
real P0-P10 runtime, generate canonical task objects from envelopes, write
failure artifacts, or orchestrate handoff.
"""

from __future__ import annotations

import json
from pathlib import Path
from copy import deepcopy
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - developer environment guard.
    Draft202012Validator = None  # type: ignore[assignment]


KERNEL_ROOT = Path(__file__).resolve().parent
TASK_OBJECT_SCHEMA = KERNEL_ROOT / "meta-layer" / "TASK_OBJECT_SCHEMA.json"

ENVELOPE_REQUIRED_FIELDS = {
    "envelope_type",
    "envelope_version",
    "source_project",
    "profile_id",
    "run_mode",
    "report_target",
    "regions",
    "operator_intent",
    "evidence_bundle",
    "evidence_context",
    "kernel_task_object_expectation",
    "deferred_runtime_behavior",
}

CANONICAL_TASK_OBJECT_TOP_LEVEL_FIELDS = {
    "schema_version",
    "task_id",
    "raw_request",
    "kernel_stage",
    "framed_objective",
    "task_classification",
    "risk_profile",
    "triggered_habits",
    "structural_decomposition",
    "required_checks",
    "status_flags",
    "verification_plan",
    "challenge_loop",
    "downstream_recommendation",
    "handoff",
}

KERNEL_INTAKE_CONTEXT_REQUIRED_FIELDS = {
    "source_envelope",
    "operator_request",
    "source_context",
    "evidence_context",
    "expectation_context",
    "deferred_behavior_context",
    "mapping_stage",
}

CANDIDATE_RESPONSE_REQUIRED_FIELDS = {
    "candidate_type",
    "candidate_version",
    "candidate_state",
    "invocation_stage",
    "source_context",
    "operator_request",
    "evidence_context",
    "expectation_context",
    "deferred_behavior_context",
    "source_mapping_stage",
    "terminal_artifact_written",
    "response_writer_called",
    "failure_writer_called",
    "macro_report_unlock",
}

FORBIDDEN_RESPONSE_VALIDATION_FIELDS = {
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

VALIDATED_RESPONSE_REQUIRED_FIELDS = {
    "validated_response_type",
    "validated_response_state",
    "source_candidate",
    "response_writer_allowed",
    "failure_writer_allowed",
    "macro_report_unlock",
    "validation_stage",
}

FORBIDDEN_RESPONSE_WRITER_INPUT_FIELDS = FORBIDDEN_RESPONSE_VALIDATION_FIELDS.union(
    {
        "artifact_type",
        "artifact_state",
        "artifact_path",
        "terminal_artifact_written",
        "response_writer_called",
        "failure_writer_called",
        "writer_stage",
    }
)

BLOCKING_FAILURE_SOURCE_REQUIRED_FIELDS = {
    "source_boundary",
    "failure_stage",
    "failure_code",
    "failure_message",
}

ALLOWED_BLOCKING_FAILURE_STAGES = {
    "reader",
    "envelope_validation",
    "intake_mapping",
    "runtime_invocation",
    "response_validation",
    "response_writer",
}

FORBIDDEN_BLOCKING_FAILURE_SOURCE_FIELDS = {
    "failure_artifact_path",
    "response_artifact_path",
    "cli_success_signal",
    "report_eligibility",
    "macro_report_eligibility",
    "downstream_reporting_allowed",
    "actual_handoff",
    "handoff_marker",
}

CLASSIFIED_FAILURE_REQUIRED_FIELDS = {
    "failure_type",
    "classified_failure_type",
    "classified_failure_state",
    "failure_stage",
    "failure_code",
    "failure_message",
    "source_boundary",
    "is_blocking",
    "terminal_artifact_written",
    "response_artifact_written",
    "failure_artifact_written",
    "macro_report_unlock",
    "classification_stage",
}

FORBIDDEN_FAILURE_WRITER_INPUT_FIELDS = FORBIDDEN_BLOCKING_FAILURE_SOURCE_FIELDS.union(
    {
        "artifact_type",
        "artifact_state",
        "artifact_path",
        "response_writer_called",
        "failure_writer_called",
        "writer_stage",
    }
)

FORBIDDEN_TERMINAL_DRY_RUN_MARKER_FIELDS = {
    "cli_behavior_added",
    "cli_success_signal",
    "actual_handoff",
    "actual_handoff_executed",
    "handoff_marker",
    "macro_report_eligibility",
    "report_eligibility",
    "downstream_reporting_allowed",
    "scheduler_result",
    "queue_discovery",
    "polling_behavior",
    "watcher_behavior",
    "retry_behavior",
    "backoff_behavior",
    "cleanup_behavior",
}

FORBIDDEN_TERMINAL_DRY_RUN_TRUE_FIELDS = {
    "macro_report_unlock",
    "terminal_artifact_written",
    "response_artifact_written",
    "failure_artifact_written",
    "response_writer_called",
    "failure_writer_called",
}

OUTPUT_DESTINATION_POLICY_REQUIRED_FIELDS = {
    "response_artifact_path",
    "failure_artifact_path",
}

OUTPUT_DESTINATION_POLICY_ALLOWED_FIELDS = OUTPUT_DESTINATION_POLICY_REQUIRED_FIELDS.union(
    {
        "macro_report_unlock",
        "actual_handoff_executed",
        "cli_behavior_added",
    }
)

FORBIDDEN_OUTPUT_DESTINATION_POLICY_FIELDS = {
    "queue",
    "queue_dir",
    "queue_path",
    "queue_directory",
    "queue_discovery",
    "scheduler",
    "scheduler_input",
    "scheduler_result",
    "polling",
    "polling_behavior",
    "watcher",
    "watcher_behavior",
    "retry",
    "retry_behavior",
    "backoff",
    "backoff_behavior",
    "cleanup",
    "cleanup_behavior",
    "macro_report_eligibility",
    "report_eligibility",
    "downstream_reporting_allowed",
    "actual_handoff",
    "handoff_marker",
    "cli_success_signal",
    "external_service_input",
    "external_service_result",
}

LOCAL_INVOCATION_RESULT_FIELDS = {
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


class KernelFileExchangeAdapterScaffoldError(ValueError):
    """Raised when scaffold boundary validation fails."""


class KernelFileExchangeAdapterScaffoldNotImplementedError(
    KernelFileExchangeAdapterScaffoldError,
    NotImplementedError,
):
    """Raised for legacy blocked-boundary inputs that still fail closed."""


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise KernelFileExchangeAdapterScaffoldError(f"{label} must be a JSON object")
    return value


def _require_explicit_local_path(value: Any, label: str) -> Path:
    if not isinstance(value, (str, Path)):
        raise KernelFileExchangeAdapterScaffoldError(f"{label} must be an explicit local path")

    path_text = str(value)
    if not path_text.strip():
        raise KernelFileExchangeAdapterScaffoldError(f"{label} must be a non-empty path")

    if any(marker in path_text for marker in ("*", "?")):
        raise KernelFileExchangeAdapterScaffoldError(
            f"{label} must not contain discovery or glob markers"
        )

    return Path(value)


def _validate_output_destination_policy(policy: dict[str, Any]) -> dict[str, Path]:
    policy = _require_object(policy, "output_destination_policy")

    missing = sorted(OUTPUT_DESTINATION_POLICY_REQUIRED_FIELDS.difference(policy))
    if missing:
        raise KernelFileExchangeAdapterScaffoldError(
            f"output destination policy missing required fields: {missing}"
        )

    unknown = sorted(set(policy).difference(OUTPUT_DESTINATION_POLICY_ALLOWED_FIELDS))
    if unknown:
        raise KernelFileExchangeAdapterScaffoldError(
            f"output destination policy contains unsupported fields: {unknown}"
        )

    forbidden = sorted(
        {
            key
            for key, _ in _iter_nested_items(policy)
            if key in FORBIDDEN_OUTPUT_DESTINATION_POLICY_FIELDS
        }
    )
    if forbidden:
        raise KernelFileExchangeAdapterScaffoldError(
            "output destination policy must not contain queue, scheduler, polling, "
            f"retry, cleanup, reporting, CLI, handoff, or external service fields: {forbidden}"
        )

    for locked_field in (
        "macro_report_unlock",
        "actual_handoff_executed",
        "cli_behavior_added",
    ):
        if policy.get(locked_field) is True:
            raise KernelFileExchangeAdapterScaffoldError(
                f"output destination policy {locked_field} must not be true"
            )

    response_path = _require_explicit_local_path(
        policy["response_artifact_path"],
        "response_artifact_path",
    )
    failure_path = _require_explicit_local_path(
        policy["failure_artifact_path"],
        "failure_artifact_path",
    )

    if response_path == failure_path or response_path.resolve() == failure_path.resolve():
        raise KernelFileExchangeAdapterScaffoldError(
            "response and failure artifact destinations must be distinct"
        )

    return {
        "response_artifact_path": response_path,
        "failure_artifact_path": failure_path,
    }


def _blocking_failure_source(
    *,
    source_boundary: str,
    failure_stage: str,
    failure_code: str,
    failure_message: str,
) -> dict[str, Any]:
    return {
        "source_boundary": source_boundary,
        "failure_stage": failure_stage,
        "failure_code": failure_code,
        "failure_message": failure_message,
    }


def _local_invocation_result(
    *,
    source_envelope_path: Path,
    selected_terminal_path: str,
    response_artifact_path: Path | None,
    failure_artifact_path: Path | None,
    terminal_artifact_written: bool,
    response_writer_called: bool,
    failure_writer_called: bool,
) -> dict[str, Any]:
    result = {
        "invocation_type": "kernel_local_invocation",
        "invocation_state": "completed_terminal_artifact_written",
        "invocation_stage": "local_invocation_minimal_kernel_boundary",
        "source_envelope_path": str(source_envelope_path),
        "selected_terminal_path": selected_terminal_path,
        "response_artifact_path": str(response_artifact_path) if response_artifact_path is not None else None,
        "failure_artifact_path": str(failure_artifact_path) if failure_artifact_path is not None else None,
        "terminal_artifact_written": terminal_artifact_written,
        "response_writer_called": response_writer_called,
        "failure_writer_called": failure_writer_called,
        "macro_report_unlock": False,
        "actual_handoff_executed": False,
        "cli_behavior_added": False,
    }

    missing = sorted(LOCAL_INVOCATION_RESULT_FIELDS.difference(result))
    if missing:
        raise KernelFileExchangeAdapterScaffoldError(
            f"local invocation result missing fields: {missing}"
        )

    return result


def read_envelope_artifact(path: str | Path) -> dict[str, Any]:
    """Read exactly one local kernel input envelope artifact.

    This function performs only local file reading and JSON shape validation. It
    does not discover artifacts, mutate files, invoke runtime, or write outputs.
    """

    envelope_path = Path(path)
    if not envelope_path.is_file():
        raise KernelFileExchangeAdapterScaffoldError(
            f"envelope artifact does not exist or is not a file: {envelope_path}"
        )

    with envelope_path.open("r", encoding="utf-8") as file:
        try:
            envelope = json.load(file)
        except json.JSONDecodeError as exc:
            raise KernelFileExchangeAdapterScaffoldError(
                f"envelope artifact is not valid JSON: {envelope_path}"
            ) from exc

    return _require_object(envelope, "envelope artifact")


def validate_envelope_intake(envelope: dict[str, Any]) -> dict[str, Any]:
    """Validate envelope guardrails before any future runtime invocation."""

    envelope = _require_object(envelope, "envelope")

    missing = sorted(ENVELOPE_REQUIRED_FIELDS.difference(envelope))
    if missing:
        raise KernelFileExchangeAdapterScaffoldError(
            f"envelope missing required fields: {missing}"
        )

    if envelope.get("envelope_type") != "kernel_input_envelope":
        raise KernelFileExchangeAdapterScaffoldError(
            "artifact is not a kernel input envelope"
        )

    if envelope.get("artifact_type") == "kernel_response":
        raise KernelFileExchangeAdapterScaffoldError(
            "response artifacts are not valid envelope intake"
        )

    if envelope.get("artifact_type") == "kernel_exchange_failure":
        raise KernelFileExchangeAdapterScaffoldError(
            "failure artifacts are not valid envelope intake"
        )

    if not isinstance(envelope.get("regions"), list) or not envelope["regions"]:
        raise KernelFileExchangeAdapterScaffoldError("envelope regions must be a non-empty list")

    if not isinstance(envelope.get("operator_intent"), str) or not envelope["operator_intent"].strip():
        raise KernelFileExchangeAdapterScaffoldError(
            "envelope operator_intent must be a non-empty string"
        )

    leaked_fields = sorted(CANONICAL_TASK_OBJECT_TOP_LEVEL_FIELDS.intersection(envelope))
    if leaked_fields:
        raise KernelFileExchangeAdapterScaffoldError(
            "envelope must not contain canonical task object fields: "
            f"{leaked_fields}"
        )

    for field in ("evidence_bundle", "evidence_context", "kernel_task_object_expectation"):
        if not isinstance(envelope.get(field), dict):
            raise KernelFileExchangeAdapterScaffoldError(
                f"envelope {field} must be a JSON object"
            )

    if not isinstance(envelope.get("deferred_runtime_behavior"), list):
        raise KernelFileExchangeAdapterScaffoldError(
            "envelope deferred_runtime_behavior must be a list"
        )

    return envelope


def prepare_kernel_intake(envelope: dict[str, Any]) -> dict[str, Any]:
    """Prepare a context-only kernel intake object from one validated envelope.

    This boundary maps evidence and metadata only. It does not execute P0/P1,
    invoke runtime, generate canonical task objects, or write artifacts.
    """

    validated = validate_envelope_intake(envelope)
    return {
        "source_envelope": deepcopy(validated),
        "operator_request": validated["operator_intent"],
        "source_context": {
            "source_project": validated["source_project"],
            "profile_id": validated["profile_id"],
            "run_mode": validated["run_mode"],
            "report_target": validated["report_target"],
            "regions": deepcopy(validated["regions"]),
        },
        "evidence_context": {
            "evidence_bundle": deepcopy(validated["evidence_bundle"]),
            "evidence_context": deepcopy(validated["evidence_context"]),
        },
        "expectation_context": deepcopy(validated["kernel_task_object_expectation"]),
        "deferred_behavior_context": deepcopy(validated["deferred_runtime_behavior"]),
        "mapping_stage": "kernel_intake_context_pre_runtime",
    }


def validate_kernel_intake_context(kernel_intake: dict[str, Any]) -> dict[str, Any]:
    """Validate the context-only intake object before minimal invocation."""

    kernel_intake = _require_object(kernel_intake, "kernel_intake")

    if kernel_intake.get("envelope_type") == "kernel_input_envelope":
        raise KernelFileExchangeAdapterScaffoldError(
            "raw kernel input envelopes are not valid runtime invocation intake"
        )

    if kernel_intake.get("artifact_type") == "kernel_response":
        raise KernelFileExchangeAdapterScaffoldError(
            "response artifacts are not valid runtime invocation intake"
        )

    if kernel_intake.get("artifact_type") == "kernel_exchange_failure":
        raise KernelFileExchangeAdapterScaffoldError(
            "failure artifacts are not valid runtime invocation intake"
        )

    leaked_fields = sorted(CANONICAL_TASK_OBJECT_TOP_LEVEL_FIELDS.intersection(kernel_intake))
    if leaked_fields:
        raise KernelFileExchangeAdapterScaffoldError(
            "kernel intake must not contain canonical task object fields: "
            f"{leaked_fields}"
        )

    missing = sorted(KERNEL_INTAKE_CONTEXT_REQUIRED_FIELDS.difference(kernel_intake))
    if missing:
        raise KernelFileExchangeAdapterScaffoldError(
            f"kernel intake missing required fields: {missing}"
        )

    if kernel_intake.get("mapping_stage") != "kernel_intake_context_pre_runtime":
        raise KernelFileExchangeAdapterScaffoldError(
            "kernel intake mapping_stage must be kernel_intake_context_pre_runtime"
        )

    if not isinstance(kernel_intake.get("operator_request"), str) or not kernel_intake["operator_request"].strip():
        raise KernelFileExchangeAdapterScaffoldError(
            "kernel intake operator_request must be a non-empty string"
        )

    for field in (
        "source_envelope",
        "source_context",
        "evidence_context",
        "expectation_context",
    ):
        if not isinstance(kernel_intake.get(field), dict):
            raise KernelFileExchangeAdapterScaffoldError(
                f"kernel intake {field} must be a JSON object"
            )

    if not isinstance(kernel_intake.get("deferred_behavior_context"), list):
        raise KernelFileExchangeAdapterScaffoldError(
            "kernel intake deferred_behavior_context must be a list"
        )

    return kernel_intake


def invoke_kernel_runtime(kernel_intake: dict[str, Any]) -> dict[str, Any]:
    """Return a local candidate response object from one validated intake context.

    This is a minimal pre-writer invocation boundary. It does not execute the
    real P0-P10 runtime, validate a terminal response, write artifacts, or
    unlock reporting.
    """

    validated = validate_kernel_intake_context(kernel_intake)
    return {
        "candidate_type": "kernel_runtime_candidate_response",
        "candidate_version": "0.1.0",
        "candidate_state": "pre_writer_non_terminal",
        "invocation_stage": "kernel_runtime_invocation_candidate_only",
        "source_context": deepcopy(validated["source_context"]),
        "operator_request": validated["operator_request"],
        "evidence_context": deepcopy(validated["evidence_context"]),
        "expectation_context": deepcopy(validated["expectation_context"]),
        "deferred_behavior_context": deepcopy(validated["deferred_behavior_context"]),
        "source_mapping_stage": validated["mapping_stage"],
        "terminal_artifact_written": False,
        "response_writer_called": False,
        "failure_writer_called": False,
        "macro_report_unlock": False,
        "notes": [
            "candidate-only local invocation output",
            "not validated as terminal TASK_OBJECT_SCHEMA response",
            "stop before response validation and writers",
        ],
    }


def validate_candidate_response(candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate the current local candidate response before any writer boundary.

    This boundary validates only the Phase R8 candidate-only response contract.
    It does not validate terminal TASK_OBJECT_SCHEMA output, write artifacts,
    call writers, or unlock macro-side reporting.
    """

    candidate = _require_object(candidate, "candidate")

    if candidate.get("artifact_type") == "kernel_response":
        raise KernelFileExchangeAdapterScaffoldError(
            "response artifacts are not valid candidate response validation input"
        )

    if candidate.get("artifact_type") == "kernel_exchange_failure":
        raise KernelFileExchangeAdapterScaffoldError(
            "failure artifacts are not valid candidate response validation input"
        )

    missing = sorted(CANDIDATE_RESPONSE_REQUIRED_FIELDS.difference(candidate))
    if missing:
        raise KernelFileExchangeAdapterScaffoldError(
            f"candidate response missing required fields: {missing}"
        )

    expected_markers = {
        "candidate_type": "kernel_runtime_candidate_response",
        "candidate_state": "pre_writer_non_terminal",
        "invocation_stage": "kernel_runtime_invocation_candidate_only",
        "terminal_artifact_written": False,
        "response_writer_called": False,
        "failure_writer_called": False,
        "macro_report_unlock": False,
    }
    for field, expected in expected_markers.items():
        if candidate.get(field) != expected:
            raise KernelFileExchangeAdapterScaffoldError(
                f"candidate response {field} must be {expected!r}"
            )

    leaked_fields = sorted(FORBIDDEN_RESPONSE_VALIDATION_FIELDS.intersection(candidate))
    if leaked_fields:
        raise KernelFileExchangeAdapterScaffoldError(
            "candidate response must not contain terminal output fields: "
            f"{leaked_fields}"
        )

    if not isinstance(candidate.get("operator_request"), str) or not candidate["operator_request"].strip():
        raise KernelFileExchangeAdapterScaffoldError(
            "candidate response operator_request must be a non-empty string"
        )

    for field in (
        "source_context",
        "evidence_context",
        "expectation_context",
    ):
        if not isinstance(candidate.get(field), dict):
            raise KernelFileExchangeAdapterScaffoldError(
                f"candidate response {field} must be a JSON object"
            )

    if not isinstance(candidate.get("deferred_behavior_context"), list):
        raise KernelFileExchangeAdapterScaffoldError(
            "candidate response deferred_behavior_context must be a list"
        )

    if candidate.get("source_mapping_stage") != "kernel_intake_context_pre_runtime":
        raise KernelFileExchangeAdapterScaffoldError(
            "candidate response source_mapping_stage must be kernel_intake_context_pre_runtime"
        )

    return {
        "validated_response_type": "kernel_candidate_response_validation",
        "validated_response_state": "validated_pre_writer_non_terminal",
        "source_candidate": deepcopy(candidate),
        "response_writer_allowed": False,
        "failure_writer_allowed": False,
        "macro_report_unlock": False,
        "validation_stage": "candidate_response_validated_pre_writer",
    }


def validate_response_writer_input(validated_response: dict[str, Any]) -> dict[str, Any]:
    """Validate one local pre-writer response object for minimal response writing.

    This accepts only the current R10 local validation output. The
    `response_writer_allowed == False` marker is expected here because it means
    the object has not already crossed a writer boundary; this R14 boundary is
    the only place that may write the response artifact.
    """

    validated_response = _require_object(validated_response, "validated_response")

    missing = sorted(VALIDATED_RESPONSE_REQUIRED_FIELDS.difference(validated_response))
    if missing:
        raise KernelFileExchangeAdapterScaffoldError(
            f"validated response missing required fields: {missing}"
        )

    expected_markers = {
        "validated_response_type": "kernel_candidate_response_validation",
        "validated_response_state": "validated_pre_writer_non_terminal",
        "response_writer_allowed": False,
        "failure_writer_allowed": False,
        "macro_report_unlock": False,
        "validation_stage": "candidate_response_validated_pre_writer",
    }
    for field, expected in expected_markers.items():
        if validated_response.get(field) != expected:
            raise KernelFileExchangeAdapterScaffoldError(
                f"validated response {field} must be {expected!r}"
            )

    leaked_fields = sorted(FORBIDDEN_RESPONSE_WRITER_INPUT_FIELDS.intersection(validated_response))
    if leaked_fields:
        raise KernelFileExchangeAdapterScaffoldError(
            "validated response must not contain writer or terminal fields: "
            f"{leaked_fields}"
        )

    source_candidate = _require_object(
        validated_response.get("source_candidate"),
        "validated response source_candidate",
    )
    validate_candidate_response(source_candidate)

    return validated_response


def classify_blocking_failure(failure_source: dict[str, Any]) -> dict[str, Any]:
    """Classify one local blocking failure source before failure writing.

    This boundary produces a pre-writer classified failure object only. It does
    not write failure artifacts, call terminal writers, unlock reporting, emit
    CLI signals, or execute handoff.
    """

    failure_source = _require_object(failure_source, "failure_source")

    if failure_source.get("artifact_type") == "kernel_response":
        raise KernelFileExchangeAdapterScaffoldError(
            "response artifacts are not valid blocking failure classification input"
        )

    if failure_source.get("artifact_type") == "kernel_exchange_failure":
        raise KernelFileExchangeAdapterScaffoldError(
            "failure artifacts are not valid blocking failure classification input"
        )

    missing = sorted(BLOCKING_FAILURE_SOURCE_REQUIRED_FIELDS.difference(failure_source))
    if missing:
        raise KernelFileExchangeAdapterScaffoldError(
            f"failure source missing required fields: {missing}"
        )

    if failure_source.get("failure_stage") not in ALLOWED_BLOCKING_FAILURE_STAGES:
        raise KernelFileExchangeAdapterScaffoldError(
            f"unknown blocking failure stage: {failure_source.get('failure_stage')!r}"
        )

    for field in (
        "source_boundary",
        "failure_stage",
        "failure_code",
        "failure_message",
    ):
        if not isinstance(failure_source.get(field), str) or not failure_source[field].strip():
            raise KernelFileExchangeAdapterScaffoldError(
                f"failure source {field} must be a non-empty string"
            )

    true_terminal_markers = [
        field
        for field in (
            "terminal_artifact_written",
            "response_artifact_written",
            "failure_artifact_written",
            "macro_report_unlock",
        )
        if failure_source.get(field) is True
    ]
    if true_terminal_markers:
        raise KernelFileExchangeAdapterScaffoldError(
            "failure source must remain pre-writer and locked: "
            f"{sorted(true_terminal_markers)}"
        )

    leaked_fields = sorted(FORBIDDEN_BLOCKING_FAILURE_SOURCE_FIELDS.intersection(failure_source))
    if leaked_fields:
        raise KernelFileExchangeAdapterScaffoldError(
            "failure source must not contain terminal, reporting, CLI, or handoff fields: "
            f"{leaked_fields}"
        )

    return {
        "failure_type": "kernel_blocking_failure",
        "classified_failure_type": "kernel_blocking_failure",
        "classified_failure_state": "classified_blocking_failure_pre_writer",
        "failure_stage": failure_source["failure_stage"],
        "failure_code": failure_source["failure_code"],
        "failure_message": failure_source["failure_message"],
        "source_boundary": failure_source["source_boundary"],
        "is_blocking": True,
        "terminal_artifact_written": False,
        "response_artifact_written": False,
        "failure_artifact_written": False,
        "macro_report_unlock": False,
        "classification_stage": "blocking_failure_classified_pre_writer",
    }


def validate_failure_writer_input(classified_failure: dict[str, Any]) -> dict[str, Any]:
    """Validate one classified blocking failure object for minimal writing."""

    classified_failure = _require_object(classified_failure, "classified_failure")

    if classified_failure.get("artifact_type") == "kernel_response":
        raise KernelFileExchangeAdapterScaffoldError(
            "response artifacts are not valid failure writer input"
        )

    if classified_failure.get("artifact_type") == "kernel_exchange_failure":
        raise KernelFileExchangeAdapterScaffoldNotImplementedError(
            "failure artifacts are not valid failure writer input"
        )

    missing = sorted(CLASSIFIED_FAILURE_REQUIRED_FIELDS.difference(classified_failure))
    if missing:
        raise KernelFileExchangeAdapterScaffoldError(
            f"classified failure missing required fields: {missing}"
        )

    expected_markers = {
        "failure_type": "kernel_blocking_failure",
        "classified_failure_type": "kernel_blocking_failure",
        "classified_failure_state": "classified_blocking_failure_pre_writer",
        "is_blocking": True,
        "terminal_artifact_written": False,
        "response_artifact_written": False,
        "failure_artifact_written": False,
        "macro_report_unlock": False,
        "classification_stage": "blocking_failure_classified_pre_writer",
    }
    for field, expected in expected_markers.items():
        if classified_failure.get(field) != expected:
            raise KernelFileExchangeAdapterScaffoldError(
                f"classified failure {field} must be {expected!r}"
            )

    if classified_failure.get("failure_stage") not in ALLOWED_BLOCKING_FAILURE_STAGES:
        raise KernelFileExchangeAdapterScaffoldError(
            f"unknown blocking failure stage: {classified_failure.get('failure_stage')!r}"
        )

    for field in (
        "failure_stage",
        "failure_code",
        "failure_message",
        "source_boundary",
    ):
        if not isinstance(classified_failure.get(field), str) or not classified_failure[field].strip():
            raise KernelFileExchangeAdapterScaffoldError(
                f"classified failure {field} must be a non-empty string"
            )

    leaked_fields = sorted(FORBIDDEN_FAILURE_WRITER_INPUT_FIELDS.intersection(classified_failure))
    if leaked_fields:
        raise KernelFileExchangeAdapterScaffoldError(
            "classified failure must not contain artifact, writer, reporting, CLI, or handoff fields: "
            f"{leaked_fields}"
        )

    return classified_failure


def _iter_nested_items(value: Any) -> Any:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key, nested
            yield from _iter_nested_items(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _iter_nested_items(nested)


def _reject_terminal_dry_run_broadening_markers(value: dict[str, Any], label: str) -> None:
    leaked = sorted(
        {
            key
            for key, _ in _iter_nested_items(value)
            if key in FORBIDDEN_TERMINAL_DRY_RUN_MARKER_FIELDS
        }
    )
    if leaked:
        raise KernelFileExchangeAdapterScaffoldError(
            f"{label} must not contain CLI, handoff, reporting, scheduler, queue, polling, retry, or cleanup markers: "
            f"{leaked}"
        )

    true_markers = sorted(
        {
            key
            for key, nested in _iter_nested_items(value)
            if key in FORBIDDEN_TERMINAL_DRY_RUN_TRUE_FIELDS and nested is True
        }
    )
    if true_markers:
        raise KernelFileExchangeAdapterScaffoldError(
            f"{label} must remain pre-writer and locked: {true_markers}"
        )


def dry_run_terminal_writers(
    response_input: dict[str, Any],
    failure_input: dict[str, Any],
) -> dict[str, Any]:
    """Exercise local response and failure terminal writer branches as dry-run candidates.

    This dry-run is deterministic and local-only. It validates the current
    response and failure writer inputs, returns artifact candidates, and states
    that only one terminal artifact may be produced by any single future
    invocation. It does not write files, discover queues, poll, retry, clean up,
    add CLI behavior, unlock macro reporting, or execute handoff.
    """

    response_input = _require_object(response_input, "response_input")
    failure_input = _require_object(failure_input, "failure_input")

    if response_input.get("artifact_type") == "kernel_response":
        raise KernelFileExchangeAdapterScaffoldError(
            "response artifacts are not valid terminal writer dry-run response input"
        )
    if response_input.get("artifact_type") == "kernel_exchange_failure":
        raise KernelFileExchangeAdapterScaffoldError(
            "failure artifacts are not valid terminal writer dry-run response input"
        )
    if failure_input.get("artifact_type") == "kernel_response":
        raise KernelFileExchangeAdapterScaffoldError(
            "response artifacts are not valid terminal writer dry-run failure input"
        )
    if failure_input.get("artifact_type") == "kernel_exchange_failure":
        raise KernelFileExchangeAdapterScaffoldError(
            "failure artifacts are not valid terminal writer dry-run failure input"
        )

    _reject_terminal_dry_run_broadening_markers(response_input, "response_input")
    _reject_terminal_dry_run_broadening_markers(failure_input, "failure_input")

    validated_response = validate_response_writer_input(response_input)
    classified_failure = validate_failure_writer_input(failure_input)

    response_artifact_candidate = {
        "artifact_type": "kernel_response",
        "artifact_state": "dry_run_response_artifact_candidate",
        "source_validated_response": deepcopy(validated_response),
        "terminal_artifact_written": False,
        "response_writer_called": False,
        "failure_writer_called": False,
        "macro_report_unlock": False,
        "writer_stage": "response_writer_minimal_local_dry_run_candidate",
        "dry_run_branch_id": "response_terminal_writer_branch",
        "single_invocation_terminal_artifact_count": 1,
    }
    failure_artifact_candidate = {
        "artifact_type": "kernel_exchange_failure",
        "artifact_state": "dry_run_failure_artifact_candidate",
        "blocking": True,
        "source_classified_failure": deepcopy(classified_failure),
        "terminal_artifact_written": False,
        "response_writer_called": False,
        "failure_writer_called": False,
        "macro_report_unlock": False,
        "writer_stage": "failure_writer_minimal_local_dry_run_candidate",
        "dry_run_branch_id": "failure_terminal_writer_branch",
        "single_invocation_terminal_artifact_count": 1,
    }

    return {
        "dry_run_type": "local_terminal_writer_dry_run",
        "dry_run_state": "completed_pre_orchestration",
        "dry_run_stage": "terminal_writer_dry_run_minimal_local",
        "response_path_checked": True,
        "failure_path_checked": True,
        "mutual_exclusivity_required": True,
        "dual_write_for_single_invocation_allowed": False,
        "single_invocation_may_produce_only_one_terminal_artifact": True,
        "macro_report_unlock": False,
        "cli_behavior_added": False,
        "actual_handoff_executed": False,
        "terminal_artifact_written": False,
        "response_artifact_candidate": response_artifact_candidate,
        "failure_artifact_candidate": failure_artifact_candidate,
    }


def validate_kernel_response(task_object: dict[str, Any]) -> dict[str, Any]:
    """Validate a provided kernel response object against TASK_OBJECT_SCHEMA.

    This boundary validates only a caller-provided object. It does not create,
    repair, or write canonical task objects.
    """

    task_object = _require_object(task_object, "task_object")
    if Draft202012Validator is None:
        raise KernelFileExchangeAdapterScaffoldError(
            "jsonschema is required for TASK_OBJECT_SCHEMA validation"
        )

    schema = read_json_object(TASK_OBJECT_SCHEMA, "task object schema")
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(task_object), key=lambda error: list(error.path))
    if errors:
        details = [
            f"{list(error.path) or '<root>'}: {error.message}"
            for error in errors
        ]
        raise KernelFileExchangeAdapterScaffoldError(
            "kernel response schema validation failed: " + "; ".join(details)
        )

    return task_object


def read_json_object(path: str | Path, label: str) -> dict[str, Any]:
    """Read a local JSON object for scaffold validation boundaries."""

    json_path = Path(path)
    if not json_path.is_file():
        raise KernelFileExchangeAdapterScaffoldError(
            f"{label} does not exist or is not a file: {json_path}"
        )

    with json_path.open("r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as exc:
            raise KernelFileExchangeAdapterScaffoldError(
                f"{label} is not valid JSON: {json_path}"
            ) from exc

    return _require_object(data, label)


def write_response_artifact(task_object: dict[str, Any], destination: str | Path) -> dict[str, Any]:
    """Write one local response artifact from one validated pre-writer response.

    This is the minimal R14 response writer boundary. It writes exactly one
    local JSON artifact to an explicit destination and stops before failure
    writing, CLI behavior, macro report unlock, scheduler behavior, and handoff.
    """

    validated_response = validate_response_writer_input(task_object)
    artifact_path = Path(destination)

    if artifact_path.exists():
        if artifact_path.is_dir():
            raise KernelFileExchangeAdapterScaffoldError(
                f"response artifact destination is a directory: {artifact_path}"
            )
        raise KernelFileExchangeAdapterScaffoldError(
            f"response artifact destination already exists: {artifact_path}"
        )

    if not artifact_path.parent.is_dir():
        raise KernelFileExchangeAdapterScaffoldError(
            f"response artifact destination parent does not exist: {artifact_path.parent}"
        )

    response_artifact = {
        "artifact_type": "kernel_response",
        "artifact_version": "0.1.0",
        "artifact_state": "written_response_artifact",
        "source_validated_response": deepcopy(validated_response),
        "terminal_artifact_written": True,
        "response_writer_called": True,
        "failure_writer_called": False,
        "macro_report_unlock": False,
        "writer_stage": "response_writer_minimal_local_artifact",
    }

    with artifact_path.open("w", encoding="utf-8") as file:
        json.dump(response_artifact, file, indent=2, sort_keys=True)
        file.write("\n")

    return response_artifact


def write_failure_artifact(failure: dict[str, Any], destination: str | Path) -> dict[str, Any]:
    """Write one local failure artifact from one classified blocking failure."""

    classified_failure = validate_failure_writer_input(failure)
    artifact_path = Path(destination)

    if artifact_path.exists():
        if artifact_path.is_dir():
            raise KernelFileExchangeAdapterScaffoldError(
                f"failure artifact destination is a directory: {artifact_path}"
            )
        raise KernelFileExchangeAdapterScaffoldError(
            f"failure artifact destination already exists: {artifact_path}"
        )

    if not artifact_path.parent.is_dir():
        raise KernelFileExchangeAdapterScaffoldError(
            f"failure artifact destination parent does not exist: {artifact_path.parent}"
        )

    failure_artifact = {
        "artifact_type": "kernel_exchange_failure",
        "artifact_version": "0.1.0",
        "artifact_state": "written_failure_artifact",
        "blocking": True,
        "source_classified_failure": deepcopy(classified_failure),
        "terminal_artifact_written": True,
        "response_writer_called": False,
        "failure_writer_called": True,
        "macro_report_unlock": False,
        "writer_stage": "failure_writer_minimal_local_artifact",
    }

    with artifact_path.open("w", encoding="utf-8") as file:
        json.dump(failure_artifact, file, indent=2, sort_keys=True)
        file.write("\n")

    return failure_artifact


def invoke_local_adapter(
    envelope_path: str | Path,
    output_destination_policy: dict[str, Any],
) -> dict[str, Any]:
    """Run one explicit local envelope through the minimal adapter boundaries.

    This is a bounded local composition of existing scaffold boundaries. It
    reads one explicit envelope, prepares intake context, produces a
    candidate-only response, validates that response, selects exactly one
    terminal path, and writes either one response artifact or one failure
    artifact. It does not discover queues, poll, retry, clean up artifacts,
    add CLI behavior, unlock macro reporting, or execute handoff.
    """

    source_path = _require_explicit_local_path(envelope_path, "envelope_path")
    destinations = _validate_output_destination_policy(output_destination_policy)

    def write_blocking_failure(
        *,
        source_boundary: str,
        failure_stage: str,
        failure_code: str,
        failure_message: str,
    ) -> dict[str, Any]:
        failure_source = _blocking_failure_source(
            source_boundary=source_boundary,
            failure_stage=failure_stage,
            failure_code=failure_code,
            failure_message=failure_message,
        )
        classified = classify_blocking_failure(failure_source)
        write_failure_artifact(classified, destinations["failure_artifact_path"])
        return _local_invocation_result(
            source_envelope_path=source_path,
            selected_terminal_path="failure",
            response_artifact_path=None,
            failure_artifact_path=destinations["failure_artifact_path"],
            terminal_artifact_written=True,
            response_writer_called=False,
            failure_writer_called=True,
        )

    try:
        envelope = read_envelope_artifact(source_path)
    except KernelFileExchangeAdapterScaffoldError as exc:
        return write_blocking_failure(
            source_boundary="reader_boundary",
            failure_stage="reader",
            failure_code="reader_failed",
            failure_message=str(exc),
        )

    try:
        validated_envelope = validate_envelope_intake(envelope)
    except KernelFileExchangeAdapterScaffoldError as exc:
        return write_blocking_failure(
            source_boundary="envelope_validation_boundary",
            failure_stage="envelope_validation",
            failure_code="envelope_validation_failed",
            failure_message=str(exc),
        )

    try:
        intake = prepare_kernel_intake(validated_envelope)
    except KernelFileExchangeAdapterScaffoldError as exc:
        return write_blocking_failure(
            source_boundary="intake_mapping_boundary",
            failure_stage="intake_mapping",
            failure_code="intake_mapping_failed",
            failure_message=str(exc),
        )

    try:
        candidate = invoke_kernel_runtime(intake)
    except KernelFileExchangeAdapterScaffoldError as exc:
        return write_blocking_failure(
            source_boundary="runtime_invocation_boundary",
            failure_stage="runtime_invocation",
            failure_code="runtime_invocation_failed",
            failure_message=str(exc),
        )

    try:
        validated_response = validate_candidate_response(candidate)
    except KernelFileExchangeAdapterScaffoldError as exc:
        return write_blocking_failure(
            source_boundary="response_validation_boundary",
            failure_stage="response_validation",
            failure_code="response_validation_failed",
            failure_message=str(exc),
        )

    try:
        write_response_artifact(
            validated_response,
            destinations["response_artifact_path"],
        )
    except KernelFileExchangeAdapterScaffoldError as exc:
        return write_blocking_failure(
            source_boundary="response_writer_boundary",
            failure_stage="response_writer",
            failure_code="response_writer_failed",
            failure_message=str(exc),
        )

    return _local_invocation_result(
        source_envelope_path=source_path,
        selected_terminal_path="response",
        response_artifact_path=destinations["response_artifact_path"],
        failure_artifact_path=None,
        terminal_artifact_written=True,
        response_writer_called=True,
        failure_writer_called=False,
    )
