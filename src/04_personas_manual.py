"""
Displays and validates the manually created personas from personas_manual.json.

This script reads the manual personas file and prints a formatted summary
to help review the persona content before proceeding to spec generation.

Usage:
    python src/04_personas_manual.py
"""

import json, os

PERSONAS_PATH = os.path.join("personas", "personas_manual.json")
GROUPS_PATH = os.path.join("data", "review_groups_manual.json")


def validate_personas(personas, groups):
    group_ids = {g["group_id"] for g in groups.get("groups", [])}
    issues = []
    for p in personas:
        pid = p.get("id", "?")
        if not p.get("name"): issues.append(f"{pid}: missing name")
        if not p.get("description"): issues.append(f"{pid}: missing description")
        if not p.get("derived_from_group"): issues.append(f"{pid}: missing derived_from_group")
        elif p["derived_from_group"] not in group_ids:
            issues.append(f"{pid}: derived_from_group {p['derived_from_group']} not in review groups")
        if len(p.get("goals", [])) < 2: issues.append(f"{pid}: fewer than 2 goals")
        if len(p.get("pain_points", [])) < 2: issues.append(f"{pid}: fewer than 2 pain_points")
        if len(p.get("evidence_reviews", [])) < 1: issues.append(f"{pid}: no evidence_reviews")
    return issues


def main():
    with open(PERSONAS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(GROUPS_PATH, "r", encoding="utf-8") as f:
        groups = json.load(f)

    personas = data.get("personas", [])
    print(f"=== Manual Personas Summary ===")
    print(f"Total personas: {len(personas)}")
    print()
    for p in personas:
        print(f"  [{p.get('id')}] {p.get('name')}")
        print(f"    Group: {p.get('derived_from_group')}")
        print(f"    Goals: {len(p.get('goals',[]))}")
        print(f"    Pain points: {len(p.get('pain_points',[]))}")
        print(f"    Evidence reviews: {p.get('evidence_reviews',[])}")
        print()

    issues = validate_personas(personas, groups)
    if issues:
        print("Validation issues:")
        for issue in issues: print(f"  - {issue}")
    else:
        print("All personas validated successfully.")


if __name__ == "__main__":
    main()
