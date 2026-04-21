"""Preliminary triage scaffold for v0.1.

Triage assigns P1/P2/P3/DROP candidates using governed rules. It must not make
final analytical judgments or bypass ai-meta-kernel.
"""

from dataclasses import dataclass


TRIAGE_PRIORITIES = ("P1", "P2", "P3", "DROP")


@dataclass(frozen=True)
class TriageDecision:
    """Preliminary triage output shape."""

    preliminary_priority: str
    reason_codes: list[str]
    notes: str = ""

    def validate_priority(self) -> bool:
        return self.preliminary_priority in TRIAGE_PRIORITIES


class PreliminaryTriage:
    """Interface boundary for future TRIAGE_RULES.md implementation."""

    def evaluate(self, tagged_item: object) -> TriageDecision:
        """Evaluate one tagged item against governed triage rules."""

        raise NotImplementedError("TODO: implement governed preliminary triage.")


TODO = [
    "Translate TRIAGE_RULES.md scoring into deterministic, reviewable rules.",
    "Keep operator override behavior outside hidden runtime logic.",
    "Log false positives and false negatives for validation/RETRO_LOG.md.",
]
