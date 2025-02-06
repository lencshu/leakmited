# app/models.py
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from src.core.database import metadata

Base = declarative_base(metadata=metadata)


class PlanetOSMLine(Base):
    __tablename__ = "planet_osm_line"

    osm_id = Column(BigInteger, primary_key=True)
    highway = Column(String, nullable=True)

    tags = Column(HSTORE, nullable=True)

    way = Column(Geometry("LINESTRING", srid=4326))

    @property
    def maxspeed(self):
        """
        get 'maxspeed' from tags
        """
        if not self.tags:
            return None
        return self.tags.get("maxspeed")
