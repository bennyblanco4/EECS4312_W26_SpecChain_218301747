"""
Validates that all required files and folders exist in the SpecChain repository.

Checks for the presence of all files required by the course project rubric.

Usage:
    python src/00_validate_repo.py
"""

import os, sys

REQUIRED_FILES = [
    "data/reviews_raw.jsonl",
    "data/reviews_clean.jsonl",
    "data/dataset_metadata.json",
    "data/review_groups_manual.json",
    "data/review_groups_auto.json",
    "data/review_groups_hybrid.json",
    "personas/personas_manual.json",
    "personas/personas_auto.json",
    "personas/personas_hybrid.json",
    "spec/spec_manual.md",
    "spec/spec_auto.md",
    "spec/spec_hybrid.md",
    "tests/tests_manual.json",
    "tests/tests_auto.json",
    "tests/tests_hybrid.json",
    "metrics/metrics_manual.json",
    "metrics/metrics_auto.json",
    "metrics/metrics_hybrid.json",
    "metrics/metrics_summary.json",
    "prompts/prompt_auto.json",
    "reflection/reflection.md",
    "README.md",
    "src/00_validate_repo.py",
    "src/01_collect_or_import.py",
    "src/02_clean.py",
    "src/03_manual_coding_template.py",
    "src/04_personas_manual.py",
    "src/05_personas_auto.py",
    "src/06_spec_generate.py",
    "src/07_tests_generate.py",
    "src/08_metrics.py",
    "src/run_all.py",
]

def validate():
    print("Checking repository structure...")
    all_ok = True
    for path in REQUIRED_FILES:
        if os.path.isfile(path):
            print(f"  {path} found")
        else:
            print(f"  MISSING: {path}")
            all_ok = False
    print()
    if all_ok:
        print("Repository validation complete — all required files are present.")
    else:
        print("Repository validation FAILED — some required files are missing.")
        sys.exit(1)

if __name__ == "__main__":
    validate()
