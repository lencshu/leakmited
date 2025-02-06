# tests/test_routers_roads.py
import pytest


@pytest.mark.sls
def test_get_roads_no_filters(client):

    resp = client.get("/roads/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    osm_ids = {item["osm_id"] for item in data}
    assert osm_ids == {101, 102}


@pytest.mark.sls
def test_get_roads_filter_maxspeed(client):

    resp = client.get("/roads/?max_speed=50")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["osm_id"] == 201


@pytest.mark.sls
def test_get_road_by_id(client):
    resp = client.get("/roads/999")
    assert resp.status_code == 200
    data = resp.json()
    assert data["osm_id"] == 999
    assert data["maxspeed"] == "40"


@pytest.mark.sls
def test_get_road_not_found(client):
    resp = client.get("/roads/7777")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Road not found"
