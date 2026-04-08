"""
Cleans the raw MindDoc reviews dataset.

Cleaning steps applied:
  1. Remove duplicate reviews (by content)
  2. Remove empty/null entries
  3. Remove extremely short reviews (< 10 characters)
  4. Remove punctuation and special characters/emojis
  5. Convert numbers to text (e.g., "5" -> "five")
  6. Remove extra whitespace
  7. Convert all words to lowercase
  8. Remove stop words (NLTK English stopwords)
  9. Lemmatize words (NLTK WordNetLemmatizer)

Reads:  data/reviews_raw.jsonl
Writes: data/reviews_clean.jsonl
        data/dataset_metadata.json

Usage:
    python src/02_clean.py
"""

import json
import os
import re
import string
from datetime import datetime

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK data is available
for resource in ["stopwords", "wordnet", "omw-1.4"]:
    try:
        nltk.data.find(f"corpora/{resource}")
    except LookupError:
        nltk.download(resource, quiet=True)

RAW_PATH = os.path.join("data", "reviews_raw.jsonl")
CLEAN_PATH = os.path.join("data", "reviews_clean.jsonl")
METADATA_PATH = os.path.join("data", "dataset_metadata.json")

NUMBER_MAP = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "nine", "9": "nine",
    "10": "ten",
}

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()


def convert_numbers_to_text(text: str) -> str:
    """Replace standalone digit sequences with their English word equivalents."""
    def replace_num(m):
        n = m.group(0)
        return NUMBER_MAP.get(n, n)
    return re.sub(r"\b\d+\b", replace_num, text)


def clean_text(text: str) -> str:
    """Apply the full cleaning pipeline to a single review string."""
    # Remove emojis and non-ASCII characters
    text = text.encode("ascii", errors="ignore").decode("ascii")
    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+", "", text)
    # Remove punctuation and special characters (keep letters, digits, spaces)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    # Convert numbers to text
    text = convert_numbers_to_text(text)
    # Lowercase
    text = text.lower()
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Tokenize, remove stop words, lemmatize
    tokens = text.split()
    tokens = [LEMMATIZER.lemmatize(t) for t in tokens if t not in STOP_WORDS]
    return " ".join(tokens)


def load_raw():
    records = []
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def clean_dataset(raw_records):
    seen_contents = set()
    removed_duplicates = 0
    removed_empty = 0
    removed_short = 0
    cleaned = []

    for r in raw_records:
        original = r.get("content", "")

        # Remove empty
        if not original or not original.strip():
            removed_empty += 1
            continue

        # Remove extremely short (< 10 chars raw)
        if len(original.strip()) < 10:
            removed_short += 1
            continue

        # Remove duplicates
        norm_key = original.strip().lower()
        if norm_key in seen_contents:
            removed_duplicates += 1
            continue
        seen_contents.add(norm_key)

        cleaned_content = clean_text(original)

        # After cleaning, skip if result is very short (< 3 tokens)
        if len(cleaned_content.split()) < 3:
            removed_short += 1
            continue

        cleaned.append({
            "id": r["id"],
            "content_raw": original,
            "content_clean": cleaned_content,
            "score": r.get("score", 0),
            "date": r.get("date", ""),
            "version": r.get("version", ""),
        })

    stats = {
        "raw_count": len(raw_records),
        "removed_duplicates": removed_duplicates,
        "removed_empty": removed_empty,
        "removed_short": removed_short,
        "final_count": len(cleaned),
    }
    return cleaned, stats


def save_clean(cleaned):
    with open(CLEAN_PATH, "w", encoding="utf-8") as f:
        for r in cleaned:
            f.write(json.dumps(r) + "\n")
    print(f"Saved {len(cleaned)} clean reviews to {CLEAN_PATH}")


def save_metadata(stats):
    metadata = {
        "app_name": "MindDoc: Mental Health Support",
        "app_id": "de.moodpath.android",
        "platform": "Google Play Store",
        "collection_method": "google-play-scraper library (python), sorted by newest, English reviews",
        "collection_date": datetime.now().strftime("%Y-%m-%d"),
        "raw_dataset_size": stats["raw_count"],
        "final_dataset_size": stats["final_count"],
        "cleaning_decisions": {
            "removed_duplicates": stats["removed_duplicates"],
            "removed_empty": stats["removed_empty"],
            "removed_short_reviews": stats["removed_short"],
            "min_raw_length_chars": 10,
            "min_clean_length_tokens": 3,
            "steps": [
                "Remove duplicate reviews (by normalized content)",
                "Remove empty/null entries",
                "Remove reviews shorter than 10 raw characters",
                "Remove emojis and non-ASCII characters",
                "Remove URLs",
                "Remove punctuation and special characters",
                "Convert numbers to English words",
                "Convert to lowercase",
                "Remove extra whitespace",
                "Remove English stop words (NLTK)",
                "Lemmatize tokens (NLTK WordNetLemmatizer)",
                "Remove reviews with fewer than 3 tokens after cleaning",
            ],
        },
        "note": (
            "MindDoc has approximately 45,000+ reviews on Google Play. "
            "We extracted the 5,000 most recent English reviews due to API limits."
        ),
    }
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata to {METADATA_PATH}")


if __name__ == "__main__":
    print("Loading raw reviews...")
    raw = load_raw()
    print(f"  Loaded {len(raw)} raw reviews")

    print("Cleaning reviews...")
    cleaned, stats = clean_dataset(raw)

    print(f"  Raw: {stats['raw_count']}")
    print(f"  Removed duplicates: {stats['removed_duplicates']}")
    print(f"  Removed empty: {stats['removed_empty']}")
    print(f"  Removed short: {stats['removed_short']}")
    print(f"  Final clean: {stats['final_count']}")

    save_clean(cleaned)
    save_metadata(stats)
    print("Cleaning complete.")
