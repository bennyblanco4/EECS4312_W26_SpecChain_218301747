"""
Computes evaluation metrics for the manual, automated, and hybrid pipelines.

Metrics computed for each pipeline:
  - dataset_size: total cleaned reviews in data/reviews_clean.jsonl
  - persona_count: number of personas in the pipeline persona file
  - requirements_count: number of requirements in the spec file
  - tests_count: number of test scenarios in the tests file
  - traceability_links: total explicit links between artifacts
  - review_coverage_ratio: fraction of reviews covered by review groups (0-1)
  - traceability_ratio: fraction of requirements traceable to a persona
  - testability_rate: fraction of requirements with at least one test
  - ambiguity_ratio: fraction of requirements with vague/non-measurable language

Writes:
  - metrics/metrics_manual.json
  - metrics/metrics_auto.json
  - metrics/metrics_hybrid.json
  - metrics/metrics_summary.json

Usage:
    python src/08_metrics.py
"""

import json, os, re

AMBIGUOUS_TERMS = [
    "easy", "simple", "fast", "quick", "better", "user-friendly", "efficient",
    "good", "nice", "appropriate", "clear", "accessible", "plain-language",
    "friendly", "seamless", "smooth", "intuitive", "helpful", "useful",
    "timely", "meaningful", "extended", "indefinitely", "soon", "reasonable",
    "standard", "normal", "modern", "adequate",
]

def count_reviews(path="data/reviews_clean.jsonl"):
    count = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip(): count += 1
    return count

def count_personas(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return len(data.get("personas", []))

def count_requirements_from_spec(spec_path):
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()
    return len(re.findall(r"^## Requirement ID:", content, re.MULTILINE))

def count_tests(tests_path):
    with open(tests_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return len(data.get("tests", []))

def compute_review_coverage(groups_path):
    total_reviews = count_reviews()
    with open(groups_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    covered = set()
    total_counted = 0
    uses_count_field = False
    for g in data.get("groups", []):
        if "review_ids" in g:
            covered.update(g["review_ids"])
        elif "review_ids_count" in g:
            uses_count_field = True
            total_counted += g["review_ids_count"]
    if uses_count_field:
        return round(min(total_counted / total_reviews, 1.0), 4)
    return round(len(covered) / total_reviews, 4)

def compute_traceability_ratio(spec_path, personas_path):
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r"^## Requirement ID:", content, flags=re.MULTILINE)
    reqs = [b for b in blocks[1:] if b.strip()]
    if not reqs: return 0.0
    traced = sum(1 for b in reqs if "Source Persona:" in b)
    return round(traced / len(reqs), 4)

def compute_testability_rate(spec_path, tests_path):
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()
    req_ids = re.findall(r"^## Requirement ID:\s*(\S+)", content, re.MULTILINE)
    if not req_ids: return 0.0
    with open(tests_path, "r", encoding="utf-8") as f:
        tests_data = json.load(f)
    tested_reqs = {t.get("requirement_id") for t in tests_data.get("tests", [])}
    covered = sum(1 for rid in req_ids if rid in tested_reqs)
    return round(covered / len(req_ids), 4)

def compute_ambiguity_ratio(spec_path):
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r"^## Requirement ID:", content, flags=re.MULTILINE)
    reqs = [b for b in blocks[1:] if b.strip()]
    if not reqs: return 0.0
    ambiguous_count = 0
    for block in reqs:
        block_lower = block.lower()
        if any(term in block_lower for term in AMBIGUOUS_TERMS):
            ambiguous_count += 1
    return round(ambiguous_count / len(reqs), 4)

def compute_traceability_links(groups_path, personas_path, spec_path, tests_path):
    with open(personas_path, "r", encoding="utf-8") as f:
        personas = json.load(f).get("personas", [])
    persona_to_group = sum(1 for p in personas if p.get("derived_from_group"))
    with open(spec_path, "r", encoding="utf-8") as f:
        spec_content = f.read()
    req_to_persona = len(re.findall(r"Source Persona:", spec_content))
    req_to_group = len(re.findall(r"Traceability:", spec_content))
    with open(tests_path, "r", encoding="utf-8") as f:
        tests = json.load(f).get("tests", [])
    test_to_req = sum(1 for t in tests if t.get("requirement_id"))
    return persona_to_group + req_to_persona + req_to_group + test_to_req

PIPELINES = {
    "manual": {"groups": "data/review_groups_manual.json", "personas": "personas/personas_manual.json", "spec": "spec/spec_manual.md", "tests": "tests/tests_manual.json", "output": "metrics/metrics_manual.json"},
    "automated": {"groups": "data/review_groups_auto.json", "personas": "personas/personas_auto.json", "spec": "spec/spec_auto.md", "tests": "tests/tests_auto.json", "output": "metrics/metrics_auto.json"},
    "hybrid": {"groups": "data/review_groups_hybrid.json", "personas": "personas/personas_hybrid.json", "spec": "spec/spec_hybrid.md", "tests": "tests/tests_hybrid.json", "output": "metrics/metrics_hybrid.json"},
}

def compute_pipeline_metrics(name, paths):
    print(f"Computing {name} pipeline metrics...")
    metrics = {
        "pipeline": name,
        "dataset_size": count_reviews(),
        "persona_count": count_personas(paths["personas"]),
        "requirements_count": count_requirements_from_spec(paths["spec"]),
        "tests_count": count_tests(paths["tests"]),
        "traceability_links": compute_traceability_links(paths["groups"], paths["personas"], paths["spec"], paths["tests"]),
        "review_coverage_ratio": compute_review_coverage(paths["groups"]),
        "traceability_ratio": compute_traceability_ratio(paths["spec"], paths["personas"]),
        "testability_rate": compute_testability_rate(paths["spec"], paths["tests"]),
        "ambiguity_ratio": compute_ambiguity_ratio(paths["spec"]),
    }
    with open(paths["output"], "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    for k,v in metrics.items(): print(f"  {k}: {v}")
    return metrics

if __name__ == "__main__":
    all_metrics = {}
    for name, paths in PIPELINES.items():
        all_metrics[name] = compute_pipeline_metrics(name, paths)
    summary = {n: {k:v for k,v in m.items() if k != "pipeline"} for n,m in all_metrics.items()}
    with open("metrics/metrics_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print("Metrics computation complete.")
