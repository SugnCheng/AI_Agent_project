"""Static checks for core Meta-Layer contract artifacts.

This helper validates only local contract files. It does not invoke kernel
runtime, generate task objects, run file-exchange fixture checks, write
artifacts, fetch sources, compose reports, or run scheduler behavior.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
KERNEL_ROOT = REPO_ROOT / "ai-meta-kernel"

MASTER_SPEC = KERNEL_ROOT / "META_LAYER_MASTER_SPEC.md"
RUNTIME_PIPELINE = KERNEL_ROOT / "meta-layer" / "RUNTIME_PIPELINE.md"
HANDOFF_CONTRACT = KERNEL_ROOT / "meta-layer" / "HANDOFF_CONTRACT.md"
TASK_OBJECT_SCHEMA = KERNEL_ROOT / "meta-layer" / "TASK_OBJECT_SCHEMA.json"

REQUIRED_FILES = [
    MASTER_SPEC,
    RUNTIME_PIPELINE,
    HANDOFF_CONTRACT,
    TASK_OBJECT_SCHEMA,
]

CANONICAL_TOP_LEVEL_FIELDS = {
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

CANONICAL_MASTER_SPEC_SECTIONS = [
    "## 1. Identity",
    "## 2. Core Mission",
    "## 7. Runtime Pipeline",
    "## 17. Task Object Contract",
    "## 18. Downstream Handoff Contract",
    "## 24. Canonical Alignment Rule",
]

CANONICAL_HANDOFF_FIELDS = [
    "raw_request",
    "framed_objective",
    "task_classification",
    "risk_profile",
    "triggered_habits",
    "structural_decomposition",
    "required_checks",
    "status_flags",
    "downstream_recommendation",
]

HANDOFF_MODES = [
    "standard_handoff",
    "restricted_handoff",
    "do_not_handoff",
]


def read_text(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"required file is missing: {path}")
    return path.read_text(encoding="utf-8")


def load_json_object(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise AssertionError(f"required JSON file is missing: {path}")
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise AssertionError(f"JSON file must contain an object: {path}")
    return data


def require_text_contains(text: str, needles: list[str], label: str) -> None:
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise AssertionError(f"{label} missing required text: {missing}")


def check_required_files_exist() -> None:
    missing = [str(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        raise AssertionError(f"required contract files are missing: {missing}")


def check_task_object_schema() -> None:
    schema = load_json_object(TASK_OBJECT_SCHEMA)

    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise AssertionError("TASK_OBJECT_SCHEMA.json must declare draft 2020-12 metadata")

    required = schema.get("required")
    if not isinstance(required, list):
        raise AssertionError("TASK_OBJECT_SCHEMA.json required must be a list")

    missing_required = sorted(CANONICAL_TOP_LEVEL_FIELDS.difference(required))
    if missing_required:
        raise AssertionError(
            "TASK_OBJECT_SCHEMA.json missing canonical top-level required fields: "
            f"{missing_required}"
        )

    properties = schema.get("properties")
    if not isinstance(properties, dict):
        raise AssertionError("TASK_OBJECT_SCHEMA.json properties must be an object")

    missing_properties = sorted(CANONICAL_TOP_LEVEL_FIELDS.difference(properties))
    if missing_properties:
        raise AssertionError(
            "TASK_OBJECT_SCHEMA.json missing canonical top-level properties: "
            f"{missing_properties}"
        )

    structural_decomposition = properties.get("structural_decomposition", {})
    structural_properties = structural_decomposition.get("properties", {})
    if "tradeoffs" not in structural_properties:
        raise AssertionError("structural_decomposition must preserve tradeoffs field")

    risk_profile = properties.get("risk_profile", {})
    risk_properties = risk_profile.get("properties", {})
    for field in ("overall_level", "categories"):
        if field not in risk_properties:
            raise AssertionError(f"risk_profile must preserve {field} field")

    downstream = properties.get("downstream_recommendation", {})
    downstream_properties = downstream.get("properties", {})
    for field in ("agent_type", "output_format", "mode"):
        if field not in downstream_properties:
            raise AssertionError(f"downstream_recommendation must preserve {field} field")

    mode_enum = downstream_properties.get("mode", {}).get("enum")
    if not isinstance(mode_enum, list):
        raise AssertionError("downstream_recommendation.mode enum must be present")

    missing_modes = sorted(set(HANDOFF_MODES).difference(mode_enum))
    if missing_modes:
        raise AssertionError(
            "TASK_OBJECT_SCHEMA.json missing canonical handoff modes: "
            f"{missing_modes}"
        )

    triggered_habits = properties.get("triggered_habits", {})
    contains = triggered_habits.get("contains", {})
    role_const = contains.get("properties", {}).get("role", {}).get("const")
    if role_const != "primary":
        raise AssertionError("triggered_habits must require at least one primary habit")


def check_master_spec_sections() -> None:
    text = read_text(MASTER_SPEC)
    require_text_contains(text, CANONICAL_MASTER_SPEC_SECTIONS, "META_LAYER_MASTER_SPEC.md")


def check_runtime_pipeline_stages() -> None:
    text = read_text(RUNTIME_PIPELINE)
    stages = [f"P{number}" for number in range(0, 11)]
    require_text_contains(text, stages, "RUNTIME_PIPELINE.md")


def check_handoff_contract_terms() -> None:
    text = read_text(HANDOFF_CONTRACT)
    require_text_contains(text, CANONICAL_HANDOFF_FIELDS, "HANDOFF_CONTRACT.md")
    require_text_contains(text, HANDOFF_MODES, "HANDOFF_CONTRACT.md")


def main() -> None:
    check_required_files_exist()
    check_task_object_schema()
    check_master_spec_sections()
    check_runtime_pipeline_stages()
    check_handoff_contract_terms()
    print("kernel-static-meta-layer-contract-checks-ok")


if __name__ == "__main__":
    main()
