# File: tests/conftest.py
import os
import pytest
import importlib

@pytest.fixture(autouse=True)
def test_env_and_db(tmp_path):
    """
    Autouse fixture untuk setiap test:
    1) Set env var DATABASE_URL ke in-memory SQLite
    2) Set REDIS_URL dan DEEPSEEK_API_KEY dummy
    3) Reload module app.database agar engine & SessionLocal dibangun ulang
       menggunakan DATABASE_URL yang baru
    4) Create & drop semua tabel di SQLite in-memory
    """
    # 1) Set environment variables
    os.environ["DATABASE_URL"]     = "sqlite:///:memory:"
    os.environ["REDIS_URL"]        = "redis://dummy:6379"
    os.environ["DEEPSEEK_API_KEY"] = "testkey"

    # 2) Reload module database supaya engine dibangun ulang
    #    (pastikan tidak ada import engine sebelum ini)
    import app.database as db_mod
    importlib.reload(db_mod)

    # 3) Buat semua tabel di SQLite in-memory
    db_mod.Base.metadata.create_all(bind=db_mod.engine)

    yield

    # 4) Drop semua tabel setelah test
    db_mod.Base.metadata.drop_all(bind=db_mod.engine)