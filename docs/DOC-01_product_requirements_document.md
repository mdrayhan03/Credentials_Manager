# Product Requirements Document (PRD)
## Project: VaultLocal (Credentials Manager)

### 1. Executive Summary
VaultLocal is a lightweight, zero-knowledge, local-first credentials manager built with Python and Flet. It aims to solve "credential sprawl" by offering an intuitive interface to manage diverse account secrets securely on-device without forced cloud lock-in.

### 2. User Journey Flow: First-Time Onboarding
1. **Launch:** App starts up; detects no local database initialization metadata.
2. **Setup Screen:** Prompted to create a Master Password with a dynamic complexity visual check.
3. **Key Generation:** System generates a 16-byte random salt, displays a sequence of emergency recovery keys, and initializes the local encrypted SQLite schema.
4. **Dashboard Redirection:** Instantly maps the user to the empty 3-column default vault dashboard.

### 3. Feature Prioritization Matrix

| Feature | Target | Description | Scope |
| :--- | :--- | :--- | :--- |
| **Master Auth Engine** | Core | Argon2id key derivation setup with automated memory zeroing. | MVP |
| **Dynamic Form Templates** | UI | Forms morph inputs based on chosen type (Web login, SSH, API Key). | MVP |
| **3-Column Layout** | Desktop | Collapsible panels: Left (Nav), Center (List), Right (Details). | MVP |
| **Volatile Clipboard** | Sec | Copies field items to OS clipboard, forcefully wiping memory cache after 30s. | MVP |
| **Activity Idle Session Hook** | Sec | Tracks GUI interactions; automatically destroys key variables on timeout. | MVP |
| **Manual Drive Push/Pull** | Sync | Backup data exchange using a targeted user-authorized Google Drive folder. | Phase 2 |

### 4. Non-Functional Constraints
* **Disk Footprint:** Bundled compilation package must remain below 80MB.
* **Memory Limits:** Idle app runtime execution RAM footprint cannot cross 120MB on desktop systems.