import hashlib
import logging
from collections import Counter

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

REQUIRED_FIELDS = ["question", "answer", "label", "domain", "difficulty"]
VALID_LABELS    = {"correct", "partial", "incorrect"}

# Set up a simple logger so validation messages are visible but don't clutter output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


class DatasetValidator:
    """
    Validates a list of answer dicts and returns a clean, deduplicated dataset.

    Usage:
        validator = DatasetValidator()
        clean_data = validator.validate(raw_data)
        validator.print_report()
    """

    def __init__(self):
        self._reset_stats()

    # ──────────────────────────────────────────
    # PUBLIC API
    # ──────────────────────────────────────────

    def validate(self, records: list[dict]) -> list[dict]:
        """
        Runs all validation passes on the list of records.

        Args:
            records: Raw list of generated answer dicts.

        Returns:
            Clean list with invalid and duplicate entries removed.
        """
        self._reset_stats()

        # Pass 1: field/schema validation
        field_valid = [r for r in records if self._validate_fields(r)]
        self.stats["removed_invalid_fields"] = len(records) - len(field_valid)

        # Pass 2: duplicate removal
        deduped = self._remove_duplicates(field_valid)
        self.stats["removed_duplicates"] = len(field_valid) - len(deduped)

        # Pass 3: record final stats
        self.stats["total_input"]  = len(records)
        self.stats["total_output"] = len(deduped)
        self.stats["label_dist"]   = dict(Counter(r["label"] for r in deduped))

        logger.info(
            "Validation complete: %d → %d records "
            "(%d invalid, %d duplicates removed).",
            self.stats["total_input"],
            self.stats["total_output"],
            self.stats["removed_invalid_fields"],
            self.stats["removed_duplicates"],
        )
        return deduped

    def print_report(self) -> None:
        """Prints a human-readable summary of the validation run."""
        print("\n" + "=" * 50)
        print("  DATASET VALIDATION REPORT")
        print("=" * 50)
        print(f"  Total records input   : {self.stats['total_input']}")
        print(f"  Records removed       : "
              f"{self.stats['removed_invalid_fields']} (invalid schema), "
              f"{self.stats['removed_duplicates']} (duplicates)")
        print(f"  Clean records output  : {self.stats['total_output']}")
        print()
        print("  Label distribution:")
        for label in ["correct", "partial", "incorrect"]:
            count = self.stats["label_dist"].get(label, 0)
            total = self.stats["total_output"] or 1
            pct   = count / total * 100
            bar   = "█" * int(pct / 3)
            print(f"    {label:<12}: {count:>4}  ({pct:5.1f}%)  {bar}")
        print("=" * 50 + "\n")

    # ──────────────────────────────────────────
    # PRIVATE HELPERS
    # ──────────────────────────────────────────

    def _validate_fields(self, record: dict) -> bool:
        """
        Returns True if the record has all required fields and a valid label.
        Logs a warning for each rejection.
        """
        # Check all required fields exist and are non-empty strings
        for field in REQUIRED_FIELDS:
            if field not in record:
                logger.warning("Missing field '%s' in record: %s", field, record)
                return False
            if not isinstance(record[field], str) or not record[field].strip():
                logger.warning(
                    "Empty or non-string value for '%s' in record: %s", field, record
                )
                return False

        # Check label is valid
        if record["label"] not in VALID_LABELS:
            logger.warning(
                "Invalid label '%s'. Expected one of %s.",
                record["label"], VALID_LABELS
            )
            return False

        return True

    def _remove_duplicates(self, records: list[dict]) -> list[dict]:
        """
        Removes records with identical (question, answer) fingerprints.
        First occurrence is kept; subsequent duplicates are dropped.
        """
        seen:   set[str]   = set()
        unique: list[dict] = []

        for record in records:
            key = self._make_fingerprint(record["question"], record["answer"])
            if key in seen:
                logger.debug(
                    "Duplicate removed — Q: '%s...'", record["question"][:40]
                )
            else:
                seen.add(key)
                unique.append(record)

        return unique

    @staticmethod
    def _make_fingerprint(question: str, answer: str) -> str:
        """
        Creates a compact hash from (question, answer) for dedup checking.
        Normalizes whitespace and case before hashing.
        """
        normalized = (question.strip().lower() + "|||" + answer.strip().lower())
        return hashlib.md5(normalized.encode()).hexdigest()

    def _reset_stats(self) -> None:
        """Resets internal stats dict for a fresh validation run."""
        self.stats: dict = {
            "total_input":             0,
            "total_output":            0,
            "removed_invalid_fields":  0,
            "removed_duplicates":      0,
            "label_dist":              {}
        }
