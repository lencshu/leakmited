# app/main.py
from fastapi import FastAPI
from mangum import Mangum

from src.core.database import engine, metadata
from src.routers import roads, stats

app = FastAPI(title="Leakmited Road Network API", description="Demo backend with FastAPI + PostGIS (planet_osm_line)", version="1.0.0")

metadata.create_all(bind=engine)

app.include_router(roads.router, prefix="/roads", tags=["roads"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])

handler = Mangum(app)
