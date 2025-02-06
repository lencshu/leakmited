# tests/test_models.py
import pytest
from sqlalchemy import text

from src.models import PlanetOSMLine


@pytest.mark.sls
def test_query_model(db_session):
    """
    query planet_osm_line
    """

    road = db_session.query(PlanetOSMLine).filter_by(osm_id=77667389).first()
    print("77667389: ", road)
    assert road is not None
    assert road.highway == "motorway_link"
    # test HSTORE
    assert road.tags is not None
    assert road.tags.get("maxspeed") == "40"
    # test geometry
    assert road.way is not None
