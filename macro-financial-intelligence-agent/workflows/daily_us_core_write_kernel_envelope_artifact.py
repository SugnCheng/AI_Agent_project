"""Write a daily_us_core kernel input envelope artifact for file exchange.

This scaffold writes the macro-produced envelope artifact only. It does not
invoke ai-meta-kernel runtime, read kernel responses, write kernel responses,
compose reports, fetch live sources, or execute schedules.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"
ENVELOPE_DIR = PROJECT_ROOT / "runtime" / "kernel_exchange" / "envelopes"
ARTIFACT_KIND = "kernel_input_envelope"
TIMESTAMP_PATTERN = re.compile(r"^\d{8}T\d{6}Z$")


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def utc_timestamp() -> str:
    """Return compact UTC timestamp for artifact naming."""

    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def validate_timestamp(timestamp: str) -> None:
    """Validate the governed compact timestamp format."""

    if not TIMESTAMP_PATTERN.match(timestamp):
        raise ValueError("timestamp must use YYYYMMDDTHHMMSSZ format")


def artifact_filename(envelope: dict[str, Any], timestamp: str) -> str:
    """Build the governed file-based exchange artifact filename."""

    validate_timestamp(timestamp)
    return (
        f"{envelope['profile_id']}__"
        f"{envelope['run_mode']}__"
        f"{envelope['report_target']}__"
        f"{timestamp}__"
        f"{ARTIFACT_KIND}.json"
    )


def load_kernel_input_envelope() -> dict[str, Any]:
    """Reuse the existing fixture kernel input envelope path."""

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


def write_envelope_artifact(timestamp: str | None = None) -> dict[str, Any]:
    """Write the governed envelope artifact and return a compact summary."""

    envelope = load_kernel_input_envelope()
    artifact_timestamp = timestamp or utc_timestamp()
    filename = artifact_filename(envelope, artifact_timestamp)
    ENVELOPE_DIR.mkdir(parents=True, exist_ok=True)
    artifact_path = ENVELOPE_DIR / filename
    artifact_path.write_text(json.dumps(envelope, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return {
        "kernel_exchange_write_envelope_status": "ok",
        "artifact_kind": ARTIFACT_KIND,
        "artifact_path": str(artifact_path.relative_to(REPO_ROOT)),
        "artifact_filename": filename,
        "profile_id": envelope["profile_id"],
        "run_mode": envelope["run_mode"],
        "report_target": envelope["report_target"],
        "regions": envelope["regions"],
        "envelope_type": envelope["envelope_type"],
        "envelope_version": envelope["envelope_version"],
        "kernel_invocation_performed": False,
        "kernel_response_read": False,
        "kernel_response_written": False,
        "canonical_task_object_generated_locally": False,
        "downstream_reporting_unlocked": False,
        "deferred_runtime_behavior": [
            "actual_ai_meta_kernel_runtime_invocation",
            "kernel_response_reading",
            "kernel_response_writing",
            "failure_artifact_writing",
            "downstream_macro_reporting",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write daily_us_core kernel input envelope artifact without invoking kernel."
    )
    parser.add_argument(
        "--timestamp",
        help="Optional compact UTC timestamp for deterministic local checks: YYYYMMDDTHHMMSSZ.",
    )
    args = parser.parse_args()

    result = write_envelope_artifact(timestamp=args.timestamp)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
