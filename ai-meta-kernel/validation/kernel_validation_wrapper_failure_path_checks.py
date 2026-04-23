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
import shutil
from types import ModuleType
from typing import Any
import uuid


REPO_ROOT = Path(__file__).resolve().parents[2]
KERNEL_ROOT = REPO_ROOT / "ai-meta-kernel"
VALIDATION_ROOT = KERNEL_ROOT / "validation"
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


def write_helper(path: Path, source: str) -> Path:
    path.write_text(source, encoding="utf-8")
    return path


@contextlib.contextmanager
def temporary_validation_dir():
    temp_root = VALIDATION_ROOT / f".kernel-wrapper-failure-path-{uuid.uuid4().hex}"
    temp_root.mkdir()
    try:
        yield temp_root
    finally:
        shutil.rmtree(temp_root)


def check_child_nonzero_stops_and_suppresses_success(wrapper: ModuleType) -> None:
    with temporary_validation_dir() as temp_root:
        failing_helper = write_helper(
            temp_root / "failing_helper.py",
            "import sys\nsys.exit(7)\n",
        )
        marker_path = temp_root / "later_helper_was_run.marker"
        later_helper = write_helper(
            temp_root / "later_helper.py",
            (
                "from pathlib import Path\n"
                f"Path({str(marker_path)!r}).write_text('ran', encoding='utf-8')\n"
            ),
        )

        exit_code, stdout, stderr = run_wrapper_with_checks(
            wrapper,
            [
                ("intentional failing helper", failing_helper),
                ("later helper must not run", later_helper),
            ],
        )

    if exit_code != 7:
        raise AssertionError(f"wrapper should return failing child exit code 7, got {exit_code}")

    if FINAL_SUCCESS_SIGNAL in stdout:
        raise AssertionError("wrapper must suppress final success signal after child failure")

    if marker_path.exists():
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
