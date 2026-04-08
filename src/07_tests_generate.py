"""
Generates structured validation tests from the automated specification.

Reads:  spec/spec_auto.md
Writes: tests/tests_auto.json

Each test scenario contains:
  - test_id: unique identifier
  - requirement_id: the requirement being tested
  - scenario: short description
  - steps: ordered list of test steps
  - expected_result: what should happen if the system works correctly

Requires: GROQ_API_KEY environment variable (if using live LLM generation)
          If GROQ_API_KEY is not set, runs in template mode.

Usage:
    export GROQ_API_KEY=your_key_here
    python src/07_tests_generate.py
"""

import json
import os
import re
import sys

SPEC_PATH = os.path.join("spec", "spec_auto.md")
TESTS_AUTO_PATH = os.path.join("tests", "tests_auto.json")

GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def parse_spec(spec_path: str) -> list[dict]:
    """Parse spec_auto.md and extract requirements."""
    requirements = []
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"^## Requirement ID:", content, flags=re.MULTILINE)
    for block in blocks[1:]:
        lines = block.strip().split("\n")
        req_id = lines[0].strip()
        req = {"requirement_id": req_id}
        for line in lines[1:]:
            if line.startswith("- **Description:**"):
                req["description"] = line.replace("- **Description:**", "").strip()
            elif line.startswith("- **Source Persona:**"):
                req["source_persona"] = line.replace("- **Source Persona:**", "").strip()
            elif line.startswith("- **Acceptance Criteria:**"):
                req["acceptance_criteria"] = line.replace("- **Acceptance Criteria:**", "").strip()
        if "description" in req:
            requirements.append(req)
    return requirements


def call_groq(client, prompt: str) -> str:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()


def generate_tests_llm(client, req: dict, test_idx: int) -> list[dict]:
    """Use LLM to generate 2 test scenarios for a requirement."""
    prompt = (
        f"Generate 2 test scenarios for this software requirement from MindDoc app:\n\n"
        f"Requirement ID: {req['requirement_id']}\n"
        f"Description: {req['description']}\n"
        f"Acceptance Criteria: {req.get('acceptance_criteria', '')}\n\n"
        f"For each test, provide:\n"
        f"- test_id: T_auto_{test_idx} and T_auto_{test_idx+1}\n"
        f"- requirement_id: {req['requirement_id']}\n"
        f"- scenario: a short scenario name\n"
        f"- steps: a list of 3-5 test steps\n"
        f"- expected_result: what should happen if the system works correctly\n\n"
        f"Respond with valid JSON array only:\n"
        f'[{{"test_id": "...", "requirement_id": "...", "scenario": "...", "steps": ["..."], "expected_result": "..."}}]'
    )
    raw = call_groq(client, prompt)
    try:
        start = raw.find("[")
        end = raw.rfind("]") + 1
        return json.loads(raw[start:end])
    except Exception:
        return []


def generate_tests_template(req: dict, test_idx: int) -> list[dict]:
    """Template-based test generation when LLM is unavailable."""
    req_id = req["requirement_id"]
    desc = req.get("description", "")
    criteria = req.get("acceptance_criteria", "")

    return [
        {
            "test_id": f"T_auto_{test_idx}",
            "requirement_id": req_id,
            "scenario": f"Verify: {desc[:80].rstrip('.')}",
            "steps": [
                "Open the MindDoc application",
                "Navigate to the relevant feature section",
                f"Perform the action described in {req_id}",
                "Observe the system response",
            ],
            "expected_result": (
                criteria if criteria
                else f"The system behaves as described in {req_id}: {desc[:100]}"
            ),
        },
        {
            "test_id": f"T_auto_{test_idx+1}",
            "requirement_id": req_id,
            "scenario": f"Boundary check for {req_id}",
            "steps": [
                "Open the MindDoc application",
                "Attempt to trigger the feature in an edge case scenario",
                f"Verify the system handles the edge case for {req_id}",
            ],
            "expected_result": (
                f"The system remains stable and does not expose errors. "
                f"The requirement described in {req_id} is satisfied."
            ),
        },
    ]


def run():
    api_key = os.getenv("GROQ_API_KEY")

    print("Parsing spec_auto.md...")
    requirements = parse_spec(SPEC_PATH)
    print(f"  Found {len(requirements)} requirements")

    all_tests = []
    test_idx = 1

    if api_key:
        from groq import Groq
        client = Groq(api_key=api_key)
        for req in requirements:
            print(f"  Generating tests for {req['requirement_id']}...")
            tests = generate_tests_llm(client, req, test_idx)
            all_tests.extend(tests)
            test_idx += len(tests) if tests else 2
    else:
        print("No GROQ_API_KEY found. Using template-based test generation.")
        for req in requirements:
            tests = generate_tests_template(req, test_idx)
            all_tests.extend(tests)
            test_idx += 2

    output = {"tests": all_tests}
    with open(TESTS_AUTO_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_tests)} tests to {TESTS_AUTO_PATH}")


if __name__ == "__main__":
    run()
