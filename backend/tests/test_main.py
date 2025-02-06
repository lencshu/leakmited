# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.mark.sls
def test_main_info():
    """
    test FastAPI meta info
    """
    assert app.title == "Leakmited Road Network API"
    assert app.version == "1.0.0"


@pytest.mark.sls
def test_main_docs():
    """
    test if /docs or /openapi.json accessible
    """
    client = TestClient(app)
    resp = client.get("/docs")
    assert resp.status_code == 200
