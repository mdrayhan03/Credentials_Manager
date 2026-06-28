# Software Architecture Document (SAD / TDD)
## Project: VaultLocal (Credentials Manager)

### 1. High-Level Engineering Paradigm
The application uses a clean decoupling layer between the UI View state managed by Flet (compiled through Flutter's graphics engine) and a background system loop run inside Python. All platform operations leverage standard inter-process command execution pipes inside Tauri/Flet hooks.

### 2. Cryptographic Specification
* **Key Derivation Function (KDF):** Argon2id (`pyca/cryptography`)
    *   **Memory Cost ($m$):** 65,536 KB (64 MB)
    *   **Time Cost ($t$):** 3 iterations
    *   **Parallelism ($p$):** 4 threads
    *   **Salt:** 16-byte secure random value generated via `os.urandom()`, kept plain-text inside the `vault_metadata` block.
* **Payload Encryption Engine:** AES-256-GCM
    *   **Key Length:** 256 bits (32 bytes derived via KDF).
    *   **Nonce Allocation:** Unique 12-byte initialization vector (`os.urandom(12)`) per individual payload block entry.

### 3. Memory Management Strategy
Because standard Python string instances (`str`) are immutable and tracked dynamically by a generational garbage collector, raw credentials can linger inside memory cells long after variables go out of scope. 
* **Mitigation Protocol:** All password fields and intermediate key arrays must handle sensitive characters exclusively via mutable bytearrays (`bytearray`).
* **Purge Function:** Before dropping references, memory fields must overwrite raw bytes with an explicit inline null pass:
```python
def clear_secret(secret_target: bytearray):
    for i in range(len(secret_target)):
        secret_target[i] = 0
```