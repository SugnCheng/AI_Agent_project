"""Read a daily_us_core kernel response or failure artifact for file exchange.

This scaffold reads local file-based exchange artifacts only. It does not
invoke ai-meta-kernel runtime, generate kernel responses, compose reports,
fetch live sources, call external services, or mutate runtime artifacts.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"
RUNTIME_EXCHANGE_ROOT = PROJECT_ROOT / "runtime" / "kernel_exchange"
RESPONSE_DIR = RUNTIME_EXCHANGE_ROOT / "responses"
FAILURE_DIR = RUNTIME_EXCHANGE_ROOT / "failures"
BOUNDARY_SCRIPT = PROJECT_ROOT / "workflows" / "daily_us_core_kernel_runtime_boundary.py"

PROFILE_ID = "daily_us_core"
RUN_MODE = "daily_brief_run"
REPORT_TARGET = "daily_brief"
TIMESTAMP_PATTERN = re.compile(r"^\d{8}T\d{6}Z$")
VALID_FAILURE_STAGES = {
    "pre_invoke",
    "invoke",
    "response_parse",
    "response_schema_validation",
    "response_state_validation",
}


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> Any:
    """Load JSON artifact from disk."""

    return json.loads(path.read_text(encoding="utf-8"))


def resolve_path(path_value: str) -> Path:
    """Resolve absolute or repo-relative paths."""

    path = Path(path_value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def repo_relative(path: Path | None) -> str | None:
    """Return a repo-relative path string when possible."""

    if path is None:
        return None
    try:
        return str(path.resolve().relative_to(REPO_ROOT.resolve()))
    except ValueError:
        return str(path)


def parse_exchange_filename(path: Path) -> dict[str, str]:
    """Parse governed file-exchange artifact filename parts."""

    name = path.name
    if not name.endswith(".json"):
        raise ValueError("artifact filename must end with .json")
    stem = name[:-5]
    parts = stem.split("__")
    if len(parts) != 5:
        raise ValueError("artifact filename must contain five __ separated parts")
    profile_id, run_mode, report_target, timestamp, artifact_kind = parts
    if profile_id != PROFILE_ID:
        raise ValueError(f"profile_id must be {PROFILE_ID}")
    if run_mode != RUN_MODE:
        raise ValueError(f"run_mode must be {RUN_MODE}")
    if report_target != REPORT_TARGET:
        raise ValueError(f"report_target must be {REPORT_TARGET}")
    if not TIMESTAMP_PATTERN.match(timestamp):
        raise ValueError("timestamp must use YYYYMMDDTHHMMSSZ format")
    if artifact_kind not in {"kernel_input_envelope", "kernel_response", "kernel_failure"}:
        raise ValueError("artifact_kind must be kernel_input_envelope, kernel_response, or kernel_failure")
    return {
        "profile_id": profile_id,
        "run_mode": run_mode,
        "report_target": report_target,
        "timestamp": timestamp,
        "artifact_kind": artifact_kind,
    }


def base_stem_from_path_or_stem(value: str) -> str:
    """Return the shared artifact stem without the artifact kind."""

    candidate = Path(value).name
    if candidate.endswith(".json"):
        candidate = candidate[:-5]
    parts = candidate.split("__")
    if len(parts) == 5:
        artifact_kind = parts[-1]
        if artifact_kind not in {"kernel_input_envelope", "kernel_response", "kernel_failure"}:
            raise ValueError("artifact_kind must be kernel_input_envelope, kernel_response, or kernel_failure")
        parts = parts[:-1]
    if len(parts) != 4:
        raise ValueError("artifact stem must contain profile_id, run_mode, report_target, and timestamp")
    profile_id, run_mode, report_target, timestamp = parts
    if profile_id != PROFILE_ID or run_mode != RUN_MODE or report_target != REPORT_TARGET:
        raise ValueError("artifact stem does not match daily_us_core governed slice")
    if not TIMESTAMP_PATTERN.match(timestamp):
        raise ValueError("timestamp must use YYYYMMDDTHHMMSSZ format")
    return "__".join(parts)


def paths_from_base_stem(base_stem: str) -> tuple[Path, Path]:
    """Build response and failure paths for the shared artifact stem."""

    response_path = RESPONSE_DIR / f"{base_stem}__kernel_response.json"
    failure_path = FAILURE_DIR / f"{base_stem}__kernel_failure.json"
    return response_path, failure_path


def load_boundary_module() -> Any:
    """Load existing kernel response validation helpers."""

    return load_module("daily_us_core_kernel_runtime_boundary", BOUNDARY_SCRIPT)


def validate_failure_artifact(failure: Any) -> dict[str, Any]:
    """Validate v0.1 failure artifact shape and keep reporting blocked."""

    errors: list[str] = []
    if not isinstance(failure, dict):
        errors.append("failure artifact must be object-like")
    else:
        if failure.get("artifact_type") != "kernel_exchange_failure":
            errors.append("artifact_type must be kernel_exchange_failure")
        if failure.get("blocking") is not True:
            errors.append("blocking must be true for v0.1 failure artifacts")
        if failure.get("failure_stage") not in VALID_FAILURE_STAGES:
            errors.append("failure_stage is missing or invalid")
        if not isinstance(failure.get("failure_reason"), str) or not failure.get("failure_reason"):
            errors.append("failure_reason is required")

    return {
        "kernel_response_validation": "not_applicable",
        "kernel_response_state": "blocked",
        "blocking_reasons": errors or ["kernel failure artifact present"],
        "restricting_reasons": [],
        "downstream_reporting_allowed": False,
        "downstream_reporting_mode": "blocked",
    }


def response_decision(response_path: Path) -> dict[str, Any]:
    """Validate a response artifact and return downstream decision fields."""

    try:
        response = load_json(response_path)
    except json.JSONDecodeError as exc:
        decision = blocked_decision(f"response artifact is not valid JSON: {exc}", "kernel_response")
        decision["kernel_response_validation"] = "failed"
        return decision

    boundary = load_boundary_module()
    validation = boundary.validate_future_kernel_response(response)
    state = validation["kernel_response_state"]
    reporting_allowed = validation["downstream_reporting_allowed"] and state in {"standard", "restricted"}
    if validation["kernel_response_validation"] != "ok":
        state = "blocked"
        reporting_allowed = False

    return {
        "kernel_response_validation": validation["kernel_response_validation"],
        "schema_error_count": validation["schema_error_count"],
        "schema_errors": validation["schema_errors"],
        "kernel_response_state": state,
        "blocking_reasons": validation["blocking_reasons"],
        "restricting_reasons": validation["restricting_reasons"],
        "downstream_reporting_allowed": reporting_allowed,
        "downstream_reporting_mode": state,
    }


def blocked_decision(reason: str, artifact_kind: str | None = None) -> dict[str, Any]:
    """Build a blocked downstream decision."""

    return {
        "kernel_response_validation": "not_run",
        "schema_error_count": 0,
        "schema_errors": [],
        "kernel_response_state": "blocked",
        "blocking_reasons": [reason],
        "restricting_reasons": [],
        "downstream_reporting_allowed": False,
        "downstream_reporting_mode": "blocked",
        "artifact_kind": artifact_kind,
    }


def classify_explicit_response(response_path: Path) -> dict[str, Any]:
    """Read and classify an explicit response artifact path."""

    if not response_path.exists():
        return {
            "artifact_match_status": "missing_explicit_response_artifact",
            "response_artifact_path": response_path,
            "failure_artifact_path": None,
            **blocked_decision("explicit response artifact not found", "kernel_response"),
        }
    return {
        "artifact_match_status": "explicit_response",
        "artifact_kind": "kernel_response",
        "response_artifact_path": response_path,
        "failure_artifact_path": None,
        **response_decision(response_path),
    }


def classify_explicit_failure(failure_path: Path) -> dict[str, Any]:
    """Read and classify an explicit failure artifact path."""

    if not failure_path.exists():
        return {
            "artifact_match_status": "missing_explicit_failure_artifact",
            "response_artifact_path": None,
            "failure_artifact_path": failure_path,
            **blocked_decision("explicit failure artifact not found", "kernel_failure"),
        }
    try:
        failure = load_json(failure_path)
    except json.JSONDecodeError as exc:
        return {
            "artifact_match_status": "explicit_failure",
            "artifact_kind": "kernel_failure",
            "response_artifact_path": None,
            "failure_artifact_path": failure_path,
            **blocked_decision(f"failure artifact is not valid JSON: {exc}", "kernel_failure"),
        }
    return {
        "artifact_match_status": "explicit_failure",
        "artifact_kind": "kernel_failure",
        "response_artifact_path": None,
        "failure_artifact_path": failure_path,
        **validate_failure_artifact(failure),
    }


def classify_matching_artifacts(base_stem: str) -> dict[str, Any]:
    """Find matching response/failure artifacts for a shared envelope stem."""

    response_path, failure_path = paths_from_base_stem(base_stem)
    response_exists = response_path.exists()
    failure_exists = failure_path.exists()

    if response_exists and failure_exists:
        return {
            "artifact_match_status": "both_response_and_failure",
            "artifact_kind": "ambiguous",
            "response_artifact_path": response_path,
            "failure_artifact_path": failure_path,
            **blocked_decision("both response and failure artifacts exist for the same stem", "ambiguous"),
        }
    if failure_exists:
        return classify_explicit_failure(failure_path) | {"artifact_match_status": "failure_only"}
    if response_exists:
        return classify_explicit_response(response_path) | {"artifact_match_status": "response_only"}

    return {
        "artifact_match_status": "no_matching_artifact",
        "artifact_kind": None,
        "response_artifact_path": response_path,
        "failure_artifact_path": failure_path,
        **blocked_decision("no matching response or failure artifact found"),
    }


def read_kernel_exchange_response(
    response_artifact: str | None = None,
    failure_artifact: str | None = None,
    envelope_artifact: str | None = None,
    artifact_stem: str | None = None,
) -> dict[str, Any]:
    """Read response/failure artifact input and emit compact decision."""

    provided = [
        value is not None for value in (response_artifact, failure_artifact, envelope_artifact, artifact_stem)
    ]
    if sum(provided) != 1:
        raise ValueError("provide exactly one of response_artifact, failure_artifact, envelope_artifact, artifact_stem")

    if response_artifact:
        decision = classify_explicit_response(resolve_path(response_artifact))
    elif failure_artifact:
        decision = classify_explicit_failure(resolve_path(failure_artifact))
    else:
        stem_source = envelope_artifact if envelope_artifact is not None else artifact_stem
        assert stem_source is not None
        if envelope_artifact is not None:
            envelope_path = resolve_path(envelope_artifact)
            if not envelope_path.exists():
                base_stem = base_stem_from_path_or_stem(stem_source)
                decision = {
                    "artifact_match_status": "missing_envelope_artifact",
                    "artifact_kind": None,
                    "response_artifact_path": None,
                    "failure_artifact_path": None,
                    **blocked_decision("explicit envelope artifact not found"),
                }
            else:
                parsed = parse_exchange_filename(envelope_path)
                if parsed["artifact_kind"] != "kernel_input_envelope":
                    raise ValueError("envelope artifact must have artifact_kind kernel_input_envelope")
                base_stem = base_stem_from_path_or_stem(envelope_path.name)
                decision = classify_matching_artifacts(base_stem)
        else:
            base_stem = base_stem_from_path_or_stem(stem_source)
            decision = classify_matching_artifacts(base_stem)

    artifact_kind = decision.get("artifact_kind")
    return {
        "kernel_exchange_read_response_status": "ok",
        "artifact_match_status": decision["artifact_match_status"],
        "artifact_kind": artifact_kind,
        "response_artifact_path": repo_relative(decision.get("response_artifact_path")),
        "failure_artifact_path": repo_relative(decision.get("failure_artifact_path")),
        "kernel_response_validation": decision["kernel_response_validation"],
        "schema_error_count": decision.get("schema_error_count", 0),
        "schema_errors": decision.get("schema_errors", []),
        "kernel_response_state": decision["kernel_response_state"],
        "blocking_reasons": decision["blocking_reasons"],
        "restricting_reasons": decision["restricting_reasons"],
        "downstream_reporting_allowed": decision["downstream_reporting_allowed"],
        "downstream_reporting_mode": decision["downstream_reporting_mode"],
        "kernel_runtime_invocation_performed": False,
        "canonical_task_object_generated_locally": False,
        "report_composition_performed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read a daily_us_core file-based kernel response or failure artifact without invoking kernel."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--response-artifact", help="Explicit kernel_response JSON artifact path.")
    group.add_argument("--failure-artifact", help="Explicit kernel_failure JSON artifact path.")
    group.add_argument("--envelope-artifact", help="Explicit kernel_input_envelope JSON artifact path.")
    group.add_argument("--artifact-stem", help="Shared artifact stem without artifact kind, or full artifact filename.")
    args = parser.parse_args()

    result = read_kernel_exchange_response(
        response_artifact=args.response_artifact,
        failure_artifact=args.failure_artifact,
        envelope_artifact=args.envelope_artifact,
        artifact_stem=args.artifact_stem,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
