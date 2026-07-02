1. Raw idea generation
2. Make detailed idea and documentations
3. PRD, SA, DSD, Test & Threat matrix documents
4. UI/UX design for desktop in powerpoint
5. High level design document
6. Low level design document
architecture model about done here

[Developer Mode]
1. git setup
2. venv setup
3. install flet, cryptograph and cert
4. make Directory Scaffolding

## todo
### Milestone 1: Core Storage & Database Layer (v0.1.0)
- Goal: Establish the persistence engine and repository layout.

- Issues to Create & Assign here:

    - Issue #1: Implement DatabaseConn Singleton class in database_model.py.

    - Issue #2: Design and execute local SQLite table initialization schemas (users, credentials, settings, activities).

    - Issue #3: Build the CRUD Repository layers (UserRepo, CredentialsRepo, SettingsRepo, ActivityRepo).

### Milestone 2: Cryptographic Infrastructure (v0.2.0)
- Goal: Implement zero-knowledge security primitives and memory isolation.

- Issues to Create & Assign here:

    - Issue #4: Build Argon2id key derivation module inside database_model.py.

    - Issue #5: Implement AES-256-GCM authenticated encryption/decryption routines for binary data payloads.

    - Issue #6: Implement explicit memory-zeroing helper function using mutable bytearray references.

### Milestone 3: ViewModel State Management (v0.3.0)
- Goal: Construct the reactive business logic engines without any UI dependencies.

- Issues to Create & Assign here:

    - Issue #7: Create AuthViewModel singleton state machine with an internal session countdown listener.

    - Issue #8: Create VaultViewModel singleton containing real-time in-memory list filtering logic.

    - Issue #9: Create background thread pool task to automatically wipe the operating system clipboard after 30 seconds.

### Milestone 4: Flet Responsive View Layer (v1.0.0-MVP)
- Goal: Assemble the final responsive graphical interface and bind it to the viewmodel layer.

- Issues to Create & Assign here:

    - Issue #10: Build Singleton UI views for Login and Signin onboarding layouts.

    - Issue #11: Implement top-level Dashboard shell container utilizing Flet's ResponsiveRow.

    - Issue #12: Build the nested view elements (Leftboard, Rightboard, and Mainboard tab-routers).

    - Issue #13: Package final application compilation assets into platform binaries via flet build.