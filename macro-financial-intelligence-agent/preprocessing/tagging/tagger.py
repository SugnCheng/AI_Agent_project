"""Tagging scaffold for v0.1 preprocessing.

Tagging supplies simple metadata for triage and bundle packaging. It is not a
substitute for ai-meta-kernel reasoning.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TagSet:
    """Tags required by INGESTION_BUNDLE.schema.json item fields."""

    topic_tags: list[str]
    market_tags: list[str]
    risk_tags: list[str]


class Tagger:
    """Interface boundary for future rule-based tagging."""

    def tag(self, normalized_item: object) -> TagSet:
        """Assign governed tags to one normalized item."""

        raise NotImplementedError("TODO: implement governed rule-based tagging.")


TODO = [
    "Define controlled vocabularies for topic_tags, market_tags, and risk_tags.",
    "Decide whether watchlist topic matching happens here or in triage.",
    "Ensure tags remain descriptive metadata, not final analysis.",
]
