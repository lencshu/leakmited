# src/schemas.py
from pydantic import BaseModel
from typing import List, Optional


class Geometry(BaseModel):
    # type: str
    coordinates: List[List[float]]


class RoadProperties(BaseModel):
    maxspeed: Optional[int]
    highway: Optional[str]
    osm_id: int


class RoadGeoJSON(BaseModel):
    geometry: Geometry
    # properties: RoadProperties


class RoadBase(BaseModel):
    osm_id: int
    highway: Optional[str]
    maxspeed: Optional[str]

    class Config:
        from_attributes = True  # auto parse Pydantic from orm


class StatsBase(BaseModel):
    total_length: float
    speed_distribution: dict[str, float]
