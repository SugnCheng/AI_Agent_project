"""Local kernel runtime boundary scaffold for daily_us_core v0.1.

This helper prepares the boundary for a future ai-meta-kernel runtime call.
It does not invoke the kernel, does not generate a canonical kernel task
object, and does not allow downstream reporting to continue.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"
KERNEL_TASK_SCHEMA_PATH = REPO_ROOT / "ai-meta-kernel" / "meta-layer" / "TASK_OBJECT_SCHEMA.json"

BLOCKING_STATUS_FLAGS = {
    "needs_reframe",
    "needs_user_clarification",
}
RESTRICTING_STATUS_FLAGS = {
    "needs_verification",
    "needs_user_alignment",
    "high_risk_restricted",
    "ethics_escalated",
}
BLOCKING_CHALLENGE_RESULTS = {
    "clarify_first",
    "reframe_first",
    "escalate",
    "decline",
}
ALLOWED_HANDOFF_MODES = {
    "standard_handoff",
    "restricted_handoff",
    "do_not_handoff",
}


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_kernel_input_envelope() -> dict[str, Any]:
    """Reuse the current fixture kernel input envelope helper."""

    envelope_module = load_module(
        "daily_us_core_fixture_kernel_input_envelope",
        PROJECT_ROOT / "workflows" / "daily_us_core_fixture_kernel_input_envelope.py",
    )
    result = envelope_module.run_fixture_kernel_input_envelope(include_envelope=True)
    if result.get("canonical_task_object_generated") is not False:
        raise ValueError("macro agent must not generate a canonical kernel task object")
    if result.get("envelope_validation") != "ok":
        raise ValueError("kernel input envelope validation did not pass")
    envelope = result.get("kernel_input_envelope")
    if not isinstance(envelope, dict):
        raise ValueError("kernel input envelope is missing or not object-like")
    return envelope


def invoke_kernel_runtime(envelope: dict[str, Any]) -> dict[str, Any]:
    """Future ai-meta-kernel runtime invocation boundary.

    The macro agent must not synthesize a kernel response locally. This function
    intentionally raises until a governed kernel runtime integration is approved.
    """

    if not isinstance(envelope, dict):
        raise TypeError("kernel runtime envelope must be object-like")
    raise NotImplementedError("ai-meta-kernel runtime invocation is not implemented in v0.1")


def load_json(path: str | Path) -> Any:
    """Load JSON from disk for future kernel response validation."""

    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_kernel_task_schema() -> dict[str, Any]:
    """Load the upstream kernel task object schema."""

    schema = load_json(KERNEL_TASK_SCHEMA_PATH)
    if not isinstance(schema, dict):
        raise ValueError("kernel task schema must be object-like")
    return schema


def required_kernel_fields() -> list[str]:
    """Return top-level required fields from the upstream kernel schema."""

    required = load_kernel_task_schema().get("required")
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        raise ValueError("kernel schema required fields must be a string array")
    return required


def validate_kernel_response_shape(response: Any) -> list[str]:
    """Validate object-likeness and required top-level kernel fields."""

    errors: list[str] = []
    if not isinstance(response, dict):
        return ["kernel response must be object-like"]

    for field in required_kernel_fields():
        if field not in response:
            errors.append(f"missing required kernel field '{field}'")

    return errors


def validate_kernel_response_schema(response: Any) -> list[str]:
    """Validate a future kernel response against TASK_OBJECT_SCHEMA.json."""

    shape_errors = validate_kernel_response_shape(response)
    if shape_errors:
        return shape_errors

    try:
        from jsonschema import Draft202012Validator
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "jsonschema is required for kernel response schema validation. "
            "Install dependencies from macro-financial-intelligence-agent/requirements.txt."
        ) from exc

    schema = load_kernel_task_schema()
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(response), key=lambda error: list(error.path))
    return [_format_schema_error(error) for error in errors]


def detect_blocked_or_restricted_state(response: Any) -> dict[str, Any]:
    """Detect whether a future kernel response blocks or restricts reporting."""

    if not isinstance(response, dict):
        return {
            "kernel_response_state": "blocked",
            "blocking_reasons": ["kernel response must be object-like"],
            "restricting_reasons": [],
            "downstream_reporting_allowed": False,
        }

    status_flags = set(response.get("status_flags", []))
    downstream_recommendation = response.get("downstream_recommendation", {})
    handoff = response.get("handoff", {})
    challenge_loop = response.get("challenge_loop", {})

    mode = downstream_recommendation.get("mode")
    challenge_result = challenge_loop.get("result")
    blocking_reasons: list[str] = []
    restricting_reasons: list[str] = []

    for flag in sorted(status_flags.intersection(BLOCKING_STATUS_FLAGS)):
        blocking_reasons.append(f"blocking status flag: {flag}")
    for flag in sorted(status_flags.intersection(RESTRICTING_STATUS_FLAGS)):
        restricting_reasons.append(f"restricting status flag: {flag}")

    if mode == "do_not_handoff":
        blocking_reasons.append("downstream_recommendation.mode is do_not_handoff")
    elif mode not in ALLOWED_HANDOFF_MODES:
        blocking_reasons.append("downstream_recommendation.mode is missing or invalid")

    if handoff.get("handoff_ready") is not True:
        blocking_reasons.append("handoff.handoff_ready is not true")

    if challenge_result in BLOCKING_CHALLENGE_RESULTS:
        blocking_reasons.append(f"challenge_loop.result is {challenge_result}")

    state = "standard"
    if blocking_reasons:
        state = "blocked"
    elif mode == "restricted_handoff" or restricting_reasons:
        state = "restricted"

    return {
        "kernel_response_state": state,
        "blocking_reasons": blocking_reasons,
        "restricting_reasons": restricting_reasons,
        "downstream_reporting_allowed": state in {"standard", "restricted"},
    }


def validate_future_kernel_response(response: Any) -> dict[str, Any]:
    """Run local validation checks for a future kernel-produced task object."""

    schema_errors = validate_kernel_response_schema(response)
    state = detect_blocked_or_restricted_state(response)
    return {
        "kernel_response_validation": "ok" if not schema_errors else "failed",
        "schema_error_count": len(schema_errors),
        "schema_errors": schema_errors,
        **state,
    }


def build_boundary_summary() -> dict[str, Any]:
    """Build compact developer-facing boundary status without invoking kernel."""

    envelope = load_kernel_input_envelope()
    return {
        "kernel_runtime_boundary_status": "prepared",
        "source_project": "macro-financial-intelligence-agent",
        "profile_id": envelope["profile_id"],
        "run_mode": envelope["run_mode"],
        "report_target": envelope["report_target"],
        "regions": envelope["regions"],
        "envelope_type": envelope["envelope_type"],
        "envelope_version": envelope["envelope_version"],
        "kernel_invocation_implemented": False,
        "canonical_task_object_generated_locally": False,
        "future_kernel_response_validation_available": True,
        "downstream_reporting_blocked": True,
        "deferred_runtime_behavior": sorted(
            set(envelope["deferred_runtime_behavior"])
            | {
                "actual_ai_meta_kernel_runtime_invocation",
                "kernel_response_consumption",
                "downstream_macro_reporting",
            }
        ),
    }


def _format_schema_error(error: Any) -> str:
    path = ".".join(str(part) for part in error.path)
    location = path if path else "<root>"
    return f"{location}: {error.message}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare the daily_us_core kernel runtime boundary without invoking kernel."
    )
    parser.add_argument(
        "--kernel-response-json",
        help="Optional future kernel response JSON file to validate against the upstream schema.",
    )
    args = parser.parse_args()

    result = build_boundary_summary()
    if args.kernel_response_json:
        response = load_json(args.kernel_response_json)
        result["future_kernel_response_check"] = validate_future_kernel_response(response)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
