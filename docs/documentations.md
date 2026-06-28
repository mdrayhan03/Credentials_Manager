1. Product Requirements Document (PRD)
Written By: You (as the Product Owner / Founder).
Purpose: Defines WHAT you are building and WHY. It focuses entirely on features, user experience, constraints, and business goals.
Key Sections for your app: Feature prioritization matrix (MVP vs. Phase 2), user journey flows (e.g., “First-time onboarding to Master Password creation”), and app footprint constraints (RAM/disk size).
2. Software Architecture Document (SAD) / Technical Design Document (TDD)
Written By: You (as the Senior Engineer).
Purpose: Defines HOW you are going to build it. It translates the PRD features into actual code structures, library selections, and data formats.
Key Sections for your app:
* Data Models & Database Schema: Explicit definition of the SQLite tables, keys, and column types.
* Cryptographic Specification: Exact details on the security primitives. For example: “Argon2id configuration params: $m=65536$, $t=3$, $p=4$, using a random 16-byte salt saved in cleartext header.
* ”Memory Management Strategy: Explicit details on how Python memory handles strings containing raw passwords to prevent RAM sniffing leaks.
3. Database Schema & Data Dictionary
Written By: You (as the Database Designer).
Purpose: A sub-document of the TDD that serves as the single source of truth for your local storage layout.
Key Sections for your app: Detailed column breakdowns showing which fields are saved as plain text (like the item title or favicon URL) vs. which fields are saved as encrypted binary BLOBs (usernames, passwords, security notes).
4. Test Plan & Threat Model Matrix
Written By: You (as the QA and Security Engineer).
Purpose: Ensures the app behaves correctly and remains absolutely secure against potential local attack vectors.
Key Sections for your app:
* Functional Test Cases: Check lists for UI reactions (e.g., “Verify clipboard clears exactly 30 seconds after copying.”).
* Threat Modeling: Documenting local vectors like: “What happens if an attacker steals the .db file from the user’s AppData folder?” or “What happens if the app crashes while writing a new credential to disk?” (ensuring ACID compliance prevents file corruption).