# tests/conftest.py

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from src.main import app
from src.core.database import get_db, metadata

load_dotenv(".env.dev")

TEST_DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}" f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def db_setup():
    metadata.create_all(bind=test_engine)
    yield
    metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """
    new session for each test function
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        # transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    test_client = TestClient(app)

    yield test_client

    app.dependency_overrides.clear()
