"""Validate runtime artifact retention policy contract examples.

This helper is standalone local validation only. It validates in-memory policy
objects and checks that this helper remains outside the governed wrapper. It
does not create, delete, promote, or mutate runtime artifacts.
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATION_ROOT = REPO_ROOT / "ai-meta-kernel" / "validation"
WRAPPER_PATH = VALIDATION_ROOT / "run_all_kernel_local_checks.py"

SUCCESS_SIGNAL = "kernel-runtime-artifact-policy-contract-checks-ok"

REQUIRED_FIELDS = {
    "policy_type",
    "policy_state",
    "policy_stage",
    "artifact_category",
    "retention_decision",
    "promotion_decision",
    "cleanup_decision",
    "commit_allowed",
    "cleanup_automation_allowed",
    "fixture_promotion_allowed",
    "macro_report_unlock",
    "actual_handoff_executed",
    "cli_behavior_added",
}

VALID_ARTIFACT_CATEGORIES = {
    "committed_static_fixture",
    "generated_local_runtime_artifact",
    "dry_run_artifact_candidate",
    "temporary_validation_artifact",
    "promoted_regression_fixture_candidate",
}

VALID_RETENTION_DECISIONS = {
    "retain_local",
    "ignore_for_commit",
    "review_for_promotion",
    "cleanup_deferred",
    "blocked",
}

VALID_PROMOTION_DECISIONS = {
    "not_promoted",
    "review_required",
    "promotion_candidate_only",
    "rejected",
}

VALID_CLEANUP_DECISIONS = {
    "cleanup_not_implemented",
    "cleanup_blocked",
    "cleanup_deferred",
    "explicit_manual_review_required",
}

LOCKED_FALSE_FIELDS = {
    "cleanup_automation_allowed",
    "macro_report_unlock",
    "actual_handoff_executed",
    "cli_behavior_added",
}

REVIEW_ORIENTED_PROMOTION_DECISIONS = {
    "review_required",
    "promotion_candidate_only",
}


def valid_reviewed_promotion_state(policy: dict[str, object]) -> bool:
    return (
        policy.get("artifact_category") == "promoted_regression_fixture_candidate"
        and policy.get("retention_decision") == "review_for_promotion"
        and policy.get("promotion_decision") in REVIEW_ORIENTED_PROMOTION_DECISIONS
        and policy.get("cleanup_decision") == "explicit_manual_review_required"
        and policy.get("policy_state") == "review_required"
    )


def validate_policy(policy: object) -> list[str]:
    errors: list[str] = []

    if not isinstance(policy, dict):
        return ["policy must be an object"]

    missing = sorted(REQUIRED_FIELDS.difference(policy))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    if policy.get("artifact_category") not in VALID_ARTIFACT_CATEGORIES:
        errors.append("unknown artifact_category")

    if policy.get("retention_decision") not in VALID_RETENTION_DECISIONS:
        errors.append("unknown retention_decision")

    if policy.get("promotion_decision") not in VALID_PROMOTION_DECISIONS:
        errors.append("unknown promotion_decision")

    if policy.get("cleanup_decision") not in VALID_CLEANUP_DECISIONS:
        errors.append("unknown cleanup_decision")

    for field in sorted(LOCKED_FALSE_FIELDS):
        if policy.get(field) is True:
            errors.append(f"{field} must remain false")

    category = policy.get("artifact_category")
    commit_allowed = policy.get("commit_allowed")
    fixture_promotion_allowed = policy.get("fixture_promotion_allowed")
    reviewed_promotion_state = valid_reviewed_promotion_state(policy)

    if category in {
        "dry_run_artifact_candidate",
        "temporary_validation_artifact",
    } and commit_allowed is True:
        errors.append(f"{category} must not be commit_allowed")

    if (
        category == "generated_local_runtime_artifact"
        and commit_allowed is True
        and not reviewed_promotion_state
    ):
        errors.append(
            "generated runtime artifacts must not be commit_allowed unless "
            "governed reviewed promotion semantics are represented"
        )

    if category == "promoted_regression_fixture_candidate":
        if not reviewed_promotion_state:
            errors.append(
                "promoted regression fixture candidates require review-oriented "
                "promotion semantics"
            )
        if commit_allowed is True:
            errors.append(
                "promoted regression fixture candidates remain candidate-only "
                "and must not be commit_allowed"
            )

    if category == "committed_static_fixture":
        if policy.get("policy_state") != "reviewed_committed_static_fixture":
            errors.append(
                "committed static fixtures must represent already reviewed "
                "committed fixture semantics"
            )
        if policy.get("promotion_decision") != "not_promoted":
            errors.append("committed static fixtures must not imply promotion")
        if policy.get("cleanup_decision") != "cleanup_not_implemented":
            errors.append("committed static fixtures must not imply cleanup")

    if fixture_promotion_allowed is True and not reviewed_promotion_state:
        errors.append(
            "fixture_promotion_allowed requires governed reviewed promotion state"
        )

    if reviewed_promotion_state and fixture_promotion_allowed is True:
        errors.append(
            "reviewed promotion state is candidate-only in this helper and must "
            "not enable fixture promotion"
        )

    return errors


def expect_valid(name: str, policy: object) -> None:
    errors = validate_policy(policy)
    if errors:
        raise AssertionError(f"{name} should be valid: {errors}")


def expect_invalid(name: str, policy: object) -> None:
    errors = validate_policy(policy)
    if not errors:
        raise AssertionError(f"{name} should be invalid")


def base_policy(**overrides: object) -> dict[str, object]:
    policy: dict[str, object] = {
        "policy_type": "runtime_artifact_retention_cleanup_policy",
        "policy_state": "local_policy_validation",
        "policy_stage": "minimal_validation_helper_slice",
        "artifact_category": "generated_local_runtime_artifact",
        "retention_decision": "retain_local",
        "promotion_decision": "not_promoted",
        "cleanup_decision": "cleanup_not_implemented",
        "commit_allowed": False,
        "cleanup_automation_allowed": False,
        "fixture_promotion_allowed": False,
        "macro_report_unlock": False,
        "actual_handoff_executed": False,
        "cli_behavior_added": False,
    }
    policy.update(overrides)
    return policy


def verify_wrapper_unchanged() -> None:
    wrapper_text = WRAPPER_PATH.read_text(encoding="utf-8")
    helper_name = Path(__file__).name
    if helper_name in wrapper_text:
        raise AssertionError("wrapper inclusion rejected: helper is in CHECKS")


def run_positive_cases() -> None:
    expect_valid("generated artifact default", base_policy())
    expect_valid(
        "dry-run candidate",
        base_policy(
            artifact_category="dry_run_artifact_candidate",
            retention_decision="ignore_for_commit",
        ),
    )
    expect_valid(
        "temporary validation artifact",
        base_policy(
            artifact_category="temporary_validation_artifact",
            retention_decision="cleanup_deferred",
            cleanup_decision="cleanup_deferred",
        ),
    )
    expect_valid(
        "promoted candidate review semantics",
        base_policy(
            policy_state="review_required",
            artifact_category="promoted_regression_fixture_candidate",
            retention_decision="review_for_promotion",
            promotion_decision="promotion_candidate_only",
            cleanup_decision="explicit_manual_review_required",
        ),
    )
    expect_valid(
        "committed static fixture",
        base_policy(
            policy_state="reviewed_committed_static_fixture",
            artifact_category="committed_static_fixture",
            retention_decision="retain_local",
            promotion_decision="not_promoted",
            cleanup_decision="cleanup_not_implemented",
            commit_allowed=True,
        ),
    )


def run_fail_closed_cases() -> None:
    expect_invalid("non-object policy", ["not", "an", "object"])
    missing_field_policy = base_policy()
    del missing_field_policy["policy_type"]
    expect_invalid("missing required field", missing_field_policy)
    expect_invalid("unknown category", base_policy(artifact_category="unknown"))
    expect_invalid("unknown retention", base_policy(retention_decision="unknown"))
    expect_invalid("unknown promotion", base_policy(promotion_decision="unknown"))
    expect_invalid("unknown cleanup", base_policy(cleanup_decision="unknown"))
    expect_invalid(
        "generated artifact commit",
        base_policy(commit_allowed=True),
    )
    expect_invalid(
        "dry-run candidate commit",
        base_policy(
            artifact_category="dry_run_artifact_candidate",
            retention_decision="ignore_for_commit",
            commit_allowed=True,
        ),
    )
    expect_invalid(
        "temporary validation commit",
        base_policy(
            artifact_category="temporary_validation_artifact",
            retention_decision="cleanup_deferred",
            commit_allowed=True,
        ),
    )
    expect_invalid(
        "cleanup automation",
        base_policy(cleanup_automation_allowed=True),
    )
    expect_invalid(
        "fixture promotion automation",
        base_policy(fixture_promotion_allowed=True),
    )
    expect_invalid(
        "macro report unlock",
        base_policy(macro_report_unlock=True),
    )
    expect_invalid(
        "actual handoff",
        base_policy(actual_handoff_executed=True),
    )
    expect_invalid(
        "cli behavior",
        base_policy(cli_behavior_added=True),
    )


def main() -> int:
    run_positive_cases()
    run_fail_closed_cases()
    verify_wrapper_unchanged()
    print(SUCCESS_SIGNAL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
