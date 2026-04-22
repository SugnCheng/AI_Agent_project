"""Validate governed kernel response fixtures against boundary semantics.

This local helper checks static fixture kernel responses only. It does not
invoke ai-meta-kernel runtime and does not generate kernel responses.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"
BOUNDARY_SCRIPT = PROJECT_ROOT / "workflows" / "daily_us_core_kernel_runtime_boundary.py"
FIXTURE_ROOT = PROJECT_ROOT / "fixtures" / "kernel_responses"

FIXTURE_EXPECTATIONS = (
    (
        "standard",
        FIXTURE_ROOT / "daily_us_core_standard_kernel_response.example.json",
        "standard",
    ),
    (
        "restricted",
        FIXTURE_ROOT / "daily_us_core_restricted_kernel_response.example.json",
        "restricted",
    ),
    (
        "blocked",
        FIXTURE_ROOT / "daily_us_core_blocked_kernel_response.example.json",
        "blocked",
    ),
)


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> Any:
    """Load a static JSON fixture."""

    return json.loads(path.read_text(encoding="utf-8"))


def validate_fixture_states() -> dict[str, Any]:
    """Validate fixture kernel responses and expected state classifications."""

    boundary = load_module("daily_us_core_kernel_runtime_boundary", BOUNDARY_SCRIPT)
    results: list[dict[str, Any]] = []
    failures: list[str] = []

    for fixture_name, fixture_path, expected_state in FIXTURE_EXPECTATIONS:
        response = load_json(fixture_path)
        validation = boundary.validate_future_kernel_response(response)
        actual_state = validation["kernel_response_state"]
        schema_status = validation["kernel_response_validation"]
        passed = schema_status == "ok" and actual_state == expected_state

        if not passed:
            failures.append(
                f"{fixture_name}: expected state {expected_state}, "
                f"got {actual_state}, schema status {schema_status}"
            )

        results.append(
            {
                "fixture": fixture_name,
                "path": str(fixture_path.relative_to(REPO_ROOT)),
                "expected_state": expected_state,
                "actual_state": actual_state,
                "kernel_response_validation": schema_status,
                "schema_error_count": validation["schema_error_count"],
                "blocking_reason_count": len(validation["blocking_reasons"]),
                "restricting_reason_count": len(validation["restricting_reasons"]),
                "passed": passed,
            }
        )

    return {
        "kernel_response_fixture_checks": "ok" if not failures else "failed",
        "fixture_count": len(results),
        "passed_count": sum(1 for result in results if result["passed"]),
        "failed_count": len(failures),
        "fixtures": results,
        "failures": failures,
        "runtime_invocation_performed": False,
        "kernel_responses_generated_locally": False,
    }


def main() -> None:
    result = validate_fixture_states()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["failures"]:
        raise SystemExit(1)
    print("kernel-response-fixture-checks-ok")


if __name__ == "__main__":
    main()
