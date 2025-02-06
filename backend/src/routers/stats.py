# app/routers/stats.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast
from geoalchemy2.types import Geography

from src.core.database import get_db
from src.models import PlanetOSMLine
from src.schemas import StatsBase

router = APIRouter()


@router.get("/", response_model=StatsBase)
def get_stats(db: Session = Depends(get_db)):
    """
    Return road statistics:
    - total_length: ST_Length(way)
    - speed_distribution: number of roads for each maxspeed value
    """

    # ST_Length(way) returns values in degrees when using SRID=4326
    # total_length_deg = db.query(func.sum(func.ST_Length(PlanetOSMLine.way))).scalar() or 0.0

    # in meter
    # total_length_meter = db.query(func.sum(func.ST_Length(PlanetOSMLine.way.op("::geography")))).scalar() or 0.0
    total_length_meter = db.query(func.sum(func.ST_Length(cast(PlanetOSMLine.way, Geography)))).scalar() or 0.0

    # number of roads for each maxspeed value
    rows = (
        db.query(PlanetOSMLine.tags["maxspeed"].label("maxspeed"), func.count(PlanetOSMLine.osm_id))
        .filter(PlanetOSMLine.tags.has_key("maxspeed"))
        .group_by(PlanetOSMLine.tags["maxspeed"])
        .all()
    )

    dist_dict = {}
    for ms, cnt in rows:
        label = ms if ms else "Unknown"
        dist_dict[label] = cnt

    return StatsBase(total_length=total_length_meter, speed_distribution=dist_dict)
