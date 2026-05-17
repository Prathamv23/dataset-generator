import argparse
import json
import logging
import sys
from pathlib import Path

from answer_generator import AnswerGenerator
from validator        import DatasetValidator
from exporter         import DatasetExporter

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# CONSTANTS / DEFAULTS
# ─────────────────────────────────────────────
DEFAULT_QUESTIONS_FILE = "sample_questions.json"
DEFAULT_OUTPUT_DIR     = "output"
DEFAULT_MIN_SAMPLES    = 100   # pipeline will loop questions until this is met


# ─────────────────────────────────────────────
# PIPELINE FUNCTION (importable by main project)
# ─────────────────────────────────────────────

def run_pipeline(
    questions_file: str  = DEFAULT_QUESTIONS_FILE,
    questions:      list | None = None,       # allow direct injection
    output_dir:     str  = DEFAULT_OUTPUT_DIR,
    min_samples:    int  = DEFAULT_MIN_SAMPLES,
    export_formats: list | None = None,
) -> list[dict]:
    """
    Full pipeline: generate → validate → export.

    Args:
        questions_file: Path to a JSON file containing question objects.
                        Ignored if `questions` is passed directly.
        questions:      Pre-loaded list of question dicts. If provided,
                        `questions_file` is skipped. This is the entry point
                        for the main project's question module.
        output_dir:     Directory to write exported files.
        min_samples:    Minimum number of answer records to generate.
                        If the question list is small, it is cycled until met.
        export_formats: Formats to export. Default: ["json", "csv"].

    Returns:
        List of validated answer dicts (same records written to disk).
    """
    if export_formats is None:
        export_formats = ["json", "csv"]

    # ── STEP 1: Load questions ────────────────────────────────────────────────
    if questions is None:
        questions = _load_questions(questions_file)

    if not questions:
        logger.error("No questions found. Exiting.")
        sys.exit(1)

    logger.info("Loaded %d unique questions.", len(questions))

    # ── STEP 2: Generate answers ──────────────────────────────────────────────
    raw_records = _generate_records(questions, min_samples)
    logger.info("Generated %d raw answer records.", len(raw_records))

    # ── STEP 3: Validate ──────────────────────────────────────────────────────
    validator    = DatasetValidator()
    clean_records = validator.validate(raw_records)
    validator.print_report()

    # ── STEP 4: Export ────────────────────────────────────────────────────────
    exporter     = DatasetExporter(output_dir=output_dir)
    output_paths = exporter.export(clean_records, formats=export_formats)
    exporter.print_summary(output_paths, len(clean_records))

    return clean_records


# ─────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────

def _load_questions(filepath: str) -> list[dict]:
    """
    Reads and parses the questions JSON file.
    Returns an empty list and logs an error if the file is missing.
    """
    path = Path(filepath)
    if not path.exists():
        logger.error("Questions file not found: %s", filepath)
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        logger.error("Expected a JSON array in %s, got %s.", filepath, type(data))
        return []

    logger.info("Questions loaded from '%s'.", filepath)
    return data


def _generate_records(questions: list[dict], min_samples: int) -> list[dict]:
    """
    Calls AnswerGenerator for each question, cycling the question list until
    `min_samples` total records are produced.

    Each question produces 3 records (one per label), so the minimum number of
    full cycles = ceil(min_samples / (3 * len(questions))).
    """
    generator = AnswerGenerator()   # no fixed seed → random each run
    records: list[dict] = []

    # Determine how many passes over the question list are needed
    records_per_pass = len(questions) * 3      # 3 labels per question
    passes_needed    = max(1, -(-min_samples // records_per_pass))  # ceiling div

    logger.info(
        "Target: %d samples → %d pass(es) over %d questions.",
        min_samples, passes_needed, len(questions)
    )

    for pass_num in range(passes_needed):
        for q in questions:
            try:
                new_records = generator.generate_answers(q)
                records.extend(new_records)
            except Exception as exc:           # never crash the whole pipeline
                logger.warning(
                    "Skipping question due to error: %s | %s", q.get("question"), exc
                )

        logger.info(
            "Pass %d/%d complete — %d records so far.",
            pass_num + 1, passes_needed, len(records)
        )

    return records


# ─────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synthetic Interview Dataset Generator — Answer & Label Module",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --questions my_questions.json
  python main.py --samples 300 --output results/
  python main.py --formats json          # export JSON only
        """
    )
    parser.add_argument(
        "--questions", default=DEFAULT_QUESTIONS_FILE,
        help=f"Path to input questions JSON file (default: {DEFAULT_QUESTIONS_FILE})"
    )
    parser.add_argument(
        "--output", default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for exported files (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--samples", type=int, default=DEFAULT_MIN_SAMPLES,
        help=f"Minimum number of answer records to generate (default: {DEFAULT_MIN_SAMPLES})"
    )
    parser.add_argument(
        "--formats", nargs="+", default=["json", "csv"],
        choices=["json", "csv"],
        help="Export formats (default: json csv)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    print("\n" + "═" * 55)
    print("  Synthetic Interview Dataset Generator")
    print("  ─  Answer & Label Generation Module")
    print("═" * 55)

    run_pipeline(
        questions_file = args.questions,
        output_dir     = args.output,
        min_samples    = args.samples,
        export_formats = args.formats,
    )

    print(" Pipeline finished successfully.")
