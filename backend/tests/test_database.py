# tests/test_database.py
import pytest
from sqlalchemy import text

from src.core.database import engine, SessionLocal


@pytest.mark.sls
def test_database_engine_connect():
    """
    test engine db connect
    """
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert list(result)[0][0] == 1


@pytest.mark.sls
def test_database_session():
    """
    test SessionLocal with simple SQL cmd
    """
    session = SessionLocal()
    try:
        res = session.execute(text("SELECT 2"))
        assert res.scalar() == 2
    finally:
        session.close()
