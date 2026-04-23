"""Failure-path checks for the kernel local validation wrapper.

This helper tests wrapper-level process-control behavior without modifying real
validation helpers. It does not invoke kernel runtime, generate task objects,
read or write runtime artifacts, fetch sources, compose reports, run scheduler
behavior, install dependencies, or repair files.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path
from types import SimpleNamespace
from types import ModuleType
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
KERNEL_ROOT = REPO_ROOT / "ai-meta-kernel"
WRAPPER_PATH = KERNEL_ROOT / "validation" / "run_all_kernel_local_checks.py"
FINAL_SUCCESS_SIGNAL = "kernel-local-validation-checks-ok"


def load_wrapper_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "run_all_kernel_local_checks_under_test",
        WRAPPER_PATH,
    )
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load wrapper module: {WRAPPER_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_wrapper_with_checks(
    wrapper: ModuleType,
    checks: list[tuple[str, Path]],
) -> tuple[int, str, str]:
    original_checks: Any = wrapper.CHECKS
    stdout = io.StringIO()
    stderr = io.StringIO()

    try:
        wrapper.CHECKS = checks
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = wrapper.main()
    finally:
        wrapper.CHECKS = original_checks

    return exit_code, stdout.getvalue(), stderr.getvalue()


def check_child_nonzero_stops_and_suppresses_success(wrapper: ModuleType) -> None:
    original_subprocess_run = wrapper.subprocess.run
    calls: list[list[str]] = []

    def fake_run(command: list[str], cwd: Path, check: bool) -> SimpleNamespace:
        calls.append(command)
        return SimpleNamespace(returncode=7)

    try:
        wrapper.subprocess.run = fake_run
        exit_code, stdout, stderr = run_wrapper_with_checks(
            wrapper,
            [
                ("intentional failing helper", WRAPPER_PATH),
                ("later helper must not run", WRAPPER_PATH),
            ],
        )
    finally:
        wrapper.subprocess.run = original_subprocess_run

    if exit_code != 7:
        raise AssertionError(f"wrapper should return failing child exit code 7, got {exit_code}")

    if FINAL_SUCCESS_SIGNAL in stdout:
        raise AssertionError("wrapper must suppress final success signal after child failure")

    if len(calls) != 1:
        raise AssertionError("wrapper must stop before running later helper after failure")

    expected_failure = (
        "kernel-local-validation-checks-failed: intentional failing helper "
        "exited with 7"
    )
    if expected_failure not in stderr:
        raise AssertionError("wrapper stderr missing child failure message")


def check_missing_helper_path_fails_closed(wrapper: ModuleType) -> None:
    missing_helper = KERNEL_ROOT / "missing_kernel_validation_helper_for_failure_path.py"
    if missing_helper.exists():
        raise AssertionError(f"missing-helper test path unexpectedly exists: {missing_helper}")

    exit_code, stdout, stderr = run_wrapper_with_checks(
        wrapper,
        [("missing helper", missing_helper)],
    )

    if exit_code != 1:
        raise AssertionError(f"missing helper should return 1, got {exit_code}")

    if FINAL_SUCCESS_SIGNAL in stdout:
        raise AssertionError("wrapper must suppress final success signal after missing helper")

    expected_failure = "kernel-local-validation-checks-failed: missing helper:"
    if expected_failure not in stderr:
        raise AssertionError("wrapper stderr missing missing-helper failure message")


def main() -> None:
    wrapper = load_wrapper_module()
    check_child_nonzero_stops_and_suppresses_success(wrapper)
    check_missing_helper_path_fails_closed(wrapper)
    print("kernel-validation-wrapper-failure-path-checks-ok")


if __name__ == "__main__":
    main()
