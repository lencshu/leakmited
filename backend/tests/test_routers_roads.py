# tests/test_routers_roads.py
import pytest

from src.core.config import ROADS_NUM_LIMIT


@pytest.mark.sls
def test_get_roads_no_filters(client):

    resp = client.get("/roads/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) <= ROADS_NUM_LIMIT


@pytest.mark.sls
def test_get_roads_filter_maxspeed(client):

    resp = client.get("/roads/?max_speed=50")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) <= ROADS_NUM_LIMIT


@pytest.mark.sls
def test_get_road_by_id(client):
    resp = client.get("/roads/188447554")
    assert resp.status_code == 200
    # data = resp.json()
    # assert data["properties"]["osm_id"] == 188447554
    # assert data["properties"]["maxspeed"] == 80


@pytest.mark.sls
def test_get_road_not_found(client):
    resp = client.get("/roads/7777")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Road not found"
