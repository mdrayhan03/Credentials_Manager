# Test Plan & Threat Model Matrix
## Project: VaultLocal (Credentials Manager)

### 1. Functional QA Test Suite

| Test Case ID | Scope | Verification Target | Expected Behavior |
| :--- | :--- | :--- | :--- |
| **TC-01** | Clipboard | Automatic buffer cleansing. | Copied payload removes smoothly from desktop clipboard memory after 30 seconds. |
| **TC-02** | Idle State | App lock state on user abandonment. | Lack of UI cursor interaction for 5 minutes terminates active memory keys and resets to login view. |
| **TC-03** | Fluid Forms| Dynamic UI item switching. | Changing type from "Login" to "SSH" changes inputs cleanly without graphic rendering lag. |

### 2. Threat Modeling Matrix (Local Attack Vectors)

| Threat Profile | Risk Level | Target Vector | Architectural Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Database Exfiltration** | **High** | Attacker clones `vault.db` directly off machine disk layers. | Mitigated by **Zero-Knowledge Architecture**. Payloads require the Master Password to compute the cryptographic key; raw data is entirely unreadable without it. |
| **Data Corruption Interruption**| **Medium**| OS process crashes out mid-write transaction. | Mitigated by **SQLite ACID Properties**. Database engine rolls back incomplete queries atomically to prevent corruption. |
| **RAM Scrape Attack** | **Medium**| Memory scanner dumps application processes while unlocked. | Mitigated by **Mutable Bytearrays**. High-value credentials zero out memory registers immediately after use. |