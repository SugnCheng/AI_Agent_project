"""Raw acquisition item shape for v0.1 scaffolding.

This module defines the minimum raw item shape expected after controlled
whitelist acquisition. It does not fetch, crawl, parse live pages, or infer
market meaning.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RawItem:
    """Minimum raw source item captured before preprocessing.

    Field names intentionally mirror FETCH_POLICY.md and the ingestion bundle
    traceability requirements.
    """

    source_id: str
    retrieved_at: str
    source_url: str
    title: str
    raw_text: str
    content_type: str
    region: str
    language: str
    published_at: str | None = None
    canonical_url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate_minimum_fields(self) -> list[str]:
        """Return missing minimum fields without mutating the item."""

        required = {
            "source_id": self.source_id,
            "retrieved_at": self.retrieved_at,
            "source_url": self.source_url,
            "title": self.title,
            "raw_text": self.raw_text,
            "content_type": self.content_type,
            "region": self.region,
            "language": self.language,
        }
        return [name for name, value in required.items() if not value]


TODO = [
    "Decide whether RawItem timestamps must be validated with datetime parsing.",
    "Decide how quarantined raw items should be represented before bundle creation.",
]
