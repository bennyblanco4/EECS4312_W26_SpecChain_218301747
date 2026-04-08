# Reflection: Comparing Manual, Automated, and Hybrid Pipelines

**App:** MindDoc: Mental Health Support (package: de.moodpath.android)
**Student ID:** 218301747
**Course:** EECS 4312 – Software Requirements Engineering, Winter 2026

---

## Pipeline Overview

This project implemented three pipelines for transforming 4,278 cleaned Google Play reviews into structured software artifacts: personas, specifications, and validation tests. The three pipelines — manual, automated, and hybrid — produced measurably different outputs that reveal important trade-offs in requirements engineering practice.

---

## Differences Between the Pipelines

**Manual pipeline:** Reading through reviews one by one allowed for thematic nuance that no algorithm captured automatically. The five manual groups (paywall frustration, mood tracking, notification reliability, data privacy, therapeutic content) were clean and non-overlapping, each representing a genuinely distinct type of user concern. However, with only 65 reviews covered across 5 groups (coverage ratio: 0.0152), the manual pipeline necessarily worked with a small, curated slice of the dataset. This is a fundamental limitation: a human reading thousands of reviews for deep coding is impractical at scale.

**Automated pipeline:** K-Means clustering with TF-IDF features assigned every review to a cluster, yielding 100% review coverage. This is the automated pipeline's clearest advantage. However, one cluster (A2: Daily check-ins, reminders, and subscription concerns) absorbed 2,101 reviews — nearly half the dataset — into a single group combining two quite different user concerns (notification habits and pricing frustration). The LLM-generated requirement descriptions also tended to use more vague language ("easy-to-understand," "timely," "meaningful"), resulting in a measured ambiguity ratio of 0.27.

**Hybrid pipeline:** Beginning with the automated outputs and revising them produced the most refined artifacts. Themes were renamed to remove ambiguous words, persona descriptions were grounded more specifically in review evidence, and specifications added measurable thresholds (e.g., ten-minute notification delivery tolerance, 30-second chart update, 24-month data retention). However, the hybrid specification still contained some vague terms ("clear," "accessible," "plain-language") because not all qualitative language can be eliminated without losing meaningful context.

---

## Which Pipeline Produced the Clearest Personas?

The **manual pipeline** produced the clearest, most grounded personas. Each persona was directly tied to a coherent, hand-curated group of reviews. For example, the Privacy-Aware Mental Health User (P4) was derived from reviews explicitly discussing third-party data sharing, mandatory account creation, and the absence of app lock features — a specific cluster of concerns that the automated clustering diluted across multiple groups.

The automated personas, while structurally complete, sometimes included unsupported claims. For example, the auto-generated persona for A5 claimed users rely on "guided coping exercises" — a feature that reviewers in that cluster rarely discussed. The hybrid pipeline corrected this by removing unsupported assumptions from auto personas.

---

## Which Pipeline Produced the Most Useful Requirements?

The **hybrid pipeline** produced the most useful requirements. Manual requirements were well-grounded but some were slightly vague (e.g., FR7: "allow users to access basic features" without defining what "basic" means). The automated requirements were broader in coverage but harder to test (e.g., FR_auto_1 required an "easy-to-understand" onboarding without defining what easy means). The hybrid requirements added concrete measurable criteria: specific time tolerances, minimum counts, and behavioral constraints that make each requirement directly verifiable.

---

## Which Pipeline Had the Strongest Traceability?

All three pipelines achieved a traceability ratio of 1.0 — every requirement was explicitly linked to a persona and a review group. However, the **hybrid pipeline** had the strongest semantic traceability: the links were grounded in revised, coherent review groups whose themes accurately described the clustered reviews. The automated pipeline's traceability links were formally present but some pointed back to an overly broad group (A2 with 2,101 mixed reviews), weakening the semantic meaning of the trace.

---

## Problems in the Automated Outputs

1. **Large, mixed clusters:** The K-Means algorithm produced one cluster with 2,101 reviews covering unrelated concerns (notification reliability and subscription frustration). This reflects a fundamental limitation of bag-of-words clustering: semantically distinct concerns may share overlapping vocabulary.

2. **Vague requirements:** The LLM-generated requirements frequently used imprecise language. Terms like "easy," "timely," and "meaningful" appear in requirements without measurable thresholds, reducing testability.

3. **Unsupported persona claims:** Some automated personas included assumptions not directly supported by the review evidence (e.g., attributing coping exercise engagement to users who primarily reviewed mood tracking).

4. **Repetitive test steps:** Template-based test generation produced generic steps ("Open the app," "Navigate to the relevant feature") that do not provide specific enough guidance for real test execution.

---

## Summary

| Metric | Manual | Automated | Hybrid |
|---|---|---|---|
| Dataset size | 4,278 | 4,278 | 4,278 |
| Personas | 5 | 5 | 5 |
| Requirements | 12 | 15 | 15 |
| Tests | 24 | 30 | 30 |
| Review coverage | 1.52% | 100% | 100% |
| Traceability ratio | 1.00 | 1.00 | 1.00 |
| Testability rate | 1.00 | 1.00 | 1.00 |
| Ambiguity ratio | 0.42 | 0.27 | 0.53 |

The hybrid pipeline is the recommended approach for practical requirements engineering: automation provides speed and comprehensive review coverage, while human judgment catches incoherent groupings, removes unsupported claims, and adds the measurable specificity that makes requirements testable in practice.
