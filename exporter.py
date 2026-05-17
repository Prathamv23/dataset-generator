import csv
import json
import os
import logging
from datetime import datetime
from typing import Literal

logger = logging.getLogger(__name__)

# Output directory (relative to project root)
DEFAULT_OUTPUT_DIR = "output"

# Column order for CSV export (makes the file predictable and readable)
CSV_COLUMNS = ["question", "answer", "label", "domain", "difficulty"]


class DatasetExporter:
    """
    Exports a validated list of answer dicts to disk in one or more formats.

    Usage:
        exporter = DatasetExporter(output_dir="output")
        paths = exporter.export(records, formats=["json", "csv"])
        print(paths)  # {"json": "output/dataset_...", "csv": "output/dataset_..."}
    """

    def __init__(self, output_dir: str = DEFAULT_OUTPUT_DIR):
        """
        Args:
            output_dir: Directory where exported files will be saved.
                        Created automatically if it does not exist.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # ──────────────────────────────────────────
    # PUBLIC API
    # ──────────────────────────────────────────

    def export(
        self,
        records: list[dict],
        formats: list[Literal["json", "csv"]] | None = None,
        filename_prefix: str = "dataset"
    ) -> dict[str, str]:
        """
        Exports records to all requested formats and returns a dict of output paths.

        Args:
            records:          Validated list of answer dicts.
            formats:          List of formats to export. Default: ["json", "csv"].
            filename_prefix:  Base name for output files.

        Returns:
            Dict mapping format name → file path. Example:
            {"json": "output/dataset_20240101_120000.json", "csv": "output/...csv"}
        """
        if formats is None:
            formats = ["json", "csv"]

        if not records:
            logger.warning("No records to export. Skipping.")
            return {}

        # Generate a timestamped filename to avoid overwriting previous runs
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{filename_prefix}_{timestamp}"

        output_paths: dict[str, str] = {}

        for fmt in formats:
            if fmt == "json":
                path = self._export_json(records, base_name)
            elif fmt == "csv":
                path = self._export_csv(records, base_name)
            else:
                logger.warning("Unknown format '%s' — skipping.", fmt)
                continue
            output_paths[fmt] = path

        return output_paths

    # ──────────────────────────────────────────
    # FORMAT-SPECIFIC EXPORTERS
    # ──────────────────────────────────────────

    def _export_json(self, records: list[dict], base_name: str) -> str:
        """
        Writes records as a pretty-printed JSON array.

        Structure:
        {
          "metadata": { ... },
          "records": [ { ... }, ... ]
        }
        """
        path = os.path.join(self.output_dir, f"{base_name}.json")

        # Wrap records in a metadata envelope — useful for ML pipeline logging
        payload = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_records": len(records),
                "label_counts": self._count_labels(records),
                "domains": sorted(set(r["domain"] for r in records)),
            },
            "records": records
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        logger.info("JSON exported → %s  (%d records)", path, len(records))
        return path

    def _export_csv(self, records: list[dict], base_name: str) -> str:
        """
        Writes records as a CSV file with a fixed column order.

        The CSV is UTF-8 encoded and uses Unix line endings for compatibility
        with pandas and most ML tooling.
        """
        path = os.path.join(self.output_dir, f"{base_name}.csv")

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=CSV_COLUMNS,
                extrasaction="ignore"   # silently ignore any extra fields
            )
            writer.writeheader()
            writer.writerows(records)

        logger.info("CSV  exported → %s  (%d records)", path, len(records))
        return path

    # ──────────────────────────────────────────
    # HELPERS
    # ──────────────────────────────────────────

    @staticmethod
    def _count_labels(records: list[dict]) -> dict[str, int]:
        """Returns a count of each label for the metadata block."""
        counts: dict[str, int] = {"correct": 0, "partial": 0, "incorrect": 0}
        for r in records:
            label = r.get("label", "")
            if label in counts:
                counts[label] += 1
        return counts

    def print_summary(self, output_paths: dict[str, str], record_count: int) -> None:
        """Prints a user-friendly export summary to stdout."""
        print("\n" + "=" * 50)
        print("  EXPORT SUMMARY")
        print("=" * 50)
        print(f"  Total records exported : {record_count}")
        for fmt, path in output_paths.items():
            abs_path = os.path.abspath(path)
            size_kb  = os.path.getsize(path) / 1024
            print(f"  [{fmt.upper():4}]  {abs_path}  ({size_kb:.1f} KB)")
        print("=" * 50 + "\n")
