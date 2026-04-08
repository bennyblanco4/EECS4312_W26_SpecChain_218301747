"""
Runs the full automated pipeline end-to-end for the MindDoc SpecChain project.

Execution order:
  Step 1: src/01_collect_or_import.py  -- collect raw reviews from Google Play
  Step 2: src/02_clean.py              -- clean raw reviews, produce reviews_clean.jsonl
  Step 3: src/05_personas_auto.py      -- cluster reviews, generate auto groups and personas (requires GROQ_API_KEY)
  Step 4: src/06_spec_generate.py      -- generate automated specification from personas
  Step 5: src/07_tests_generate.py     -- generate automated tests from spec
  Step 6: src/08_metrics.py            -- compute metrics for all three pipelines

Note: Manual and hybrid pipeline artifacts must be created manually by the student.
      This script only automates the steps intended for programmatic generation.

Files produced:
  data/reviews_raw.jsonl
  data/reviews_clean.jsonl
  data/dataset_metadata.json
  data/review_groups_auto.json
  personas/personas_auto.json
  prompts/prompt_auto.json
  spec/spec_auto.md
  tests/tests_auto.json
  metrics/metrics_manual.json
  metrics/metrics_auto.json
  metrics/metrics_hybrid.json
  metrics/metrics_summary.json

Usage:
    python src/run_all.py
"""

import subprocess, sys, os


def run_step(script_path, step_name):
    print(f"\n[Step] {step_name}")
    print(f"  Running: python {script_path}")
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=False,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ERROR: {step_name} failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"  {step_name} completed.")


STEPS = [
    ("src/01_collect_or_import.py", "Step 1: Collect raw reviews from Google Play"),
    ("src/02_clean.py", "Step 2: Clean raw reviews"),
    ("src/05_personas_auto.py", "Step 3: Auto grouping and persona generation (requires GROQ_API_KEY)"),
    ("src/06_spec_generate.py", "Step 4: Generate automated specification"),
    ("src/07_tests_generate.py", "Step 5: Generate automated tests"),
    ("src/08_metrics.py", "Step 6: Compute all pipeline metrics"),
]


if __name__ == "__main__":
    print("=== SpecChain Automated Pipeline ===")
    print("App: MindDoc: Mental Health Support")
    print()

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("WARNING: GROQ_API_KEY is not set.")
        print("  Steps 3 and 4 will use template-based generation instead of the Groq LLM.")
        print("  Set GROQ_API_KEY to enable full LLM-powered generation.")
        print()

    for script_path, step_name in STEPS:
        run_step(script_path, step_name)

    print()
    print("=== Pipeline complete ===")
    print("Run python src/00_validate_repo.py to confirm all files are present.")
