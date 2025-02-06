# app/routers/roads.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from src.core.database import get_db
from src.models import PlanetOSMLine
from src.schemas import RoadBase

router = APIRouter()


@router.get("/roads", response_model=List[RoadBase])
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
    return roads


@router.get("/roads/{osm_id}", response_model=RoadBase)
def get_road_by_id(osm_id: int, db: Session = Depends(get_db)):
    """
    Retrieve detailed information about a specific road by osm_id.
    """
    road = db.query(PlanetOSMLine).filter(PlanetOSMLine.osm_id == osm_id).first()
    if not road:
        raise HTTPException(status_code=404, detail="Road not found")
    return road
