# High-Level Design Document (HLD)
## Project: VaultLocal (Credentials Manager)
## Architecture Style: Monolithic MVVM (Model-View-ViewModel)

---

### 1. Architectural System Overview

VaultLocal uses a **Monolithic MVVM Architecture**. The UI layer (Views) reads reactive state directly from the Business Logic layer (ViewModels), which processes backend persistence, caching, and cryptographic transitions via the Data Layer (Models).
```
+------------------------------------------------------------------------------------------------+
|                                           VIEWS LAYER                                          |
|  +------------+   +-------------+   +-------------------------------------------------------+  |
|  | login_view |   | signin_view |   |                    dashboard_view                     |  |
|  +------------+   +-------------+   | +-----------+ +--------------------+ +--------------+ |  |
|                                     | | leftboard | |     mainboard      | |  rightboard  | |  |
|                                     | +-----------+ | (home/creds/setts) | +--------------+ |  |
|                                     |               +--------------------+                  |  |
|                                     +-------------------------------------------------------+  |
+--------------------------------------------------+---------------------------------------------+
| Data Binding / Events
v
+------------------------------------------------------------------------------------------------+
|                                       VIEWMODELS LAYER                                         |
|         +-----------------------+    +-----------------------+    +-----------------------+    |
|         |     auth_viewmodel    |    |    vault_viewmodel    |    |   settings_viewmodel  |    |
|         +-----------------------+    +-----------------------+    +-----------------------+    |
+--------------------------------------------------+---------------------------------------------+
| Explicit Calls / In-Memory Payload Streams
v
+------------------------------------------------------------------------------------------------+
|                                          MODELS LAYER                                          |
|                 +------------------+  +------------------+  +------------------+               |
|                 | credential_model |  |  database_model  |  |  settings_model  |               |
|                 +------------------+  +------------------+  +------------------+               |
+--------------------------------------------------+---------------------------------------------+
| ACID Encrypted BLOB Storage (AES-256-GCM)
v
[ Local sqlite3 DB ]
```

---

### 2. File-by-File Blueprint & Operational Responsibilities

#### 📂 `models/` (Data Entities & Core Logic)
*   **`credential.py`**: Contains strict immutable data schemas mapping record types (`Login`, `SSH`, etc.). Restricts plaintext credentials from expanding unmanaged across the Python heap.
*   **`database.py`**: Manages filesystem operations via SQLite3. Houses the core **Argon2id** key derivation factory and performs **AES-256-GCM** encryption/decryption routines directly on JSON payloads prior to storage execution.
*   **`settings.py`**: Manages app state preferences (e.g., locking timeline configuration, theme indices, local backup file targets).

#### 📂 `viewmodels/` (Reactive Business Rules)
*   **`auth_viewmodel.py`**: Controls session state boundaries. Validates input tokens on setup, keeps derived vault keys inside secure byte arrays, and fires a countdown state for auto-lock rules.
*   **`vault_viewmodel.py`**: The dynamic state core of the runtime application. Filters lists as queries stream through views, structures additions depending on contextual template items, and operates the volatile clipboard clearing loops.
*   **`settings_viewmodel.py`**: Bridges UI preference adjustments instantly into file storage models.

#### 📂 `views/` (Flet Presentation Components)
*   **`login_view.py`**: Renders basic master passcode access prompts.
*   **`signin_view.py`**: Handles primary initialization screens, dynamic password requirements checks, and recovery token validation.
*   **`dashboard_view.py`**: Top-level UI orchestration structure using Flet's `ResponsiveRow`. Handles orientation checks (Desktop 3-column split vs Mobile stacked panel transitions).
*   **`menuboard.py`**: Desktop menubar. Provides left board and right board open close controls and Navigate path.
*   **`leftboard.py`**: Desktop navigation drawer. Provides rapid switching hooks for active layout tabs.
*   **`mainboard.py`**: Dynamic middle routing container that updates to render children components (`home_main`, `credentials_main`, or `settings_main`).
*   **`rightboard.py`**: Collapsible description window. Exposes password visibility modifiers, credential copy toggles, and item deletion parameters.
*   **`home_main.py`**: Initial dashboard panel showing recent additions, favorite credentials, and security health summaries.
*   **`credentials_main.py`**: Central list control hub showing live-filtered password items and record types.
*   **`settings_main.py`**: Basic configuration configuration interface (theme adjustments, clear cache, lock timings).

---

### 3. Component Interaction Flow (Sequence Trace)

The following example diagrams a real-time event when a user looks up an item, modifying view visibility without breaking security boundaries.
```
[views/dashboard]        [viewmodels/vault]        [models/database]        [sqlite3 DB]
|                         |                         |                     |
|--- 1. Type "Github" --->|                         |                     |
|    on_change event      |                         |                     |
|                         |--- 2. filter_search() ->|                     |
|                         |    (Scans memory pool)  |                     |
|                         |                         |                     |
|                         |    If data stale:       |                     |
|                         |---- 3. fetch_records  ->|                     |
|                         |                         |--- 4. Query BLOB -->|
|                         |                         |<-- 5. Return BLOB --|
|                         |<-- 6. Decrypt (AES) ----|                     |
|<-- 7. Update View State-|                         |                     |
|    & fire page.update() |                         |                     |
```

---

### 4. Technical Constraints & Design Rules

1.  **State Cleanliness**: No view files (`views/`) may query SQLite or execute cryptography directly. They are restricted to adjusting graphical components and triggering methods on their bounded ViewModels.
2.  **Explicit Zeroing**: Any ViewModel that releases references to sensitive user information must trigger standard byte-level nullification passes over structural strings to prevent leftover items in RAM.
3.  **UI Fluidity**: To keep the interface lightweight, real-time query scanning inside `vau