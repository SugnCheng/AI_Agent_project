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


class KernelFileExchangeAdapterScaffoldError(ValueError):
    """Raised when scaffold boundary validation fails."""


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise KernelFileExchangeAdapterScaffoldError(f"{label} must be a JSON object")
    return value


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


def write_failure_artifact(failure: dict[str, Any], destination: str | Path) -> None:
    """Future blocking failure writer boundary.

    Failure writing remains blocked until a governed implementation pass.
    """

    _require_object(failure, "failure")
    Path(destination)
    raise NotImplementedError(
        "Failure artifact writing is intentionally not implemented in this scaffold."
    )
