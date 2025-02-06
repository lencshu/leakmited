# tests/test_schemas.py
import pytest
from pydantic import ValidationError

from src.schemas import RoadBase, StatsBase


@pytest.mark.sls
def test_road_base_schema():
    road_data = {"osm_id": 123, "highway": "primary", "maxspeed": "80"}
    road = RoadBase(**road_data)
    assert road.osm_id == 123
    assert road.highway == "primary"
    assert road.maxspeed == "80"


@pytest.mark.sls
def test_road_base_missing_field():
    """
    when missing osm_id, Pydantic should raise ValidationError
    """
    with pytest.raises(ValidationError):
        RoadBase(highway="primary")


@pytest.mark.sls
def test_stats_base_schema():
    stats_data = {"total_length": 1234.5, "speed_distribution": {"50": 10, "90": 3}}
    stats = StatsBase(**stats_data)
    assert stats.total_length == 1234.5
    assert stats.speed_distribution["50"] == 10
