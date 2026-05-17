"""Validate cleanup automation boundary contract examples.

This helper is standalone local validation only. It validates in-memory cleanup
decision objects and checks that this helper remains outside the governed
wrapper. It does not create, read, delete, promote, or mutate runtime artifacts.
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATION_ROOT = REPO_ROOT / "ai-meta-kernel" / "validation"
WRAPPER_PATH = VALIDATION_ROOT / "run_all_kernel_local_checks.py"

SUCCESS_SIGNAL = "kernel-cleanup-boundary-contract-checks-ok"

REQUIRED_FIELDS = {
    "cleanup_type",
    "cleanup_state",
    "cleanup_stage",
    "source_artifact_path",
    "artifact_category",
    "policy_reference",
    "cleanup_eligibility",
    "cleanup_decision",
    "deletion_allowed",
    "filesystem_mutation_allowed",
    "fixture_promotion_allowed",
    "manual_review_required",
    "macro_report_unlock",
    "actual_handoff_executed",
    "cli_behavior_added",
}

VALID_ARTIFACT_CATEGORIES = {
    "committed_static_fixture",
    "promoted_regression_fixture_candidate",
    "generated_local_runtime_artifact",
    "dry_run_artifact_candidate",
    "temporary_validation_artifact",
}

VALID_CLEANUP_ELIGIBILITIES = {
    "not_eligible",
    "eligible_for_review_only",
    "eligible_for_future_cleanup_policy",
    "blocked",
    "deferred",
}

VALID_CLEANUP_DECISIONS = {
    "cleanup_not_implemented",
    "cleanup_blocked",
    "cleanup_deferred",
    "review_required",
    "no_action",
}

DELETION_ELIGIBLE_VALUES = {
    "eligible_for_future_cleanup_policy",
}

LOCKED_FALSE_FIELDS = {
    "deletion_allowed",
    "filesystem_mutation_allowed",
    "fixture_promotion_allowed",
    "macro_report_unlock",
    "actual_handoff_executed",
    "cli_behavior_added",
}

CLEANUP_EXECUTION_STATES = {
    "cleanup_executed",
    "cleanup_automation_executed",
    "artifact_deleted",
    "filesystem_mutated",
}


def has_policy_reference(cleanup: dict[str, object]) -> bool:
    reference = cleanup.get("policy_reference")
    return isinstance(reference, str) and bool(reference.strip())


def validate_cleanup_decision(cleanup: object) -> list[str]:
    errors: list[str] = []

    if not isinstance(cleanup, dict):
        return ["cleanup decision must be an object"]

    missing = sorted(REQUIRED_FIELDS.difference(cleanup))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    category = cleanup.get("artifact_category")
    eligibility = cleanup.get("cleanup_eligibility")
    decision = cleanup.get("cleanup_decision")

    if category not in VALID_ARTIFACT_CATEGORIES:
        errors.append("unknown artifact_category")

    if eligibility not in VALID_CLEANUP_ELIGIBILITIES:
        errors.append("unknown cleanup_eligibility")

    if decision not in VALID_CLEANUP_DECISIONS:
        errors.append("unknown cleanup_decision")

    for field in sorted(LOCKED_FALSE_FIELDS):
        if cleanup.get(field) is True:
            errors.append(f"{field} must remain false")

    if cleanup.get("cleanup_state") in CLEANUP_EXECUTION_STATES:
        errors.append("cleanup execution marker rejected")

    if eligibility in DELETION_ELIGIBLE_VALUES and cleanup.get("deletion_allowed") is True:
        errors.append("cleanup eligibility must not imply deletion")

    if (
        eligibility in DELETION_ELIGIBLE_VALUES
        and cleanup.get("filesystem_mutation_allowed") is True
    ):
        errors.append("cleanup eligibility must not imply filesystem mutation")

    if (
        eligibility in DELETION_ELIGIBLE_VALUES
        and cleanup.get("fixture_promotion_allowed") is True
    ):
        errors.append("cleanup eligibility must not imply fixture promotion")

    if decision in {
        "cleanup_not_implemented",
        "cleanup_blocked",
        "cleanup_deferred",
    } and cleanup.get("deletion_allowed") is True:
        errors.append(f"{decision} must not allow deletion")

    if decision == "review_required" and cleanup.get("manual_review_required") is not True:
        errors.append("review_required must not be treated as automatic approval")

    if decision == "no_action" and cleanup.get("filesystem_mutation_allowed") is True:
        errors.append("no_action must not mutate filesystem")

    if category == "committed_static_fixture":
        if eligibility in DELETION_ELIGIBLE_VALUES:
            errors.append("committed static fixtures must never be deletion eligible")
        if cleanup.get("deletion_allowed") is True:
            errors.append("committed static fixtures must not allow deletion")

    if (
        category == "promoted_regression_fixture_candidate"
        and cleanup.get("deletion_allowed") is True
    ):
        errors.append("promoted regression fixture candidates must not be deleted")

    if category == "promoted_regression_fixture_candidate":
        if decision != "review_required" or cleanup.get("manual_review_required") is not True:
            errors.append("promoted regression fixture candidates require review")

    if category == "generated_local_runtime_artifact" and not has_policy_reference(cleanup):
        errors.append("generated local runtime artifacts require policy_reference")

    if (
        category == "dry_run_artifact_candidate"
        and cleanup.get("deletion_allowed") is True
    ):
        errors.append("dry-run artifact candidates are not deleted by default")

    if (
        category == "temporary_validation_artifact"
        and cleanup.get("deletion_allowed") is True
    ):
        errors.append(
            "temporary validation artifacts require governed policy before deletion"
        )

    return errors


def expect_valid(name: str, cleanup: object) -> None:
    errors = validate_cleanup_decision(cleanup)
    if errors:
        raise AssertionError(f"{name} should be valid: {errors}")


def expect_invalid(name: str, cleanup: object) -> None:
    errors = validate_cleanup_decision(cleanup)
    if not errors:
        raise AssertionError(f"{name} should be invalid")


def base_cleanup(**overrides: object) -> dict[str, object]:
    cleanup: dict[str, object] = {
        "cleanup_type": "cleanup_automation_boundary_decision",
        "cleanup_state": "validation_only",
        "cleanup_stage": "minimal_validation_helper_slice",
        "source_artifact_path": "explicit/local/runtime_artifact.example.json",
        "artifact_category": "generated_local_runtime_artifact",
        "policy_reference": "runtime_artifact_policy_object",
        "cleanup_eligibility": "deferred",
        "cleanup_decision": "cleanup_not_implemented",
        "deletion_allowed": False,
        "filesystem_mutation_allowed": False,
        "fixture_promotion_allowed": False,
        "manual_review_required": False,
        "macro_report_unlock": False,
        "actual_handoff_executed": False,
        "cli_behavior_added": False,
    }
    cleanup.update(overrides)
    return cleanup


def verify_wrapper_unchanged() -> None:
    wrapper_text = WRAPPER_PATH.read_text(encoding="utf-8")
    helper_name = Path(__file__).name
    if helper_name in wrapper_text:
        raise AssertionError("wrapper inclusion rejected: helper is in CHECKS")
    if SUCCESS_SIGNAL in wrapper_text:
        raise AssertionError("wrapper inclusion rejected: success signal is in wrapper")


def run_positive_cases() -> None:
    expect_valid("generated local runtime artifact default", base_cleanup())
    expect_valid(
        "committed static fixture not eligible",
        base_cleanup(
            artifact_category="committed_static_fixture",
            policy_reference="reviewed_static_fixture_policy",
            cleanup_eligibility="not_eligible",
            cleanup_decision="no_action",
        ),
    )
    expect_valid(
        "promoted candidate review only",
        base_cleanup(
            artifact_category="promoted_regression_fixture_candidate",
            cleanup_eligibility="eligible_for_review_only",
            cleanup_decision="review_required",
            manual_review_required=True,
        ),
    )
    expect_valid(
        "dry-run candidate default no action",
        base_cleanup(
            artifact_category="dry_run_artifact_candidate",
            cleanup_eligibility="not_eligible",
            cleanup_decision="no_action",
        ),
    )
    expect_valid(
        "temporary validation artifact deferred",
        base_cleanup(
            artifact_category="temporary_validation_artifact",
            cleanup_eligibility="eligible_for_future_cleanup_policy",
            cleanup_decision="cleanup_deferred",
        ),
    )


def run_fail_closed_cases() -> None:
    expect_invalid("non-object cleanup decision", ["not", "an", "object"])
    missing_field_cleanup = base_cleanup()
    del missing_field_cleanup["cleanup_type"]
    expect_invalid("missing required field", missing_field_cleanup)
    expect_invalid(
        "unknown cleanup eligibility",
        base_cleanup(cleanup_eligibility="unknown"),
    )
    expect_invalid(
        "unknown cleanup decision",
        base_cleanup(cleanup_decision="unknown"),
    )
    expect_invalid(
        "unknown artifact category",
        base_cleanup(artifact_category="unknown"),
    )
    expect_invalid(
        "cleanup eligibility deletion marker",
        base_cleanup(
            cleanup_eligibility="eligible_for_future_cleanup_policy",
            deletion_allowed=True,
        ),
    )
    expect_invalid(
        "cleanup eligibility filesystem mutation marker",
        base_cleanup(
            cleanup_eligibility="eligible_for_future_cleanup_policy",
            filesystem_mutation_allowed=True,
        ),
    )
    expect_invalid(
        "cleanup eligibility fixture promotion marker",
        base_cleanup(
            cleanup_eligibility="eligible_for_future_cleanup_policy",
            fixture_promotion_allowed=True,
        ),
    )
    expect_invalid(
        "cleanup_not_implemented deletion",
        base_cleanup(deletion_allowed=True),
    )
    expect_invalid(
        "cleanup_blocked deletion",
        base_cleanup(cleanup_decision="cleanup_blocked", deletion_allowed=True),
    )
    expect_invalid(
        "cleanup_deferred deletion",
        base_cleanup(cleanup_decision="cleanup_deferred", deletion_allowed=True),
    )
    expect_invalid(
        "review required automatic approval",
        base_cleanup(cleanup_decision="review_required", manual_review_required=False),
    )
    expect_invalid(
        "no action filesystem mutation",
        base_cleanup(cleanup_decision="no_action", filesystem_mutation_allowed=True),
    )
    expect_invalid(
        "committed fixture deletion eligible",
        base_cleanup(
            artifact_category="committed_static_fixture",
            cleanup_eligibility="eligible_for_future_cleanup_policy",
        ),
    )
    expect_invalid(
        "committed fixture deletion allowed",
        base_cleanup(
            artifact_category="committed_static_fixture",
            cleanup_eligibility="not_eligible",
            deletion_allowed=True,
        ),
    )
    expect_invalid(
        "promoted candidate deletion allowed",
        base_cleanup(
            artifact_category="promoted_regression_fixture_candidate",
            cleanup_decision="review_required",
            manual_review_required=True,
            deletion_allowed=True,
        ),
    )
    expect_invalid(
        "promoted candidate missing review",
        base_cleanup(artifact_category="promoted_regression_fixture_candidate"),
    )
    expect_invalid(
        "generated runtime artifact missing policy reference",
        base_cleanup(policy_reference=""),
    )
    expect_invalid(
        "dry-run candidate deletion allowed",
        base_cleanup(artifact_category="dry_run_artifact_candidate", deletion_allowed=True),
    )
    expect_invalid(
        "temporary validation deletion allowed",
        base_cleanup(
            artifact_category="temporary_validation_artifact",
            deletion_allowed=True,
        ),
    )
    expect_invalid(
        "cleanup execution marker",
        base_cleanup(cleanup_state="cleanup_executed"),
    )
    expect_invalid("macro report unlock", base_cleanup(macro_report_unlock=True))
    expect_invalid("actual handoff", base_cleanup(actual_handoff_executed=True))
    expect_invalid("cli behavior", base_cleanup(cli_behavior_added=True))


def main() -> int:
    run_positive_cases()
    run_fail_closed_cases()
    verify_wrapper_unchanged()
    print(SUCCESS_SIGNAL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
