# 🎓 Synthetic Interview Dataset Generator

<div align="center">

### Answer & Label Generation Module

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)
![Dataset](https://img.shields.io/badge/Dataset-100%2B%20Samples-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> Internship Project — Synthetic Answer & Label Generation Pipeline  
> Built for AI Evaluation, Testing & Validation Support

</div>

---

# 📌 Project Overview

This project is a modular **Synthetic Interview Dataset Generator** designed to create labeled interview answer datasets for testing and AI evaluation systems.

The system accepts interview questions generated from an external module and produces:

- ✅ Correct Answers
- ✅ Partial Answers
- ✅ Incorrect Answers
- ✅ Automatic Labels
- ✅ JSON Export
- ✅ CSV Export
- ✅ Validation Reports

The generated dataset can be used for:

- AI Interview Evaluation
- Answer Quality Classification
- Automated Grading Systems
- Testing Pipelines
- ML Training Data

---

# ✨ Features

- 🎯 Generates 3 answer types per question
- 🏷️ Automatic label assignment
- 📊 Balanced dataset distribution
- 🔍 Duplicate detection
- 📁 JSON & CSV export support
- ⚡ Modular architecture
- 🔄 Easy future API integration
- 🧪 Validation & reporting support
- 📦 Production-style folder structure

---

# 🏗️ Project Architecture

```text
sample_questions.json
        │
        ▼
   main.py
        │
        ▼
answer_generator.py
   ├── correct answers
   ├── partial answers
   └── incorrect answers
        │
        ▼
validator.py
   ├── duplicate detection
   ├── schema validation
   └── label validation
        │
        ▼
exporter.py
   ├── JSON export
   └── CSV export
```

---

# 📂 File Structure

```text
synthetic_interview_dataset/
│
├── main.py
├── answer_generator.py
├── validator.py
├── exporter.py
│
├── sample_questions.json
├── requirements.txt
├── README.md
│
└── output/
    ├── dataset_YYYYMMDD_HHMMSS.json
    └── dataset_YYYYMMDD_HHMMSS.csv
```

---

# ⚙️ How the System Works

## Step 1 — Load Questions

Questions are loaded from:

```text
sample_questions.json
```

Example:

```json
{
  "question": "What is polymorphism in OOP?",
  "domain": "OOP",
  "difficulty": "easy"
}
```

---

## Step 2 — Generate Synthetic Answers

For every question, the system generates:

| Label | Description |
|---|---|
| `correct` | Accurate interview-style answer |
| `partial` | Incomplete or vague answer |
| `incorrect` | Wrong but realistic answer |

---

## Step 3 — Assign Labels

Labels are assigned deterministically:

```python
label = "correct"
label = "partial"
label = "incorrect"
```

This guarantees:

- Balanced datasets
- Zero label ambiguity
- Consistent evaluation data

---

## Step 4 — Validation

The validator checks:

- Duplicate records
- Missing fields
- Invalid labels
- Output structure
- Dataset balance

---

## Step 5 — Export Dataset

Final dataset is exported into:

- 📄 JSON
- 📊 CSV

---

# 🚀 Quick Start

## 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 2️⃣ Run the Project

```bash
python main.py
```

---

## 3️⃣ Generate Custom Dataset Size

```bash
python main.py --samples 300
```

---

## 4️⃣ Export JSON Only

```bash
python main.py --formats json
```

---

# 📥 Input Format

## `sample_questions.json`

```json
[
  {
    "question": "What is inheritance?",
    "domain": "OOP",
    "difficulty": "easy"
  }
]
```

---

# 📤 Output Format

## JSON Output

```json
{
  "question": "What is inheritance?",
  "answer": "Inheritance allows one class to acquire properties from another class.",
  "label": "correct",
  "domain": "OOP",
  "difficulty": "easy"
}
```

---

## CSV Output

```csv
question,answer,label,domain,difficulty
What is inheritance?,Inheritance allows...,correct,OOP,easy
```

---

# 📊 Example Validation Report

```text
==================================================
  DATASET VALIDATION REPORT
==================================================

Total Records Input   : 108
Records Removed       : 0
Clean Records Output  : 108

Label Distribution:

correct     : 36 (33.3%)
partial     : 36 (33.3%)
incorrect   : 36 (33.3%)

==================================================
```

---

# 🧠 Label Generation Logic

Labels are generated using a deterministic template-based system.

Example:

```python
generate_correct_answer()
generate_partial_answer()
generate_incorrect_answer()
```

This ensures:

- Predictable quality
- Balanced distributions
- No random label mismatch
- Easy scalability

---

# 🔮 Future Integration

This module is designed as a reusable component.

## Integration Flow

```text
Question Generator Module
            │
            ▼
Synthetic Answer Generator
            │
            ▼
Labeled Dataset Output
            │
            ▼
AI Evaluation System
```

---

## Future API Integration

The template engine can later be replaced with:

- OpenAI API
- Claude API
- Gemini API

without changing the rest of the pipeline.

Example:

```python
def _pick_answer():
    return call_llm_api(prompt)
```

---

# 🏛️ Architecture Decisions

| Decision | Reason |
|---|---|
| Modular structure | Easy maintenance |
| Deterministic labels | Prevents label mismatch |
| Template-based answers | Fast & API-free |
| Timestamped exports | Prevents overwriting |
| Separate validator | Cleaner testing pipeline |
| JSON + CSV export | Flexible integration |

---

# 🧪 Technologies Used

- Python
- pandas
- json
- csv
- random
- argparse
- datetime

---

# 📈 Dataset Statistics

| Metric | Value |
|---|---|
| Minimum Samples | 100+ |
| Labels | 3 |
| Export Formats | JSON, CSV |
| Validation Support | Yes |
| Duplicate Detection | Yes |

---

# 📌 Use Cases

- AI Interview Platforms
- Automated Evaluation Systems
- ML Training Pipelines
- Synthetic Data Generation
- Testing & Validation

---

# 👨‍💻 Internship Task Scope

This project was developed as part of an internship module focused on:

- Synthetic data generation
- Dataset validation
- AI evaluation support
- Testing infrastructure

The question generation module already existed separately.

---

# 📚 References

- Python Documentation
- pandas Documentation
- JSON Documentation
- CSV Module Documentation
- GitHub

---

# 📜 License

This project is created for educational and internship purposes.

---

<div align="center">

### ⭐ If you found this project useful, consider starring the repository!

</div>
