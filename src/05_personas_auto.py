"""
Automated review grouping and persona generation pipeline for MindDoc.

Step 4.1: Groups similar reviews using TF-IDF + K-Means clustering,
          then uses the Groq LLM to label and describe each group.
Step 4.2: Uses the Groq LLM to generate structured persona objects
          from the auto-generated review groups.

Requires: GROQ_API_KEY environment variable
Model:    meta-llama/llama-4-scout-17b-16e-instruct

Reads:  data/reviews_clean.jsonl
Writes: data/review_groups_auto.json
        personas/personas_auto.json
        prompts/prompt_auto.json

Usage:
    export GROQ_API_KEY=your_key_here
    python src/05_personas_auto.py
"""

import json
import os
import random
import sys
from collections import defaultdict

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

CLEAN_PATH = os.path.join("data", "reviews_clean.jsonl")
GROUPS_AUTO_PATH = os.path.join("data", "review_groups_auto.json")
PERSONAS_AUTO_PATH = os.path.join("personas", "personas_auto.json")
PROMPTS_PATH = os.path.join("prompts", "prompt_auto.json")

N_CLUSTERS = 5
REVIEWS_PER_GROUP_SAMPLE = 10
RANDOM_SEED = 42

GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def load_clean_reviews():
    records = []
    with open(CLEAN_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def cluster_reviews(reviews, n_clusters=N_CLUSTERS):
    """Cluster reviews using TF-IDF vectorization and K-Means."""
    texts = [r["content_clean"] for r in reviews]
    vectorizer = TfidfVectorizer(max_features=2000, min_df=3, max_df=0.85)
    X = vectorizer.fit_transform(texts)
    kmeans = KMeans(n_clusters=n_clusters, random_state=RANDOM_SEED, n_init=10)
    labels = kmeans.fit_predict(X)
    return labels


def build_cluster_groups(reviews, labels):
    """Build group dictionaries mapping cluster label -> list of reviews."""
    groups = defaultdict(list)
    for review, label in zip(reviews, labels):
        groups[label].append(review)
    return groups


def call_groq(client, prompt: str) -> str:
    """Call the Groq API and return the text response."""
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()


def generate_group_theme(client, sample_reviews: list[str], group_index: int) -> dict:
    """Use the LLM to generate a theme and description for a review cluster."""
    reviews_text = "\n".join(f"- {r}" for r in sample_reviews[:10])
    prompt = (
        f"You are analyzing user reviews for MindDoc, a mental health tracking app.\n"
        f"The following {len(sample_reviews[:10])} reviews belong to the same cluster "
        f"(Cluster {group_index + 1}):\n\n"
        f"{reviews_text}\n\n"
        f"Based on these reviews, provide:\n"
        f"1. A short theme label (3-6 words, e.g. 'Subscription and paywall frustration')\n"
        f"2. A 1-2 sentence description of the common feedback in this group\n\n"
        f"Respond in this JSON format only (no extra text):\n"
        f'{{"theme": "...", "description": "..."}}'
    )
    raw = call_groq(client, prompt)
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except Exception:
        return {"theme": f"Review cluster {group_index + 1}", "description": raw[:200]}


def generate_persona(client, group: dict) -> dict:
    """Use the LLM to generate a structured persona object from a review group."""
    sample_reviews = "\n".join(f"- {r['content_raw'][:200]}" for r in group["sample_reviews"][:8])
    prompt = (
        f"You are a software requirements engineer analyzing user reviews for MindDoc, "
        f"a mental health tracking and support app.\n\n"
        f"Review group theme: \"{group['theme']}\"\n"
        f"Group description: \"{group['description']}\"\n\n"
        f"Sample reviews from this group:\n{sample_reviews}\n\n"
        f"Create a user persona that represents this group. Respond with valid JSON only "
        f"(no explanation, no markdown fences):\n"
        f'{{"id": "P_auto_{group["group_id"]}", "name": "...", "description": "...", '
        f'"derived_from_group": "{group["group_id"]}", '
        f'"goals": ["...", "..."], '
        f'"pain_points": ["...", "..."], '
        f'"context": ["...", "..."], '
        f'"constraints": ["...", "..."], '
        f'"evidence_reviews": [list of 2-4 review IDs from: {[r["id"] for r in group["sample_reviews"][:4]]}]}}'
    )
    raw = call_groq(client, prompt)
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except Exception:
        return {
            "id": f'P_auto_{group["group_id"]}',
            "name": group["theme"],
            "description": group["description"],
            "derived_from_group": group["group_id"],
            "goals": [],
            "pain_points": [],
            "context": [],
            "constraints": [],
            "evidence_reviews": [],
            "llm_parse_error": raw[:300],
        }


def run_pipeline():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY environment variable is not set.")
        print("Set it with: export GROQ_API_KEY=your_key_here")
        sys.exit(1)

    from groq import Groq
    client = Groq(api_key=api_key)

    print("Loading clean reviews...")
    reviews = load_clean_reviews()
    print(f"  Loaded {len(reviews)} reviews")

    print(f"Clustering reviews into {N_CLUSTERS} groups using TF-IDF + K-Means...")
    labels = cluster_reviews(reviews, N_CLUSTERS)

    raw_groups = build_cluster_groups(reviews, labels)
    print(f"  Cluster sizes: { {k: len(v) for k, v in raw_groups.items()} }")

    # Sample reviews per group for LLM prompts
    groups_for_llm = []
    random.seed(RANDOM_SEED)
    for i, (label, group_reviews) in enumerate(sorted(raw_groups.items())):
        sample = random.sample(group_reviews, min(REVIEWS_PER_GROUP_SAMPLE, len(group_reviews)))
        groups_for_llm.append({
            "label": label,
            "group_id": f"A{i+1}",
            "all_reviews": group_reviews,
            "sample_reviews": sample,
        })

    # Step 4.1: Generate group themes using LLM
    print("Generating group themes using Groq LLM...")
    review_groups_output = {"groups": []}
    prompts_used = []

    for g in groups_for_llm:
        print(f"  Processing group {g['group_id']} ({len(g['all_reviews'])} reviews)...")
        sample_texts = [r["content_raw"] for r in g["sample_reviews"]]
        theme_data = generate_group_theme(client, sample_texts, g["label"])
        g["theme"] = theme_data.get("theme", f"Cluster {g['label']}")
        g["description"] = theme_data.get("description", "")

        review_groups_output["groups"].append({
            "group_id": g["group_id"],
            "theme": g["theme"],
            "description": g["description"],
            "review_ids": [r["id"] for r in g["all_reviews"]],
            "example_reviews": [r["content_raw"][:200] for r in g["sample_reviews"][:5]],
        })

        prompts_used.append({
            "step": "group_theme_labeling",
            "group_id": g["group_id"],
            "model": GROQ_MODEL,
            "sample_size": len(sample_texts),
        })

    # Save review groups
    with open(GROUPS_AUTO_PATH, "w", encoding="utf-8") as f:
        json.dump(review_groups_output, f, indent=2, ensure_ascii=False)
    print(f"  Saved auto review groups to {GROUPS_AUTO_PATH}")

    # Step 4.2: Generate personas using LLM
    print("Generating personas using Groq LLM...")
    personas_output = {"personas": []}

    for g in groups_for_llm:
        print(f"  Generating persona for group {g['group_id']}...")
        persona = generate_persona(client, g)
        personas_output["personas"].append(persona)
        prompts_used.append({
            "step": "persona_generation",
            "group_id": g["group_id"],
            "model": GROQ_MODEL,
            "sample_reviews_used": len(g["sample_reviews"][:8]),
        })

    # Save personas
    with open(PERSONAS_AUTO_PATH, "w", encoding="utf-8") as f:
        json.dump(personas_output, f, indent=2, ensure_ascii=False)
    print(f"  Saved auto personas to {PERSONAS_AUTO_PATH}")

    # Save prompt metadata
    prompt_record = {
        "model": GROQ_MODEL,
        "clustering_approach": "TF-IDF vectorization (max 2000 features) + K-Means (k=5, n_init=10)",
        "prompts": prompts_used,
        "prompt_templates": {
            "group_theme_labeling": (
                "You are analyzing user reviews for MindDoc... "
                "[sample reviews listed] ... provide a theme label and description in JSON"
            ),
            "persona_generation": (
                "You are a software requirements engineer... "
                "[group theme, description, sample reviews] ... create a user persona in JSON"
            ),
        },
    }
    with open(PROMPTS_PATH, "w", encoding="utf-8") as f:
        json.dump(prompt_record, f, indent=2, ensure_ascii=False)
    print(f"  Saved prompts metadata to {PROMPTS_PATH}")

    print("Automated pipeline (grouping + personas) complete.")


if __name__ == "__main__":
    run_pipeline()
