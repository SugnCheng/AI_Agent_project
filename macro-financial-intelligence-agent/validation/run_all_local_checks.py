"""Run all local validation layers for macro-financial-intelligence-agent v0.1.

This is a developer-facing wrapper around the existing local validation
scripts. It does not replace them, add CI, fetch sources, execute schedules,
compose reports, or call ai-meta-kernel.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"
VALIDATION_ROOT = PROJECT_ROOT / "validation"

CHECKS = [
    ("scaffold contract checks", VALIDATION_ROOT / "scaffold_contract_checks.py"),
    (
        "dependency-backed contract checks",
        VALIDATION_ROOT / "dependency_backed_contract_checks.py",
    ),
    ("semantic contract checks", VALIDATION_ROOT / "semantic_contract_checks.py"),
]


def run_check(label: str, script_path: Path) -> None:
    """Run one validation script and stop on failure."""

    print(f"running {label}...", flush=True)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=REPO_ROOT,
        env=env,
        check=False,
    )
    if result.returncode != 0:
        print(f"{label} failed with exit code {result.returncode}", flush=True)
        raise SystemExit(result.returncode)


def main() -> None:
    for label, script_path in CHECKS:
        run_check(label, script_path)

    print("all-local-validation-checks-ok", flush=True)


if __name__ == "__main__":
    main()
