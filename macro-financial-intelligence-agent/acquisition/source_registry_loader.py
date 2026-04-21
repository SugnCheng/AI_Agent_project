"""Source registry loading scaffold for v0.1.

The source registry is YAML and remains governed by config/source_registry.yaml.
This scaffold intentionally does not implement a production YAML parser or
runtime source expansion.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SourceRegistry:
    """In-memory placeholder for an approved source registry."""

    path: Path
    raw_text: str
    parsed: dict[str, Any] | None = None


class SourceRegistryLoader:
    """Minimal loader boundary for the whitelist source registry."""

    def __init__(self, registry_path: str | Path) -> None:
        self.registry_path = Path(registry_path)

    def load_text(self) -> SourceRegistry:
        """Load registry text only.

        This is enough for scaffold-level file presence checks. Structured YAML
        parsing is intentionally deferred until a YAML dependency decision is
        made.
        """

        raw_text = self.registry_path.read_text(encoding="utf-8")
        return SourceRegistry(path=self.registry_path, raw_text=raw_text)

    def load_structured(self) -> SourceRegistry:
        """Future structured YAML loading entry point."""

        raise NotImplementedError(
            "TODO: choose and govern YAML parsing before structured registry loading."
        )


TODO = [
    "Choose YAML parser dependency or a controlled internal parser for config/source_registry.yaml.",
    "Validate source_id uniqueness and enabled-source eligibility during structured loading.",
    "Validate authority_tier and fetch_method values against governed vocabularies.",
]
