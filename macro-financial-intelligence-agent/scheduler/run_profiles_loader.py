"""Run profiles loading scaffold for v0.1.

This helper performs minimal structured YAML loading when PyYAML is installed.
It does not run schedules, evaluate cron expressions, or launch jobs.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RunProfiles:
    """In-memory representation of governed run profile configuration."""

    path: Path
    raw_text: str
    parsed: dict[str, Any]


class RunProfilesLoader:
    """Minimal loader boundary for scheduler/run_profiles.yaml."""

    def __init__(self, profiles_path: str | Path) -> None:
        self.profiles_path = Path(profiles_path)

    def load_structured(self) -> RunProfiles:
        """Load run profiles with PyYAML and perform minimal shape checks."""

        raw_text = self.profiles_path.read_text(encoding="utf-8")
        try:
            import yaml
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "PyYAML is required for structured run profile loading. "
                "Install dependencies from macro-financial-intelligence-agent/requirements.txt."
            ) from exc

        parsed = yaml.safe_load(raw_text)
        if not isinstance(parsed, dict):
            raise ValueError("run_profiles.yaml must parse to a mapping.")

        required_top_level = {
            "version",
            "global_defaults",
            "run_modes",
            "profiles",
        }
        missing = sorted(required_top_level - set(parsed))
        if missing:
            raise ValueError(f"run_profiles.yaml missing top-level keys: {missing}")

        profiles = parsed.get("profiles")
        if not isinstance(profiles, list):
            raise ValueError("run_profiles.yaml 'profiles' must be a list.")

        profile_ids: list[str] = []
        for index, profile in enumerate(profiles):
            if not isinstance(profile, dict):
                raise ValueError(f"profiles[{index}] must be a mapping.")
            profile_id = profile.get("profile_id")
            if not isinstance(profile_id, str) or not profile_id:
                raise ValueError(f"profiles[{index}] missing non-empty profile_id.")
            profile_ids.append(profile_id)

        duplicates = sorted(
            {profile_id for profile_id in profile_ids if profile_ids.count(profile_id) > 1}
        )
        if duplicates:
            raise ValueError(f"duplicate profile_id values: {duplicates}")

        return RunProfiles(path=self.profiles_path, raw_text=raw_text, parsed=parsed)


TODO = [
    "Validate profile source_selection against config/source_registry.yaml.",
    "Validate run_mode and report_target against INGESTION_BUNDLE.schema.json.",
    "Do not implement cron execution in this loader.",
]
