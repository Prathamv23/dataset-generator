# 🎓 Synthetic Interview Dataset Generator
### Answer & Label Generation Module

> **Internship Project** — This module is responsible for generating synthetic
> answers and labels for interview questions. The question generation module
> is handled separately and feeds into this pipeline.

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [File Structure](#file-structure)
3. [How the System Works](#how-the-system-works)
4. [How Labels Are Generated](#how-labels-are-generated)
5. [Quick Start](#quick-start)
6. [Input & Output Formats](#input--output-formats)
7. [Future Integration with the Main Project](#future-integration-with-the-main-project)
8. [Architecture Decisions](#architecture-decisions)

---

## Project Overview

This module takes a list of interview questions (JSON) and generates a labeled
synthetic dataset with **three answer variants per question**:

| Label       | Meaning                                                     |
|-------------|-------------------------------------------------------------|
| `correct`   | Accurate, concise, interview-quality answer                 |
| `partial`   | Shows some understanding but lacks depth or has gaps        |
| `incorrect` | Confidently wrong — mimics common misconceptions            |

The dataset can be used to train or evaluate answer-quality classifiers,
interview coaching tools, or automated grading systems.

---

## File Structure

```
synthetic_interview_dataset/
│
├── main.py                  # Orchestrator — run this to execute the pipeline
├── answer_generator.py      # Core engine: generates correct/partial/incorrect answers
├── validator.py             # Schema validation + duplicate detection
├── exporter.py              # Writes output to JSON and/or CSV
│
├── sample_questions.json    # 36 sample questions across 7 domains
├── requirements.txt         # Python dependencies
├── README.md                # This file
│
└── output/                  # Created automatically on first run
    ├── dataset_YYYYMMDD_HHMMSS.json
    └── dataset_YYYYMMDD_HHMMSS.csv
```

---

## How the System Works

```
sample_questions.json
        │
        ▼
   main.py: _load_questions()
        │
        ▼
   answer_generator.py: AnswerGenerator.generate_answers()
     ├── _pick_answer(domain, "correct")
     ├── _pick_answer(domain, "partial")
     └── _pick_answer(domain, "incorrect")
        │
        ▼   (3 records per question)
   validator.py: DatasetValidator.validate()
     ├── Field schema check
     └── Duplicate fingerprint check
        │
        ▼
   exporter.py: DatasetExporter.export()
     ├── output/dataset_*.json
     └── output/dataset_*.csv
```

**To reach 100+ records:** The pipeline automatically cycles the question list
as many times as needed (each pass yields `questions × 3` records).
With 36 sample questions → 1 pass = 108 records ✅

---

## How Labels Are Generated

Labels are **assigned deterministically**, not predicted:

1. `generate_answers()` is called once per question.
2. It calls `_pick_answer(domain, label)` **three times**, once per label.
3. Each call selects a random answer from a pre-written template bank indexed
   by `(domain, label)` — e.g., `ANSWER_BANK["OOP"]["correct"]`.
4. The label is set **before** the text is retrieved — there is no ambiguity.

This approach ensures:
- ✅ 100% balanced label distribution (exactly 1/3 each)
- ✅ No label leakage or guessing
- ✅ Deterministic quality (templates are human-written)
- ✅ Easy to replace with LLM generation later

---

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run with Defaults (36 questions → 108 records)
```bash
python main.py
```

### Run with Custom Options
```bash
# Generate at least 300 records
python main.py --samples 300

# Use a custom questions file
python main.py --questions path/to/my_questions.json

# Export JSON only
python main.py --formats json

# Custom output directory
python main.py --output results/my_run
```

### Expected Output
```
18:42:01 [INFO] Loaded 36 unique questions.
18:42:01 [INFO] Target: 100 samples → 1 pass(es) over 36 questions.
18:42:01 [INFO] Pass 1/1 complete — 108 records so far.
18:42:01 [INFO] Validation complete: 108 → 108 records (0 invalid, 0 duplicates).

==================================================
  DATASET VALIDATION REPORT
==================================================
  Total records input   : 108
  Records removed       : 0 (invalid schema), 0 (duplicates)
  Clean records output  : 108

  Label distribution:
    correct     :   36  (33.3%)  ███████████
    partial     :   36  (33.3%)  ███████████
    incorrect   :   36  (33.3%)  ███████████
==================================================

==================================================
  EXPORT SUMMARY
==================================================
  Total records exported : 108
  [JSON]  /path/to/output/dataset_20240101_184201.json  (42.3 KB)
  [CSV ]  /path/to/output/dataset_20240101_184201.csv   (28.1 KB)
==================================================
```

---

## Input & Output Formats

### Input: `sample_questions.json`
```json
[
  {
    "question": "What is polymorphism in OOP?",
    "domain": "OOP",
    "difficulty": "easy"
  }
]
```

### Output: `dataset_*.json`
```json
{
  "metadata": {
    "generated_at": "2024-01-01T18:42:01",
    "total_records": 108,
    "label_counts": { "correct": 36, "partial": 36, "incorrect": 36 },
    "domains": ["Algorithms", "Databases", "Machine Learning", ...]
  },
  "records": [
    {
      "question":   "What is polymorphism in OOP?",
      "answer":     "Polymorphism allows objects of different classes...",
      "label":      "correct",
      "domain":     "OOP",
      "difficulty": "easy"
    }
  ]
}
```

### Output: `dataset_*.csv`
```
question,answer,label,domain,difficulty
What is polymorphism in OOP?,Polymorphism allows objects...,correct,OOP,easy
```

---

## Future Integration with the Main Project

This module is designed as a **drop-in component**. Integration options:

### Option 1 — Direct Python Import (recommended)
```python
# In the main project's orchestration script:
from synthetic_interview_dataset.main import run_pipeline

# Pass your already-generated questions directly
my_questions = question_module.generate()   # your existing module
labeled_records = run_pipeline(
    questions  = my_questions,
    output_dir = "output/run_001",
    min_samples = 500
)
```

### Option 2 — CLI / Subprocess
```bash
# Write questions to JSON, then call this module
python answer_generator_module/main.py \
    --questions generated_questions.json \
    --samples 500 \
    --output pipeline_output/
```

### Option 3 — API Replacement (future)
When scaling beyond template-based generation, replace the
`_pick_answer()` method in `answer_generator.py` with an LLM API call:

```python
# answer_generator.py — future version
def _pick_answer(self, domain: str, label: str) -> str:
    prompt = f"Generate a {label} answer for domain {domain}..."
    return call_llm_api(prompt)   # OpenAI / Claude / Gemini
```

The rest of the pipeline — validator, exporter, main.py — **does not change**.

---

## Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| Template banks per domain | Predictable quality, zero API cost, easy to extend |
| Deterministic label assignment | No label errors, perfect balance guaranteed |
| Fingerprint-based dedup | O(n) dedup without pandas dependency for core logic |
| Timestamped output files | Prevents overwriting across multiple runs |
| `run_pipeline()` function | Main project can import and call without subprocess |
| Modular files | Each module has one responsibility — easy to test and replace |

---

*Module developed as part of the Synthetic Interview Dataset Generator internship project.*
