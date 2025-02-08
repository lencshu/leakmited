# app/routers/stats.py
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast
from geoalchemy2.types import Geography

from src.core.database import get_db
from src.models import PlanetOSMLine
from src.schemas import StatsBase

router = APIRouter()

# Global cache to store the results of stats queries
stats_cache = {}


@router.get("/")
async def root(request: Request):
    client_ip = request.client.host
    print(f"Received request for root endpoint from IP: {client_ip}")
    return {"message": "Hello from Lambda"}


@router.get("/stats", response_model=StatsBase)
def get_stats(db: Session = Depends(get_db)):
    """
    Return road statistics:
    - total_length: ST_Length(way)
    - speed_distribution: number of roads for each maxspeed value
    """
    # Check if the stats are already cached
    if "stats" in stats_cache:
        print("returning cached stats data")
        return stats_cache["stats"]

    # ST_Length(way) returns values in degrees when using SRID=4326
    # total_length_deg = db.query(func.sum(func.ST_Length(PlanetOSMLine.way))).scalar() or 0.0

    # query for total length of all roads in meters
    total_length_meter = db.query(func.sum(func.ST_Length(cast(PlanetOSMLine.way, Geography)))).scalar() or 0.0

    rows = (
        db.query(PlanetOSMLine.tags["maxspeed"].label("maxspeed"), func.count(PlanetOSMLine.osm_id))
        .filter(PlanetOSMLine.tags.has_key("maxspeed"))
        .group_by(PlanetOSMLine.tags["maxspeed"])
        .all()
    )

    dist_dict = {}
    for ms, cnt in rows:
        if ms in ["30", "50", "70", "90", "110", "130"]:
            label = ms
            dist_dict[label] = cnt

    # cache to reuse for the next time
    stats_data = StatsBase(total_length=total_length_meter, speed_distribution=dist_dict)
    stats_cache["stats"] = stats_data

    return stats_data
