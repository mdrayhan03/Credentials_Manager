# Database Schema & Data Dictionary
## Project: VaultLocal (Credentials Manager)

VaultLocal leverages a standard local SQLite3 implementation file (`vault.db`). To preserve security visibility, structural indexes are left unencrypted, whereas data payloads are fully ciphered.

### 1. Table: `vault_metadata`
Stores application configuration data and target variables needed to authenticate database integrity.

| Column Name | Data Type | Key / Index | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY | Single row counter constraint (Value: 1). |
| `salt` | BLOB | None | 16-byte raw salt value used during Argon2id routines. |
| `verification_hash` | TEXT | None | Encrypted dummy payload block verified at runtime to validate correct master key entry. |

### 2. Table: `vault_credentials`
Stores actual credentials. Structural metadata remains plaintext for indexing speed; sensitive attributes reside inside a combined payload string.

| Column Name | Data Type | Key / Index | Storage State | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | TEXT | PRIMARY KEY | Plaintext UUID | Universally unique item identification reference. |
| `title` | TEXT | INDEX | Plaintext | User-defined tracking reference label. |
| `cred_type` | TEXT | None | Plaintext | Type discriminator (`login`, `ssh`, `card`). |
| `nonce` | BLOB | None | Plaintext | 12-byte initialization vector used for this entry. |
| `encrypted_payload` | BLOB | None | AES-256-GCM | Encrypted JSON string string parsing dynamic schema fields. |
| `updated_at` | INTEGER | None | Plaintext | Unix timestamp metric used to dictate future sync conflicts. |

#### Payload Schema Example (Decrypted JSON string format before database mapping)
*   **Type `login`:** `{"username": "johndoe", "email": "john@example.com", "password": "secret_password"}`
*   **Type `ssh`:** `{"username": "root", "ip": "192.168.1.50", "ssh_key": "-----BEGIN OPENSSH...", "password": ""}