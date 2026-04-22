"""Fixture bundle to kernel input envelope scaffold for daily_us_core v0.1.

This helper converts the current fixture ingestion bundle into a deterministic
kernel input envelope. It does not invoke ai-meta-kernel runtime and does not
generate a canonical TASK_OBJECT_SCHEMA.json object.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"
KERNEL_META_LAYER_ROOT = REPO_ROOT / "ai-meta-kernel" / "meta-layer"

ENVELOPE_TYPE = "macro_fixture_bundle_kernel_input"
ENVELOPE_VERSION = "0.1.0"
SOURCE_PROJECT = "macro-financial-intelligence-agent"
OPERATOR_INTENT = (
    "Ask the Meta-Layer to frame this validated macro-financial evidence bundle "
    "for downstream research reporting. Do not treat this as a request for direct "
    "trading advice."
)

KERNEL_REQUIRED_OUTPUT_FIELDS = (
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
)

KERNEL_OWNED_CONCLUSION_FIELDS = (
    "raw_request",
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
)


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_fixture_bundle_output() -> dict[str, Any]:
    """Reuse the existing fixture bundle assembler and request its artifact."""

    bundle_module = load_module(
        "daily_us_core_fixture_bundle_assembler",
        PROJECT_ROOT / "workflows" / "daily_us_core_fixture_bundle_assembler.py",
    )
    return bundle_module.run_fixture_bundle_assembler(include_bundle=True)


def build_evidence_context(bundle_output: dict[str, Any]) -> dict[str, Any]:
    """Build evidence-only context from the fixture bundle output."""

    bundle = bundle_output["fixture_bundle_artifact"]
    items = bundle["items"]
    return {
        "bundle_status": {
            "fixture_bundle_status": bundle_output["fixture_bundle_status"],
            "schema_validation": bundle_output["schema_validation"],
            "invariant_validation": bundle_output["invariant_validation"],
        },
        "counts": {
            "item_count_raw": bundle_output["item_count_raw"],
            "item_count_after_dedup": bundle_output["item_count_after_dedup"],
            "bundle_item_count": bundle_output["bundle_item_count"],
            "source_count": bundle_output["source_count"],
        },
        "priority_counts": bundle_output["priority_counts"],
        "source_ids": sorted({item["source_id"] for item in items}),
        "evidence_only_note": (
            "Bundle fields are evidence/context only. The macro agent does not "
            "convert preliminary_priority, risk_tags, source metadata, or "
            "summary_seed into kernel conclusions."
        ),
    }


def build_kernel_task_object_expectation() -> dict[str, Any]:
    """Describe kernel-owned outputs without filling them as conclusions."""

    return {
        "kernel_owned": True,
        "handoff_contract_path": "../ai-meta-kernel/meta-layer/HANDOFF_CONTRACT.md",
        "task_object_schema_path": "../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json",
        "required_output_fields": list(KERNEL_REQUIRED_OUTPUT_FIELDS),
        "macro_agent_must_not_prefill_as_conclusions": list(KERNEL_OWNED_CONCLUSION_FIELDS),
        "notes": (
            "This envelope is input material for the Meta-Layer. The kernel must "
            "perform framing, classification, risk calibration, habit triggering, "
            "structural decomposition, verification planning, challenge loop, "
            "status flagging, downstream recommendation, and handoff emission."
        ),
    }


def build_kernel_input_envelope(bundle_output: dict[str, Any]) -> dict[str, Any]:
    """Build the deterministic macro-side kernel input envelope."""

    bundle = bundle_output["fixture_bundle_artifact"]
    return {
        "envelope_type": ENVELOPE_TYPE,
        "envelope_version": ENVELOPE_VERSION,
        "source_project": SOURCE_PROJECT,
        "profile_id": bundle_output["profile_id"],
        "run_mode": bundle_output["run_mode"],
        "report_target": bundle_output["report_target"],
        "regions": bundle_output["regions"],
        "operator_intent": OPERATOR_INTENT,
        "evidence_bundle": bundle,
        "evidence_context": build_evidence_context(bundle_output),
        "kernel_task_object_expectation": build_kernel_task_object_expectation(),
        "deferred_runtime_behavior": sorted(
            set(bundle_output["deferred_runtime_behavior"])
            | {
                "kernel_runtime_execution",
                "canonical_task_object_generation",
                "report_composition",
            }
        ),
    }


def validate_envelope_not_kernel_task_object(envelope: dict[str, Any]) -> None:
    """Validate the envelope does not pretend to be a canonical kernel task object."""

    errors: list[str] = []
    top_level_keys = set(envelope)
    forbidden_present = sorted(top_level_keys.intersection(KERNEL_OWNED_CONCLUSION_FIELDS))
    if forbidden_present:
        errors.append(
            "envelope must not pre-fill kernel-owned top-level fields: "
            + ", ".join(forbidden_present)
        )

    if set(KERNEL_REQUIRED_OUTPUT_FIELDS).issubset(top_level_keys):
        errors.append("envelope must not contain all canonical task object required fields")

    expectation = envelope.get("kernel_task_object_expectation", {})
    if expectation.get("kernel_owned") is not True:
        errors.append("kernel_task_object_expectation.kernel_owned must be true")
    if set(expectation.get("required_output_fields", [])) != set(KERNEL_REQUIRED_OUTPUT_FIELDS):
        errors.append("kernel_task_object_expectation required fields are incomplete")

    if errors:
        raise ValueError("kernel input envelope validation failed:\n- " + "\n- ".join(errors))


def validate_kernel_input_envelope(envelope: dict[str, Any]) -> None:
    """Validate local envelope invariants without calling the kernel."""

    errors: list[str] = []
    required_fields = (
        "envelope_type",
        "envelope_version",
        "source_project",
        "profile_id",
        "run_mode",
        "report_target",
        "regions",
        "operator_intent",
        "evidence_bundle",
        "evidence_context",
        "kernel_task_object_expectation",
        "deferred_runtime_behavior",
    )
    for field in required_fields:
        if field not in envelope:
            errors.append(f"missing envelope field '{field}'")

    if envelope.get("envelope_type") != ENVELOPE_TYPE:
        errors.append("unexpected envelope_type")
    if envelope.get("envelope_version") != ENVELOPE_VERSION:
        errors.append("unexpected envelope_version")
    if envelope.get("source_project") != SOURCE_PROJECT:
        errors.append("unexpected source_project")
    if not envelope.get("operator_intent"):
        errors.append("operator_intent must be non-empty")
    if not envelope.get("evidence_bundle"):
        errors.append("evidence_bundle must be present")

    deferred = set(envelope.get("deferred_runtime_behavior", []))
    if "kernel_runtime_execution" not in deferred:
        errors.append("deferred_runtime_behavior must include kernel_runtime_execution")
    if "ai_meta_kernel_runtime_handoff" not in deferred:
        errors.append("deferred_runtime_behavior must include ai_meta_kernel_runtime_handoff")

    if errors:
        raise ValueError("kernel input envelope validation failed:\n- " + "\n- ".join(errors))
    validate_envelope_not_kernel_task_object(envelope)


def run_fixture_kernel_input_envelope(include_envelope: bool) -> dict[str, Any]:
    """Build and validate the fixture bundle to kernel input envelope."""

    bundle_output = load_fixture_bundle_output()
    envelope = build_kernel_input_envelope(bundle_output)
    validate_kernel_input_envelope(envelope)

    result: dict[str, Any] = {
        "kernel_input_envelope_status": "ok",
        "envelope_type": envelope["envelope_type"],
        "envelope_version": envelope["envelope_version"],
        "source_project": envelope["source_project"],
        "profile_id": envelope["profile_id"],
        "run_mode": envelope["run_mode"],
        "report_target": envelope["report_target"],
        "regions": envelope["regions"],
        "evidence_bundle_id": envelope["evidence_bundle"]["bundle_metadata"]["bundle_id"],
        "evidence_item_count": len(envelope["evidence_bundle"]["items"]),
        "kernel_owned_field_count": len(KERNEL_REQUIRED_OUTPUT_FIELDS),
        "envelope_validation": "ok",
        "canonical_task_object_generated": False,
        "deferred_runtime_behavior": envelope["deferred_runtime_behavior"],
    }
    if include_envelope:
        result["kernel_input_envelope"] = envelope
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a fixture bundle to kernel input envelope without kernel runtime."
    )
    parser.add_argument(
        "--show-envelope",
        action="store_true",
        help="Print the full in-memory kernel input envelope.",
    )
    args = parser.parse_args()

    result = run_fixture_kernel_input_envelope(include_envelope=args.show_envelope)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
