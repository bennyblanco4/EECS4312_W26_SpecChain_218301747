# MindDoc Hybrid Specification
**App:** MindDoc: Mental Health Support
**Pipeline:** Hybrid (automated outputs refined manually)
**Derived from:** personas/personas_hybrid.json

---

## Requirement ID: FR_hybrid_1

- **Description:** The system shall present a clear, linear onboarding flow that introduces each major feature (check-in, insights, exercises) with a brief plain-language description and an example interaction before reaching the main dashboard.
- **Source Persona:** P_hybrid_H1 – Broad Wellness Adopter
- **Traceability:** Derived from review group H1
- **Acceptance Criteria:** Given a new user opens the app for the first time, when they complete the onboarding flow, then they must have passed through at least one screen per major feature (check-in, insights, exercises) with a description of what that feature does. No clinical terminology may appear without an in-line explanation.
- **Notes:** Rewritten from FR_auto_1 to specify "linear onboarding," list exact features that must be introduced, and add the plain-language constraint. The auto version was too vague ("easy-to-understand") without measurable criteria.

---

## Requirement ID: FR_hybrid_2

- **Description:** The system shall provide at least three educational articles on distinct mental health topics (e.g., anxiety, depression, stress) that are written at a reading level accessible to general audiences and do not require clinical prior knowledge.
- **Source Persona:** P_hybrid_H1 – Broad Wellness Adopter
- **Traceability:** Derived from review group H1
- **Acceptance Criteria:** Given a user navigates to the educational content section, when they browse the article list, then at least three articles on distinct mental health topics must be present. Each article must be written without unexplained clinical jargon. A user unfamiliar with psychology must be able to understand the core message of each article.
- **Notes:** Rewritten from FR_auto_2. Added the specific count (three articles) and the topic diversity requirement. The original acceptance criteria was not measurable.

---

## Requirement ID: FR_hybrid_3

- **Description:** The system shall remain crash-free and responsive during the core user flow including app launch, check-in completion, navigation between the home, insights, and settings screens, and app resumption from background.
- **Source Persona:** P_hybrid_H1 – Broad Wellness Adopter
- **Traceability:** Derived from review group H1
- **Acceptance Criteria:** Given a user performs the core flow (launch → check-in → insights → settings → home), when each screen transition and check-in submission occurs, then no crash, force-close, or unhandled exception must occur. When the app is resumed from background after being inactive for up to ten minutes, it must restore to the previous screen within three seconds.
- **Notes:** Rewritten from FR_auto_3 to add specific screen coverage and a measurable resume time constraint. Auto version only said "no crashes during standard usage" without defining what standard usage means.

---

## Requirement ID: FR_hybrid_4

- **Description:** The system shall allow users to complete up to three check-in sessions per day, each consisting of structured mood and emotional state questions, with each session completing in under three minutes.
- **Source Persona:** P_hybrid_H2 – Reminder-Dependent Check-in User
- **Traceability:** Derived from review group H2
- **Acceptance Criteria:** Given a user opens the check-in screen, when they complete all questions and submit, then the session must be recorded to mood history within five seconds and the total interaction time from opening to confirmation must be under three minutes. A second and third check-in session must be available within the same calendar day.
- **Notes:** Retained core intent from FR_auto_4 but added the three-minute completion constraint and the five-second save confirmation requirement. These were absent in the auto version.

---

## Requirement ID: FR_hybrid_5

- **Description:** The system shall deliver push notification reminders at user-configured times with a maximum delivery delay of ten minutes, even if the app has been closed or the device screen is off.
- **Source Persona:** P_hybrid_H2 – Reminder-Dependent Check-in User
- **Traceability:** Derived from review group H2
- **Acceptance Criteria:** Given a user has configured at least one reminder time and the app has the necessary notification permissions, when the scheduled time arrives, then a push notification must be delivered within ten minutes regardless of whether the app is open or closed. Tapping the notification must open the check-in screen directly.
- **Notes:** Significantly strengthened from FR_auto_5. Added the ten-minute delay tolerance and the requirement that tapping the notification opens check-in directly. Auto version only said "deliver a visible push notification" without measurable timing criteria.

---

## Requirement ID: FR_hybrid_6

- **Description:** The system shall allow free-tier users to complete unlimited daily check-ins and access a basic mood summary (overall mood score and a brief trend description) without requiring a paid subscription.
- **Source Persona:** P_hybrid_H2 – Reminder-Dependent Check-in User
- **Traceability:** Derived from review group H2
- **Acceptance Criteria:** Given a user who has not subscribed to a premium plan, when they complete a check-in and navigate to their results, then both the check-in completion and the basic summary (mood score plus one-sentence trend description) must be available without a subscription prompt. Any premium upsell must be presented as a dismissible option and must not block the basic result.
- **Notes:** Rewritten from FR_auto_6. Added the specific content that must be available for free (mood score and brief trend description) and the requirement that any upsell must be dismissible. Auto version lacked specificity about what "basic result" means.

---

## Requirement ID: FR_hybrid_7

- **Description:** The system shall detect recurring mood patterns in a user's check-in history after seven or more consecutive days of data and display at least one specific, data-referenced insight describing the detected pattern.
- **Source Persona:** P_hybrid_H3 – Pattern-Seeking Self-Reflector
- **Traceability:** Derived from review group H3
- **Acceptance Criteria:** Given a user has completed at least one check-in per day for seven consecutive days, when they navigate to the insights section, then at least one insight must reference a specific observed pattern (e.g., "Your mood scores have been consistently lower on Monday mornings") rather than generic advice. The insight must include the time range of the pattern.
- **Notes:** Rewritten from FR_auto_7. Added the requirement that insights must reference specific data rather than generic advice. Auto version said "personalized observation" without specifying what makes it personalized.

---

## Requirement ID: FR_hybrid_8

- **Description:** The system shall ensure that no two consecutive check-in sessions present an identical set of questions, and that across any ten consecutive sessions, the question pool draws from at least fifteen distinct questions.
- **Source Persona:** P_hybrid_H3 – Pattern-Seeking Self-Reflector
- **Traceability:** Derived from review group H3
- **Acceptance Criteria:** Given a user completes two consecutive check-in sessions, when the question sets are compared, then the two sets must not be identical (at least one question must differ). Given a user completes ten consecutive sessions, when the full question history is reviewed, then at least fifteen distinct questions must have appeared across those ten sessions.
- **Notes:** Significantly strengthened from FR_auto_8. Added the specific ten-session / fifteen-question measurable constraint. Auto version only said "at least one question must differ" between sessions, which is a necessary but insufficient condition for meaningful variety.

---

## Requirement ID: FR_hybrid_9

- **Description:** The system shall provide an optional free-text journal entry field during each check-in session, and the entered text must be stored alongside the structured check-in data and remain retrievable for at least 12 months.
- **Source Persona:** P_hybrid_H3 – Pattern-Seeking Self-Reflector
- **Traceability:** Derived from review group H3
- **Acceptance Criteria:** Given a user completes a check-in and enters text in the journal field, when they submit the session, then the journal text must be stored linked to that check-in record. Given the user navigates to their check-in history, when they select a past entry, then the journal text from that entry must be displayed. Journal entries from more than 30 days ago must remain accessible.
- **Notes:** Extended from FR_auto_9 to add the retention requirement (12 months, verified at 30-day minimum). Auto version only required that the entry be saved and retrievable in the current session.

---

## Requirement ID: FR_hybrid_10

- **Description:** The system shall provide mood trend visualizations for weekly (7-day) and monthly (30-day) time ranges, with each chart updating to reflect newly completed check-ins within 30 seconds of submission.
- **Source Persona:** P_hybrid_H4 – Long-Term Emotional Trend Monitor
- **Traceability:** Derived from review group H4
- **Acceptance Criteria:** Given a user navigates to the mood history section, when they select either the weekly or monthly view, then a chart displaying mood data for the selected time range must appear. After a new check-in is submitted, when the user returns to the mood history section, then the chart must reflect the new data point within 30 seconds.
- **Notes:** Strengthened from FR_auto_10. Added the 30-second data freshness requirement. Auto version listed the requirement but had no constraint on how quickly charts would update after new data was entered.

---

## Requirement ID: FR_hybrid_11

- **Description:** The system shall retain all user check-in history, mood data, and journal entries for a minimum of 24 months from the date of entry and must not delete any user data when the app is updated or reinstalled.
- **Source Persona:** P_hybrid_H4 – Long-Term Emotional Trend Monitor
- **Traceability:** Derived from review group H4
- **Acceptance Criteria:** Given a user accesses their check-in history, when they scroll back to entries from more than 30 days ago, then those entries must be present and complete. Given the app is updated to a new version, when the user relaunches the app, then all previously stored check-in records, mood scores, and journal entries must remain intact.
- **Notes:** Extended from FR_auto_11 to add the 24-month retention minimum and the explicit protection against data loss during app updates. Auto version said "indefinitely" which is unmeasurable; 24 months is a concrete, testable threshold.

---

## Requirement ID: FR_hybrid_12

- **Description:** The system shall allow users to configure up to three daily reminder notifications at individually specified times, and changes to the schedule must take effect for the next scheduled notification without requiring an app restart.
- **Source Persona:** P_hybrid_H4 – Long-Term Emotional Trend Monitor
- **Traceability:** Derived from review group H4
- **Acceptance Criteria:** Given a user navigates to notification settings and sets up to three reminder times, when they save the configuration, then the settings must be persisted and the next notification must arrive at the newly configured time. If the user updates a reminder time that is more than ten minutes in the future, the notification system must reflect the change without an app restart.
- **Notes:** Rewritten from FR_auto_12 to consolidate with the notification reliability concern and add the "no restart required" testable condition. Auto version was split across FR_auto_5 and FR_auto_12 with overlapping concerns.

---

## Requirement ID: FR_hybrid_13

- **Description:** The system shall detect when a user's check-in response indicates severe psychological distress or thoughts of self-harm and must display a non-dismissible crisis support screen containing contact information for at least one regional crisis helpline before allowing the user to continue.
- **Source Persona:** P_hybrid_H5 – Mental Health Symptom-Aware User
- **Traceability:** Derived from review group H5
- **Acceptance Criteria:** Given a user selects a check-in response that indicates self-harm ideation or severe distress (e.g., a crisis-level response on any distress scale), when the response is submitted, then a crisis support screen must appear containing: (1) a supportive acknowledgment message, (2) at least one crisis helpline number appropriate to the user's detected region, and (3) a clearly labeled "I understand" button that the user must tap before the app proceeds. The screen must not be automatically dismissed or bypassed.
- **Notes:** Substantially rewritten from FR_auto_13. Added requirements for: the screen being non-dismissible, regional helpline information, and the mandatory acknowledgment button. Auto version only said "a supportive message and contact information" without specifying non-dismissibility or regional relevance.

---

## Requirement ID: FR_hybrid_14

- **Description:** The system shall present at least 20 distinct labeled emotion options during the emotional state selection step of each check-in, organized into categories of valence (positive, neutral, negative) and intensity (low, medium, high).
- **Source Persona:** P_hybrid_H5 – Mental Health Symptom-Aware User
- **Traceability:** Derived from review group H5
- **Acceptance Criteria:** Given a user reaches the emotion selection step in a check-in, when they view the emotion options, then at least 20 distinct labeled emotions must be displayed. The emotions must be visually or categorically organized into at minimum two valence groups (positive and negative). Both low-intensity and high-intensity emotions must be represented in each valence group.
- **Notes:** Raised the threshold from 15 (FR_auto_14) to 20 based on manual review of user feedback indicating that emotion options feel "limited." Added the organization requirement (valence × intensity) which was absent in the auto version.

---

## Requirement ID: FR_hybrid_15

- **Description:** The system shall recommend at least one specific, named coping exercise relevant to the user's dominant emotional state reported in the current check-in, and the recommendation must differ when distinctly different emotional states are reported in different sessions.
- **Source Persona:** P_hybrid_H5 – Mental Health Symptom-Aware User
- **Traceability:** Derived from review group H5
- **Acceptance Criteria:** Given a user completes a check-in and the system identifies a dominant emotion (e.g., anxious, sad, overwhelmed), when the results screen is displayed, then at least one named coping exercise (e.g., "4-7-8 breathing," "cognitive reframing") must be shown. Given a user reports anxiety in one session and sadness in another, when the results are compared, then the exercise recommendations for each session must differ.
- **Notes:** Rewritten from FR_auto_15 to add the requirement that recommendations are named (not just generically described) and that they must differ for different emotional states. The testability of the original was insufficient.

