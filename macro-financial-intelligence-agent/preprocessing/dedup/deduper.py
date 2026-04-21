"""Deduplication scaffold for v0.1 preprocessing.

Deduplication groups near-identical or repeated source material before bundle
creation. It must preserve the strongest available source and must not create
new analysis.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DedupResult:
    """Result shape for future deduplication."""

    retained_items: list[Any]
    dropped_items: list[Any]
    dedup_groups: dict[str, list[str]]


class Deduper:
    """Interface boundary for future dedup logic."""

    def deduplicate(self, normalized_items: list[Any]) -> DedupResult:
        """Deduplicate normalized items.

        TODO: implement deterministic grouping after item identity and source
        priority rules are settled.
        """

        raise NotImplementedError("TODO: implement governed deduplication.")


TODO = [
    "Define exact dedup_group_id generation rules.",
    "Define official-source precedence when media repeats an official source.",
    "Define how duplicate drops are logged for review.",
]
