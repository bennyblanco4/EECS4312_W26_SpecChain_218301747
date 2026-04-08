# MindDoc Manual Specification
**App:** MindDoc: Mental Health Support  
**Pipeline:** Manual  
**Derived from:** personas/personas_manual.json  

---

## Requirement ID: FR1

- **Description:** The system shall display a clear and complete list of free versus premium features to the user before account creation and before any onboarding questions are presented.
- **Source Persona:** P1 – Budget-Conscious Mental Health Seeker
- **Traceability:** Derived from review group G1 (Subscription and paywall frustration)
- **Acceptance Criteria:** Given a new user launches the app for the first time, when the onboarding screen is shown, then a summary of free and paid features must be visible before the user is asked any personal questions or prompted to create an account.

---

## Requirement ID: FR2

- **Description:** The system shall allow users to complete the full 14-day initial assessment and receive a basic summary report without requiring a paid subscription.
- **Source Persona:** P1 – Budget-Conscious Mental Health Seeker
- **Traceability:** Derived from review group G1 (Subscription and paywall frustration)
- **Acceptance Criteria:** Given a user has completed 14 days of check-in responses, when they request their assessment results, then the system must display at minimum a basic summary of mood trends and a general recommendation, without redirecting to a subscription purchase screen.

---

## Requirement ID: FR3

- **Description:** The system shall allow users to log their mood and emotional state at least three times per day using a structured questionnaire that takes no more than two minutes to complete.
- **Source Persona:** P2 – Daily Mood Tracker
- **Traceability:** Derived from review group G2 (Daily mood check-in and emotional self-tracking)
- **Acceptance Criteria:** Given a user opens the check-in screen, when they respond to the questionnaire, then the session must complete in under two minutes and the response must be recorded to the user's mood history immediately upon submission.

---

## Requirement ID: FR4

- **Description:** The system shall display a mood history dashboard showing the user's emotional trends over the past 7, 30, and 90 days.
- **Source Persona:** P2 – Daily Mood Tracker
- **Traceability:** Derived from review group G2 (Daily mood check-in and emotional self-tracking)
- **Acceptance Criteria:** Given the user navigates to the mood history section, when they select a time range (7 days, 30 days, or 90 days), then the system must display a chart or graph representing the user's aggregated mood scores for the selected period, using data from stored check-in responses.

---

## Requirement ID: FR5

- **Description:** The system shall deliver push notification reminders at user-defined times, with the ability to configure up to three reminders per day with individual time settings.
- **Source Persona:** P3 – Habit-Building Reminder Dependent
- **Traceability:** Derived from review group G3 (Notification and reminder reliability)
- **Acceptance Criteria:** Given a user enables reminders in the app settings, when they specify up to three daily reminder times, then the system must deliver a push notification at each specified time within a five-minute tolerance. Notifications must arrive on the day they are scheduled unless the user has disabled them.

---

## Requirement ID: FR6

- **Description:** The system shall maintain notification delivery reliability across all supported Android versions, including devices with aggressive battery optimization, by requesting appropriate notification permissions and providing guidance to users on battery settings.
- **Source Persona:** P3 – Habit-Building Reminder Dependent
- **Traceability:** Derived from review group G3 (Notification and reminder reliability)
- **Acceptance Criteria:** Given a user has configured at least one reminder, when the scheduled time arrives, then the notification must be delivered even if the app has been closed for more than one hour, unless the device's battery optimization has explicitly blocked the app. The system must display a one-time setup prompt guiding users to exclude the app from battery optimization.

---

## Requirement ID: FR7

- **Description:** The system shall provide a guest or anonymous mode that allows users to complete check-ins and access basic features without creating an account or providing any personally identifiable information.
- **Source Persona:** P4 – Privacy-Aware Mental Health User
- **Traceability:** Derived from review group G4 (Data privacy and account security concerns)
- **Acceptance Criteria:** Given a user launches the app for the first time, when they select the anonymous/guest mode option, then the system must allow them to access daily check-ins and basic mood tracking without requiring an email address, name, or account registration. Data in guest mode must be stored locally on the device only.

---

## Requirement ID: FR8

- **Description:** The system shall provide an in-app security lock using PIN or biometric authentication that the user can enable to prevent unauthorized access to their mood and journal data.
- **Source Persona:** P4 – Privacy-Aware Mental Health User
- **Traceability:** Derived from review group G4 (Data privacy and account security concerns)
- **Acceptance Criteria:** Given the user has enabled the app lock feature in settings, when the app is launched or resumed from background after more than one minute of inactivity, then the system must require the user to authenticate using their configured PIN or biometric method before displaying any personal data. The lock must remain active even after the app is forcibly closed and reopened.

---

## Requirement ID: FR9

- **Description:** The system shall present at least five distinct therapeutic exercise modules (e.g., mindfulness, cognitive restructuring, breathing exercises) accessible within the free tier of the application.
- **Source Persona:** P5 – Structured Mental Health Learner
- **Traceability:** Derived from review group G5 (Therapeutic exercises and mental health education)
- **Acceptance Criteria:** Given a user is in the free tier, when they navigate to the exercises or programs section, then at least five complete, interactive therapeutic modules must be available and fully functional without a subscription prompt. Each module must include a description, step-by-step instructions, and a completion confirmation.

---

## Requirement ID: FR10

- **Description:** The system shall display an educational information card linked to each type of mood or emotional pattern detected in the user's check-in data, explaining the possible psychological relevance of the pattern.
- **Source Persona:** P5 – Structured Mental Health Learner
- **Traceability:** Derived from review group G5 (Therapeutic exercises and mental health education)
- **Acceptance Criteria:** Given the system has detected a recurring mood pattern (e.g., consistently low energy in the mornings for seven consecutive days), when the user views their mood summary, then at least one educational information card relevant to that pattern must be displayed. The card must include a plain-language explanation and reference a recognized psychological framework (e.g., CBT, mindfulness-based approaches).

---

## Requirement ID: FR11

- **Description:** The system shall allow users to export a PDF summary of their mood tracking history and completed exercises, which can be shared with a healthcare provider.
- **Source Persona:** P2 – Daily Mood Tracker
- **Traceability:** Derived from review group G2 (Daily mood check-in and emotional self-tracking)
- **Acceptance Criteria:** Given a user requests an export from the mood history screen, when the export action is completed, then the system must generate a PDF document containing the user's mood trend chart, a table of check-in scores by date, and a list of completed exercises. The PDF must be shareable via the device's native share menu.

---

## Requirement ID: FR12

- **Description:** The system shall present users with a clear, plain-language privacy policy summary on first launch, explicitly stating what data is collected, whether any data is shared with third parties, and how the user can request data deletion.
- **Source Persona:** P4 – Privacy-Aware Mental Health User
- **Traceability:** Derived from review group G4 (Data privacy and account security concerns)
- **Acceptance Criteria:** Given a user opens the app for the first time, when the privacy consent screen is shown, then the system must display a summary (not just a link to the full policy) that lists: (1) the types of data collected, (2) whether data is shared with third parties and for what purpose, and (3) how the user can delete their data. The user must explicitly acknowledge this summary before proceeding.

