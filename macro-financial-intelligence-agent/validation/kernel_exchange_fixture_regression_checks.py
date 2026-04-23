"""Validate file-based kernel exchange read-response fixture branches.

This local helper exercises static fixtures only. It does not invoke
ai-meta-kernel runtime, generate kernel responses, compose reports, fetch live
sources, execute schedules, or call external services.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"
READER_SCRIPT = PROJECT_ROOT / "workflows" / "daily_us_core_read_kernel_response_artifact.py"
RESPONSE_FIXTURE_ROOT = PROJECT_ROOT / "fixtures" / "kernel_responses"
FAILURE_FIXTURE_ROOT = PROJECT_ROOT / "fixtures" / "kernel_failures"

FIXTURE_CASES = (
    {
        "case": "standard_response",
        "input_type": "response_artifact",
        "path": RESPONSE_FIXTURE_ROOT / "daily_us_core_standard_kernel_response.example.json",
        "expected_state": "standard",
        "expected_allowed": True,
    },
    {
        "case": "restricted_response",
        "input_type": "response_artifact",
        "path": RESPONSE_FIXTURE_ROOT / "daily_us_core_restricted_kernel_response.example.json",
        "expected_state": "restricted",
        "expected_allowed": True,
    },
    {
        "case": "blocked_response",
        "input_type": "response_artifact",
        "path": RESPONSE_FIXTURE_ROOT / "daily_us_core_blocked_kernel_response.example.json",
        "expected_state": "blocked",
        "expected_allowed": False,
    },
    {
        "case": "failure_artifact",
        "input_type": "failure_artifact",
        "path": FAILURE_FIXTURE_ROOT / "daily_us_core_kernel_failure.example.json",
        "expected_state": "blocked",
        "expected_allowed": False,
    },
)


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def repo_relative(path: Path) -> str:
    """Return a repo-relative path string."""

    return str(path.relative_to(REPO_ROOT))


def run_case(reader: Any, case: dict[str, Any]) -> dict[str, Any]:
    """Run one governed fixture case through the read-response scaffold."""

    path = case["path"]
    if case["input_type"] == "response_artifact":
        result = reader.read_kernel_exchange_response(response_artifact=str(path))
    elif case["input_type"] == "failure_artifact":
        result = reader.read_kernel_exchange_response(failure_artifact=str(path))
    else:
        raise ValueError(f"unsupported input_type: {case['input_type']}")

    actual_state = result["kernel_response_state"]
    actual_allowed = result["downstream_reporting_allowed"]
    passed = actual_state == case["expected_state"] and actual_allowed is case["expected_allowed"]

    return {
        "case": case["case"],
        "input_type": case["input_type"],
        "path": repo_relative(path),
        "expected_state": case["expected_state"],
        "actual_state": actual_state,
        "expected_downstream_reporting_allowed": case["expected_allowed"],
        "actual_downstream_reporting_allowed": actual_allowed,
        "artifact_match_status": result["artifact_match_status"],
        "artifact_kind": result["artifact_kind"],
        "kernel_response_validation": result["kernel_response_validation"],
        "blocking_reason_count": len(result["blocking_reasons"]),
        "restricting_reason_count": len(result["restricting_reasons"]),
        "kernel_runtime_invocation_performed": result["kernel_runtime_invocation_performed"],
        "canonical_task_object_generated_locally": result["canonical_task_object_generated_locally"],
        "report_composition_performed": result["report_composition_performed"],
        "passed": passed,
    }


def validate_kernel_exchange_fixtures() -> dict[str, Any]:
    """Run all governed file-based exchange fixture regression cases."""

    reader = load_module("daily_us_core_read_kernel_response_artifact", READER_SCRIPT)
    results = [run_case(reader, case) for case in FIXTURE_CASES]
    failures = [
        (
            f"{result['case']}: expected {result['expected_state']} "
            f"/ allowed={result['expected_downstream_reporting_allowed']}, "
            f"got {result['actual_state']} "
            f"/ allowed={result['actual_downstream_reporting_allowed']}"
        )
        for result in results
        if not result["passed"]
    ]

    return {
        "kernel_exchange_fixture_regression_checks": "ok" if not failures else "failed",
        "fixture_count": len(results),
        "passed_count": sum(1 for result in results if result["passed"]),
        "failed_count": len(failures),
        "fixtures": results,
        "failures": failures,
        "runtime_invocation_performed": False,
        "kernel_responses_generated_locally": False,
        "report_composition_performed": False,
    }


def main() -> None:
    result = validate_kernel_exchange_fixtures()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["failures"]:
        raise SystemExit(1)
    print("kernel-exchange-fixture-regression-checks-ok")


if __name__ == "__main__":
    main()
