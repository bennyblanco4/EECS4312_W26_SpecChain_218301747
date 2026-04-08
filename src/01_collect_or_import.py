"""
Collects raw reviews for the MindDoc app (package: de.moodpath.android)
from the Google Play Store using the google-play-scraper library.

Saves up to 5000 English reviews to: data/reviews_raw.jsonl
Each line is a JSON object with fields: id, content, score, date, version.

Usage:
    python src/01_collect_or_import.py
"""

import json
import os
from datetime import datetime

from google_play_scraper import reviews, Sort

APP_ID = "de.moodpath.android"
MAX_REVIEWS = 5000
OUTPUT_PATH = os.path.join("data", "reviews_raw.jsonl")


def collect_reviews():
    print(f"Collecting reviews for {APP_ID}...")
    all_reviews = []
    continuation_token = None

    while len(all_reviews) < MAX_REVIEWS:
        batch_size = min(200, MAX_REVIEWS - len(all_reviews))
        result, continuation_token = reviews(
            APP_ID,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=batch_size,
            continuation_token=continuation_token,
        )
        if not result:
            break
        all_reviews.extend(result)
        print(f"  Collected {len(all_reviews)} reviews so far...")
        if continuation_token is None:
            break

    print(f"Total collected: {len(all_reviews)} reviews")
    return all_reviews


def save_reviews(raw_reviews):
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for i, r in enumerate(raw_reviews):
            record = {
                "id": f"rev_{i+1}",
                "original_id": r.get("reviewId", ""),
                "content": r.get("content", ""),
                "score": r.get("score", 0),
                "date": str(r.get("at", "")),
                "version": r.get("appVersion", ""),
            }
            f.write(json.dumps(record) + "\n")
    print(f"Saved {len(raw_reviews)} raw reviews to {OUTPUT_PATH}")


if __name__ == "__main__":
    raw = collect_reviews()
    save_reviews(raw)
