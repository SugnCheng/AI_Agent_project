"""Ingestion bundle schema validation helper for v0.1.

This helper validates bundle objects or files against
bundles/schemas/INGESTION_BUNDLE.schema.json when jsonschema is installed.
It does not build bundles, fetch data, run schedules, or compose reports.
"""

from pathlib import Path
from typing import Any
import json


class IngestionBundleSchemaValidator:
    """Minimal jsonschema-backed validator for governed ingestion bundles."""

    def __init__(self, schema_path: str | Path) -> None:
        self.schema_path = Path(schema_path)
        self.schema = json.loads(self.schema_path.read_text(encoding="utf-8"))

        try:
            from jsonschema import Draft202012Validator
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "jsonschema is required for ingestion bundle schema validation. "
                "Install dependencies from macro-financial-intelligence-agent/requirements.txt."
            ) from exc

        Draft202012Validator.check_schema(self.schema)
        self._validator = Draft202012Validator(self.schema)

    def validate_bundle(self, bundle: dict[str, Any]) -> list[str]:
        """Return schema validation errors without mutating the bundle."""

        errors = sorted(self._validator.iter_errors(bundle), key=lambda error: list(error.path))
        return [self._format_error(error) for error in errors]

    def validate_bundle_file(self, bundle_path: str | Path) -> list[str]:
        """Load and validate a bundle JSON file."""

        path = Path(bundle_path)
        bundle = json.loads(path.read_text(encoding="utf-8"))
        return self.validate_bundle(bundle)

    @staticmethod
    def _format_error(error: Any) -> str:
        path = ".".join(str(part) for part in error.path)
        location = path if path else "<root>"
        return f"{location}: {error.message}"


TODO = [
    "Add semantic validation beyond JSON Schema, such as date_range ordering.",
    "Validate source_id values against config/source_registry.yaml.",
    "Validate report_target alignment against reporting/templates.",
]
