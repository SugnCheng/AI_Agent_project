"""Run the governed local kernel validation helpers in order.

This wrapper is local validation orchestration only. It does not invoke kernel
runtime, generate task objects, read or write runtime artifacts, fetch sources,
compose reports, run scheduler behavior, install dependencies, or repair files.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
KERNEL_ROOT = REPO_ROOT / "ai-meta-kernel"
VALIDATION_ROOT = KERNEL_ROOT / "validation"

CHECKS = [
    (
        "static Meta-Layer contract checks",
        VALIDATION_ROOT / "static_meta_layer_contract_checks.py",
    ),
    (
        "kernel file-exchange fixture checks",
        VALIDATION_ROOT / "kernel_file_exchange_fixture_checks.py",
    ),
    (
        "kernel file-exchange adapter scaffold checks",
        VALIDATION_ROOT / "kernel_file_exchange_adapter_scaffold_checks.py",
    ),
]

FINAL_SUCCESS_SIGNAL = "kernel-local-validation-checks-ok"


def run_check(label: str, path: Path) -> int:
    if not path.is_file():
        print(
            f"kernel-local-validation-checks-failed: missing helper: {path}",
            file=sys.stderr,
        )
        return 1

    print(f"[kernel-local-validation] running: {label}", flush=True)
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=REPO_ROOT,
        check=False,
    )
    if result.returncode != 0:
        print(
            f"kernel-local-validation-checks-failed: {label} exited with "
            f"{result.returncode}",
            file=sys.stderr,
        )
    return result.returncode


def main() -> int:
    for label, path in CHECKS:
        exit_code = run_check(label, path)
        if exit_code != 0:
            return exit_code

    print(FINAL_SUCCESS_SIGNAL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
