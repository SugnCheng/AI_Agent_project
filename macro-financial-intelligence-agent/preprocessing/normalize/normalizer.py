"""Normalization scaffold for v0.1 raw items.

Normalization prepares raw acquisition output for deduplication, tagging, and
triage. It must not summarize, infer market impact, or perform kernel-level
reasoning.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NormalizedItem:
    """Normalized item shape before dedup and triage."""

    item_id: str
    source_id: str
    region: str
    retrieved_at: str
    published_at: str
    title: str
    source_url: str
    canonical_url: str
    content_type: str
    language: str
    raw_excerpt: str
    metadata: dict[str, Any]


class Normalizer:
    """Interface boundary for future normalization logic."""

    def normalize(self, raw_item: Any) -> NormalizedItem:
        """Normalize one raw item.

        TODO: implement after raw acquisition outputs are stable. The future
        implementation should preserve source meaning and avoid analytical
        rewriting.
        """

        raise NotImplementedError("TODO: implement governed raw-item normalization.")


TODO = [
    "Define item_id generation rules.",
    "Define canonical_url fallback behavior when source_url is the only available URL.",
    "Define maximum raw_excerpt length and truncation policy.",
]
