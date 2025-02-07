# tests/test_routers_stats.py
import pytest


@pytest.mark.sls
def test_stats_basic(client):
    resp = client.get("/stats/")
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_length"] is not None

    dist = data["speed_distribution"]
    assert "50" in dist
    assert "90" in dist
