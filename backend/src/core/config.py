# src/core/config.py
import os
from pydantic_settings import BaseSettings

ROADS_NUM_LIMIT = 100000


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    # STAGE: str = "dev"
    # API_PREFIX: str = "/api"

    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"


settings = Settings()
