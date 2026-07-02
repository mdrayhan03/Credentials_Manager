import pytest
import threading
import os
from unittest.mock import MagicMock
from models.database_model import DatabaseManager, SQLiteStrategy, PostgresStrategy

# =====================================================================
# 1. FIXTURES (Setup and Teardown)
# =====================================================================
@pytest.fixture(autouse=True)
def reset_database_manager():
    """Resets the DatabaseManager Singleton instance between individual tests."""
    DatabaseManager._instance = None
    yield
    DatabaseManager._instance = None


# =====================================================================
# 2. SINGLETON TEST SUITE
# =====================================================================
def test_database_manager_singleton_identity():
    """Verifies that sequential instantiations yield the exact same memory instance."""
    manager_one = DatabaseManager()
    manager_two = DatabaseManager()
    
    assert manager_one is manager_two, "DatabaseManager failed to preserve Singleton identity."


def test_database_manager_thread_safety():
    """Simulates rapid multi-threaded access to ensure the Singleton is thread-safe."""
    instances = []
    lock = threading.Lock()

    def worker():
        manager = DatabaseManager()
        with lock:
            instances.append(manager)

    # Spawn 10 concurrent threads attempting to instantiate the manager
    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Verify every thread received the absolute same object memory reference
    first_instance = instances[0]
    for instance in instances:
        assert instance is first_instance, "Thread collision detected: Multiple singletons initialized."


# =====================================================================
# 3. FACTORY STRATEGY SELECTION TEST SUITE
# =====================================================================
def test_factory_selects_sqlite_by_default(monkeypatch):
    """Ensures that the factory defaults to SQLite strategy when no env is provided."""
    monkeypatch.delenv("VAULT_ENV", raising=False)
    
    manager = DatabaseManager()
    assert isinstance(manager.db, SQLiteStrategy), "Factory failed to default to SQLiteStrategy."


def test_factory_selects_postgres_in_production(monkeypatch):
    """Ensures that the factory switches to PostgresStrategy under cloud configs."""
    monkeypatch.setenv("VAULT_ENV", "PRODUCTION_CLOUD")
    monkeypatch.setenv("DATABASE_URL", "postgresql://test_user:pass@localhost:5432/test_db")
    
    manager = DatabaseManager()
    assert isinstance(manager.db, PostgresStrategy), "Factory failed to switch to PostgresStrategy."


# =====================================================================
# 4. ROBUST TRANSACTION EXCEPTION REGRESSION TEST
# =====================================================================
def test_sqlite_transaction_rollback_on_failure(tmp_path):
    """Verifies that an unhandled query exception safely triggers an atomic rollback."""
    # Use Pytest's isolated temp directory layout to avoid littering the user profile
    test_db_file = tmp_path / "test_vault.db"
    strategy = SQLiteStrategy(db_name=str(test_db_file))
    strategy.connect()

    # Seed data to test rollback thresholds
    with strategy.transaction() as cursor:
        cursor.execute("INSERT INTO vault_settings (key, value) VALUES ('theme', 'dark');")

    # Intentional crash injection: Attempt to execute broken SQL syntax midway
    with pytest.raises(Exception):
        with strategy.transaction() as cursor:
            cursor.execute("UPDATE vault_settings SET value = 'light' WHERE key = 'theme';")
            cursor.execute("INSERT INTO force_a_crash_by_calling_non_existent_table VALUES (1);")

    # Verify rollback: The value should remain 'dark', NOT 'light'
    with strategy.transaction() as cursor:
        cursor.execute("SELECT value FROM vault_settings WHERE key = 'theme';")
        result = cursor.fetchone()[0]
        
    assert result == "dark", "Transaction committed partial data instead of executing a complete rollback."
    strategy.close()