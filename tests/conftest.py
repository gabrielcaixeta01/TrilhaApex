import os
import sys
import pathlib
from fastapi.testclient import TestClient
import pytest

# Ensure project root is importable so `import app` works under pytest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Use a separate SQLite DB for tests
DB_PATH = ROOT / "test_petstore.db"
os.environ["DATABASE_URL"] = f"sqlite:///{DB_PATH}"

# remove leftover DB from previous runs
if DB_PATH.exists():
    try:
        DB_PATH.unlink()
    except Exception:
        pass

from app.main import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
    # teardown DB file
    if DB_PATH.exists():
        try:
            DB_PATH.unlink()
        except Exception:
            pass
