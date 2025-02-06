# app/core/database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from .config import settings

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@" f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)

metadata = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
