# app/schemas.py
from typing import Optional
from pydantic import BaseModel


class RoadBase(BaseModel):
    osm_id: int
    highway: Optional[str]
    maxspeed: Optional[str]

    class Config:
        orm_mode = True  # auto parse Pydantic from orm


class StatsBase(BaseModel):
    total_length: float
    speed_distribution: dict[str, float]
