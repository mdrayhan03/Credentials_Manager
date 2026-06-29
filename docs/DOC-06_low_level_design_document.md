# Low-Level Design (LLD) Document
## Project: VaultLocal (Credentials Manager)
## Design Patterns: Monolithic MVVM, Singleton, Repository Pattern

---

### 1. Comprehensive System Map (Class Distribution)
```
[ UI Views: Singletons ]             [ ViewModels: Singletons ]        [ Repositories / Data Layer ]
+----------------------+             +------------------------+        +--------------------------+
| login / signin       | ----------> | auth_viewmodel         | -----> | user_repo                |
+----------------------+             +------------------------+        +--------------------------+
|
+----------------------+             +------------------------+        +----------+---------------+
| dashboard            |             | vault_viewmodel        | ---->  | credentials_repo         |
|  ├── leftboard       | ----------> |                        |        | activity_repo            |
|  ├── rightboard      |             +------------------------+        +--------------------------+
|  └── mainboard       |                                                          |
|       ├── home       |             +------------------------+        +----------+---------------+
|       ├── credentials| ----------> | settings_viewmodel     | ---->  | settings_repo            |
|       └── settings   |             +------------------------+        +--------------------------+
+----------------------+
```
---

### 2. Micro Class Specifications

#### 📂 Models & Storage Layer

##### `database_model.py`
*   **`DatabaseConn` (Singleton)**: Tracks the low-level SQLite3 filesystem connection handle. Implements a thread-safe `__new__` initializer.
*   **`UserRepo`**: Handles user profile registration hashes and matching operations.
*   **`CredentialsRepo`**: Handles `AES-256-GCM` query injections. Encrypts payload maps into binary BLOB structures before passing them to the DB driver.
*   **`SettingsRepo`**: Manages key/value UI preferences rows.
*   **`ActivityRepo`**: Updates and samples tracking logs used to run the background inactivity log out thread.

##### `credentials_model.py`
*   **`CredentialsDBClass` (Data Class)**: Maps explicit attributes (`id`, `title`, `cred_type`, `encrypted_payload`, `nonce`, `updated_at`).
*   **`UserClass` (Data Class)**: Holds active session parameters (`user_id`, `derived_key_buffer`).

##### `settings_model.py`
*   **`SettingsDBClass` (Data Class)**: Holds application configuration parameters (`theme_mode`, `idle_timeout_seconds`).

---

#### 📂 ViewModel Layer (State Engines)

##### `auth_viewmodel.py` (Singleton)
*   **State properties**: `is_authenticated: bool`, `auth_error_msg: str`.
*   **Methods**:
    *   `login_user(master_password: str) -> bool`: Executes Argon2id routine against `UserRepo` hash.
    *   `register_user(master_password: str)`: Creates database file structure and writes cryptographic constants.
    *   `start_idle_monitor()`: Fires a background tracking thread verifying active timestamps against `ActivityRepo`.

##### `vault_viewmodel.py` (Singleton)
*   **State properties**: `credentials_list: list`, `selected_credential: CredentialsDBClass`, `search_query: str`.
*   **Methods**:
    *   `search_vault(query: str)`: Performs in-memory list object filtering.
    *   `add_credential(title: str, c_type: str, raw_payload: dict)`: Invokes encryption pipelines and commits to `CredentialsRepo`.

##### `settings_viewmodel.py` (Singleton)
*   **State properties**: `current_theme: str`, `lock_delay: int`.
*   **Methods**:
    *   `update_theme(mode: str)`: Shifts theme configurations and updates the UI state.

---

#### 📂 View Layer (Flet Graphic Interface Components)

All View classes wrap Flet UI layout definitions inside a thread-safe Singleton model structure.

*   **`login_view.py` -> `Login` (Singleton)**: Renders the entry interface. Binds actions directly to `AuthViewModel`.
*   **`signin_view.py` -> `Signin` (Singleton)**: Handles setup workflows.
*   **`dashboard_view.py` -> `Dashboard` (Singleton)**: Top-level scaffolding frame. Holds sub-containers in a clean system matrix:
    *   `menuboard_view.py` -> Mobile slide-out toggle menu container.
    *   `leftboard_view.py` -> Static desktop category configuration menu sidebar.
    *   `rightboard_view.py` -> Details inspect slide-out drawer (displays field copy strings).
    *   `mainboard_view.py` -> Central UI layout controller panel. Automatically updates to paint child views based on the selected route:
        *   `home_main.py` -> `Home` dashboard layout views.
        *   `credentials_main.py` -> `Credentials` lists.
        *   `settings_main.py` -> `Settings` configuration layouts.

---

### 3. Implementation Blueprint Strategy for Python Singletons

To ensure singletons behave predictably across your entire app, utilize Python's structural `__new__` magic method override pattern across your system layout:

```python
class VaultViewModel:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VaultViewModel, cls).__new__(cls)
            # Initialize core structural state parameters once here
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, credentials_repo=None):
        if self._initialized:
            return
        self.repo = credentials_repo
        self.credentials_list = []
        self._initialized = True

