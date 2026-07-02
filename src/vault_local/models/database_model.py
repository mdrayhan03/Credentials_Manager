import sqlite3
import threading
import os
from abc import ABC, abstractmethod
from pathlib import Path
from contextlib import contextmanager

# =====================================================================
# 1. THE STRATEGY INTERFACE
# =====================================================================
class DatabaseStrategy(ABC):
    """
    Abstract base class defining the contract for all database drivers.
    Any future online DB (Postgres, MySQL) must implement these methods.
    """
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    @contextmanager
    def transaction(self):
        pass

    @abstractmethod
    def close(self) -> None:
        pass


# =====================================================================
# 2. CONCRETE STRATEGY: SQLITE
# =====================================================================
class SQLiteStrategy(DatabaseStrategy):
    """Concrete execution handler for your current local-first SQLite persistence."""
    def __init__(self, db_name: str = "vault.db"):
        self.db_path = Path(os.environ.get("USERPROFILE", os.path.expanduser("~"))) / ".vaultlocal" / db_name
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None

    def connect(self) -> None:
        if not self.connection:
            self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.connection.execute("PRAGMA foreign_keys = ON;")
            self.connection.execute("PRAGMA journal_mode = WAL;")
            self._create_tables()

    def _create_tables(self) -> None:
        schema = """
        BEGIN TRANSACTION;
        CREATE TABLE IF NOT EXISTS vault_metadata (
            id INTEGER PRIMARY KEY CHECK (id = 1), salt BLOB NOT NULL, verification_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS vault_credentials (
            id TEXT PRIMARY KEY, title TEXT NOT NULL, cred_type TEXT NOT NULL, nonce BLOB NOT NULL, encrypted_payload BLOB NOT NULL, updated_at INTEGER NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_cred_title ON vault_credentials(title);
        CREATE TABLE IF NOT EXISTS vault_settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS vault_activities (id INTEGER PRIMARY KEY AUTOINCREMENT, last_activity_timestamp INTEGER NOT NULL);
        COMMIT;
        """
        self.connection.executescript(schema)

    @contextmanager
    def transaction(self):
        if not self.connection:
            raise sqlite3.OperationalError("SQLite connection is closed.")
        cursor = self.connection.cursor()
        try:
            yield cursor
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cursor.close()

    def close(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None


# =====================================================================
# 3. FUTURE CONCRETE STRATEGY: POSTGRESQL (Template Blueprint)
# =====================================================================
class PostgresStrategy(DatabaseStrategy):
    """Where you will seamlessly drop your future online cloud engine logic."""
    def __init__(self, connection_string: str):
        self.conn_string = connection_string
        self.connection = None

    def connect(self) -> None:
        # In the future, you will run: pip install psycopg2-binary
        # import psycopg2
        # self.connection = psycopg2.connect(self.conn_string)
        print(f"[FUTURE INFO] Connected to online PostgreSQL cluster via string: {self.conn_string}")
        pass

    @contextmanager
    def transaction(self):
        # Implement Postgres-specific cursor transaction blocks
        print("[FUTURE INFO] Yielding Postgres transaction cursor handle...")
        yield None 

    def close(self) -> None:
        if self.connection:
            self.connection.close()


# =====================================================================
# 4. THE FACTORY & SINGLETON CONTAINER
# =====================================================================
class DatabaseManager:
    """
    Thread-safe Singleton container handling the Strategy Factory instantiation.
    Ensures that the entire monolithic app acts on a unified database strategy wrapper.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.db: DatabaseStrategy = self._factory_select_strategy()
        self.db.connect()
        self._initialized = True

    def _factory_select_strategy(self) -> DatabaseStrategy:
        """FACTORY FUNCTION: Chooses structural engine dependent on environment controls."""
        db_environment = os.environ.get("VAULT_ENV", "LOCAL")
        
        if db_environment == "PRODUCTION_CLOUD":
            # Ready for online transition instantly
            pg_url = os.environ.get("DATABASE_URL", "postgresql://user:pass@localhost:5432/vault")
            return PostgresStrategy(connection_string=pg_url)
        else:
            # Default state
            return SQLiteStrategy()