# src/routers/roads.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, cast
from typing import Optional, List

from geoalchemy2 import Geography
from geoalchemy2.shape import to_shape

from src.core.database import get_db
from src.models import PlanetOSMLine
from src.schemas import RoadGeoJSON

router = APIRouter()


def road_to_geojson(road: PlanetOSMLine) -> dict:
    """
    convert to GeoJSON:
    {
      "geometry": {
          "type": "LineString",
          "coordinates": [ [lon, lat], [lon, lat], ... ]
      },
      "properties": {
          "maxspeed": 50,
          "highway": "residential",
          "osm_id": 165436231
      }
    }
    """
    if road.way is None:
        coordinates = []
    else:
        # convert PostGIS to Shapely obj
        shape = to_shape(road.way)
        # convert Shapely to [[lon, lat], [lon, lat], ...]
        coordinates = [list(coord) for coord in shape.coords]

    geometry = {"type": "LineString", "coordinates": coordinates}

    try:
        maxspeed_val = int(road.maxspeed) if road.maxspeed is not None else None
    except ValueError:
        maxspeed_val = None

    properties = {
        "maxspeed": maxspeed_val,
        "highway": road.highway,
        "osm_id": road.osm_id,
    }
    return {"geometry": geometry, "properties": properties}


@router.get("/roads", response_model=List[RoadGeoJSON])
def get_roads(db: Session = Depends(get_db), max_speed: Optional[str] = Query(None, description="Filter roads by maximum speed, such as 50, 90, etc.")):
    """
    Retrieve a list of roads with maxspeed information, optionally filtering by max_speed.
    """
    query = db.query(PlanetOSMLine)
    # Return only roads that have maxspeed.
    query = query.filter(PlanetOSMLine.tags.has_key("maxspeed"))
    if max_speed:
        query = query.filter(PlanetOSMLine.tags["maxspeed"] == max_speed)
    # Limit to 500 entries to avoid excessive data size.
    roads = query.limit(500).all()
    return [road_to_geojson(road) for road in roads]


@router.get("/roads/{osm_id}", response_model=RoadGeoJSON)
def get_road_by_id(osm_id: int, db: Session = Depends(get_db)):
    """
    Retrieve detailed information about a specific road by osm_id.
    """
    road = db.query(PlanetOSMLine).filter(PlanetOSMLine.osm_id == osm_id).first()
    if not road:
        raise HTTPException(status_code=404, detail="Road not found")
    return road_to_geojson(road)


@router.get("/roads-statistics")
def get_roads_statistics(db: Session = Depends(get_db)):
    """
    Return the total length statistics (km) of road with limits of 30km/h, 50km/h, 70km/h and 90km/h
    demo response:
    [
       { "maxspeed": 30, "km": 10000 },
       { "maxspeed": 50, "km": 20000 },
       { "maxspeed": 70, "km": 30000 },
       { "maxspeed": 90, "km": 40000 },
    ]
    """
    results = (
        db.query(PlanetOSMLine.tags["maxspeed"].label("maxspeed"), (func.sum(func.ST_Length(cast(PlanetOSMLine.way, Geography))) / 1000.0).label("km"))
        .filter(PlanetOSMLine.tags.has_key("maxspeed"))
        .filter(PlanetOSMLine.tags["maxspeed"].in_(["30", "50", "70", "90"]))
        .group_by(PlanetOSMLine.tags["maxspeed"])
        .all()
    )
    stats = []
    for row in results:
        try:
            ms = int(row.maxspeed)
        except (ValueError, TypeError):
            ms = None
        stats.append({"maxspeed": ms, "km": float(row.km)})
    return stats
