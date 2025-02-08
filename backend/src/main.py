# app/main.py
from fastapi import FastAPI

# from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from mangum import Mangum

from src.core.database import engine, metadata
from src.routers import roads, stats

app = FastAPI(title="Leakmited Road Network API", description="Demo backend with FastAPI + PostGIS (planet_osm_line)", version="1.0.0")

# Add GZip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=100000)  # Only compress if the response size is greater than 100KB


metadata.create_all(bind=engine)

app.include_router(roads.router)
app.include_router(stats.router)

handler = Mangum(app)
