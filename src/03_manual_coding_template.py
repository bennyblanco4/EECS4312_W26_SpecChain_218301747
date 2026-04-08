"""
Template and instructions for manually coding review groups.

This script provides a guide and data structure template to assist in
the manual identification of review groups from the cleaned dataset.

Usage:
    python src/03_manual_coding_template.py
"""

import json
import os

CLEAN_PATH = os.path.join("data", "reviews_clean.jsonl")
OUTPUT_TEMPLATE_PATH = os.path.join("data", "review_groups_manual_template.json")


def load_sample_reviews(n=20):
    records = []
    with open(CLEAN_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
            if len(records) >= n:
                break
    return records


def generate_template():
    print("=== Manual Coding Instructions ===")
    print()
    print("1. Open data/reviews_clean.jsonl and read through the reviews.")
    print("2. Identify 5 groups of reviews representing distinct user types or situations.")
    print("3. Each group must include at least 10 review IDs.")
    print("4. Fill in the template below and save as data/review_groups_manual.json.")
    print()
    print("=== Sample Reviews (first 20) ===")
    reviews = load_sample_reviews(20)
    for r in reviews:
        print(f"  [{r['id']}] score={r['score']}: {r['content_raw'][:120]}")
    print()

    template = {
        "groups": [
            {
                "group_id": "G1",
                "theme": "[FILL IN: short theme name e.g. 'Subscription frustration']",
                "description": "[FILL IN: 1-2 sentence description of common feedback]",
                "review_ids": ["[FILL IN: rev_X, rev_Y, ... at least 10]"],
                "example_reviews": [
                    "[FILL IN: paste 3-5 representative review texts]",
                ],
            }
        ]
    }
    for i in range(2, 6):
        template["groups"].append({
            "group_id": f"G{i}",
            "theme": f"[FILL IN group {i} theme]",
            "description": f"[FILL IN group {i} description]",
            "review_ids": ["[FILL IN]"],
            "example_reviews": ["[FILL IN]"],
        })

    with open(OUTPUT_TEMPLATE_PATH, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2)
    print(f"Template written to {OUTPUT_TEMPLATE_PATH}")
    print("Fill in the template and copy to data/review_groups_manual.json when complete.")


if __name__ == "__main__":
    generate_template()
