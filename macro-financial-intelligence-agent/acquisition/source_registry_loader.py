"""Source registry loading scaffold for v0.1.

The source registry is YAML and remains governed by config/source_registry.yaml.
This scaffold performs minimal structured YAML loading when PyYAML is installed.
It does not fetch sources, expand sources, or implement production acquisition.
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
        """Load the source registry with PyYAML and perform minimal shape checks."""

        raw_text = self.registry_path.read_text(encoding="utf-8")
        try:
            import yaml
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "PyYAML is required for structured source registry loading. "
                "Install dependencies from macro-financial-intelligence-agent/requirements.txt."
            ) from exc

        parsed = yaml.safe_load(raw_text)
        if not isinstance(parsed, dict):
            raise ValueError("source_registry.yaml must parse to a mapping.")

        required_top_level = {
            "version",
            "defaults",
            "regions",
            "authority_tiers",
            "source_types",
            "fetch_methods",
            "sources",
        }
        missing = sorted(required_top_level - set(parsed))
        if missing:
            raise ValueError(f"source_registry.yaml missing top-level keys: {missing}")

        sources = parsed.get("sources")
        if not isinstance(sources, list):
            raise ValueError("source_registry.yaml 'sources' must be a list.")

        source_ids: list[str] = []
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                raise ValueError(f"sources[{index}] must be a mapping.")
            source_id = source.get("source_id")
            if not isinstance(source_id, str) or not source_id:
                raise ValueError(f"sources[{index}] missing non-empty source_id.")
            source_ids.append(source_id)

        duplicates = sorted({source_id for source_id in source_ids if source_ids.count(source_id) > 1})
        if duplicates:
            raise ValueError(f"duplicate source_id values: {duplicates}")

        return SourceRegistry(path=self.registry_path, raw_text=raw_text, parsed=parsed)


TODO = [
    "Validate enabled-source eligibility against run profile source_selection.",
    "Validate authority_tier and fetch_method values against governed vocabularies.",
    "Define quarantine behavior for structurally invalid source entries.",
]
