"""Ingestion bundle builder scaffold for v0.1.

This scaffold defines the boundary for creating objects compatible with
bundles/schemas/INGESTION_BUNDLE.schema.json. It does not fetch, schedule,
triage, or compose reports.
"""

from dataclasses import dataclass
from typing import Any


RUN_MODES = (
    "daily_brief_run",
    "weekly_intelligence_run",
    "custom_range_run",
    "event_watch_run",
)

REPORT_TARGETS = (
    "daily_brief",
    "weekly_intelligence_report",
    "special_event_memo",
)


@dataclass(frozen=True)
class BundleBuildRequest:
    """Inputs needed to build a schema-compatible ingestion bundle."""

    bundle_id: str
    run_mode: str
    generated_at: str
    date_range: dict[str, str]
    regions: list[str]
    report_target: str
    watchlist_topics: list[str]
    operator_notes: str
    items: list[dict[str, Any]]
    item_count_raw: int


class IngestionBundleBuilder:
    """Interface boundary for future bundle assembly."""

    def build(self, request: BundleBuildRequest) -> dict[str, Any]:
        """Build a schema-compatible ingestion bundle.

        TODO: implement after source registry loading, normalization, dedup,
        tagging, and triage scaffolds are promoted to governed behavior.
        """

        raise NotImplementedError("TODO: implement governed ingestion bundle assembly.")

    def validate_request_enums(self, request: BundleBuildRequest) -> list[str]:
        """Return enum-alignment errors without building a bundle."""

        errors: list[str] = []
        if request.run_mode not in RUN_MODES:
            errors.append(f"invalid run_mode: {request.run_mode}")
        if request.report_target not in REPORT_TARGETS:
            errors.append(f"invalid report_target: {request.report_target}")
        return errors


TODO = [
    "Validate item fields against INGESTION_BUNDLE.schema.json before bundle emission.",
    "Enforce item_count_after_dedup <= item_count_raw.",
    "Define no-new-items bundle behavior as a first-class build case.",
]
