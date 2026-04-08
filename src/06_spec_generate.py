"""
Generates structured software requirements (spec) from automated personas.

Reads:  personas/personas_auto.json
Writes: spec/spec_auto.md

Each requirement includes:
  - Unique requirement ID (FR_auto_N)
  - Description of system behavior
  - Source persona
  - Traceability to review group
  - Acceptance criteria

Requires: GROQ_API_KEY environment variable (if using live LLM generation)
          If GROQ_API_KEY is not set, runs in offline mode using template-based generation.

Usage:
    export GROQ_API_KEY=your_key_here
    python src/06_spec_generate.py
"""

import json
import os
import sys

PERSONAS_PATH = os.path.join("personas", "personas_auto.json")
SPEC_AUTO_PATH = os.path.join("spec", "spec_auto.md")

GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def load_personas():
    with open(PERSONAS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["personas"]


def call_groq(client, prompt: str) -> str:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2048,
    )
    return response.choices[0].message.content.strip()


def generate_requirements_for_persona_llm(client, persona: dict, req_start_idx: int) -> list[dict]:
    """Use LLM to generate 2-3 requirements for a given persona."""
    prompt = (
        f"You are a software requirements engineer working on MindDoc, a mental health tracking app.\n\n"
        f"Based on the following user persona, generate exactly 3 software requirements.\n\n"
        f"Persona:\n"
        f"  Name: {persona['name']}\n"
        f"  Description: {persona['description']}\n"
        f"  Goals: {', '.join(persona['goals'])}\n"
        f"  Pain Points: {', '.join(persona['pain_points'])}\n"
        f"  Derived from group: {persona['derived_from_group']}\n\n"
        f"For each requirement, provide:\n"
        f"- requirement_id: FR_auto_{req_start_idx}, FR_auto_{req_start_idx+1}, FR_auto_{req_start_idx+2}\n"
        f"- description: a clear system behavior statement starting with 'The system shall...'\n"
        f"- source_persona: the persona name\n"
        f"- traceability: the review group ID\n"
        f"- acceptance_criteria: a testable Given/When/Then statement\n\n"
        f"Respond with valid JSON only:\n"
        f'[{{"requirement_id": "...", "description": "...", "source_persona": "...", '
        f'"traceability": "...", "acceptance_criteria": "..."}}]'
    )
    raw = call_groq(client, prompt)
    try:
        start = raw.find("[")
        end = raw.rfind("]") + 1
        return json.loads(raw[start:end])
    except Exception:
        return []


def generate_requirements_template(persona: dict, req_start_idx: int) -> list[dict]:
    """Template-based requirement generation when LLM is unavailable."""
    pid = persona["id"]
    group = persona["derived_from_group"]
    name = persona["name"]
    goals = persona.get("goals", [])
    pains = persona.get("pain_points", [])

    reqs = []
    if goals:
        reqs.append({
            "requirement_id": f"FR_auto_{req_start_idx}",
            "description": f"The system shall support {goals[0].lower()} for users in the {name} segment.",
            "source_persona": name,
            "traceability": f"Derived from review group {group}",
            "acceptance_criteria": (
                f"Given a user matching the {name} profile, "
                f"when they interact with the relevant feature, "
                f"then the system must fulfill: {goals[0].lower()}."
            ),
        })
    if len(goals) > 1:
        reqs.append({
            "requirement_id": f"FR_auto_{req_start_idx+1}",
            "description": f"The system shall enable users to {goals[1].lower()}.",
            "source_persona": name,
            "traceability": f"Derived from review group {group}",
            "acceptance_criteria": (
                f"Given a user with the goal to {goals[1].lower()}, "
                f"when they use the app, then the system must provide the necessary support."
            ),
        })
    if pains:
        reqs.append({
            "requirement_id": f"FR_auto_{req_start_idx+2}",
            "description": f"The system shall address the pain point: {pains[0].lower()}.",
            "source_persona": name,
            "traceability": f"Derived from review group {group}",
            "acceptance_criteria": (
                f"Given a user who experiences {pains[0].lower()}, "
                f"when the problematic scenario occurs, "
                f"then the system must prevent or resolve the issue."
            ),
        })
    return reqs


def write_spec(requirements: list[dict]):
    lines = [
        "# MindDoc Automated Specification",
        "**App:** MindDoc: Mental Health Support",
        "**Pipeline:** Automated",
        "**Derived from:** personas/personas_auto.json",
        "",
        "---",
        "",
    ]
    for req in requirements:
        lines.append(f"## Requirement ID: {req['requirement_id']}")
        lines.append("")
        lines.append(f"- **Description:** {req['description']}")
        lines.append(f"- **Source Persona:** {req['source_persona']}")
        lines.append(f"- **Traceability:** {req['traceability']}")
        lines.append(f"- **Acceptance Criteria:** {req['acceptance_criteria']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    with open(SPEC_AUTO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Saved {len(requirements)} requirements to {SPEC_AUTO_PATH}")


def run():
    api_key = os.getenv("GROQ_API_KEY")
    personas = load_personas()
    print(f"Loaded {len(personas)} automated personas")

    all_requirements = []
    req_idx = 1

    if api_key:
        from groq import Groq
        client = Groq(api_key=api_key)
        for persona in personas:
            print(f"  Generating requirements for persona: {persona['name']}...")
            reqs = generate_requirements_for_persona_llm(client, persona, req_idx)
            all_requirements.extend(reqs)
            req_idx += len(reqs) if reqs else 3
    else:
        print("No GROQ_API_KEY found. Using template-based generation.")
        for persona in personas:
            reqs = generate_requirements_template(persona, req_idx)
            all_requirements.extend(reqs)
            req_idx += 3

    write_spec(all_requirements)
    print(f"Spec generation complete: {len(all_requirements)} requirements")


if __name__ == "__main__":
    run()
