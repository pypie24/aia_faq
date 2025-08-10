import os
import logging
from functools import lru_cache

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from distutils.util import strtobool

load_dotenv()


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    DEBUG: bool = strtobool(os.getenv("DEBUG", "False"))
    VERSION: str = os.getenv("VERSION", "0.1.0")
    TITLE: str = os.getenv("TITLE", "FastAPI")
    OPENAI_HOST: str = os.environ["OPENAI_HOST"]
    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
    OPENAI_MODEL: str = os.environ["OPENAI_MODEL"]
    ENVIRONMENT: str = os.environ["ENVIRONMENT"]
    POSTGRES_HOST: str = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT: str = os.environ["POSTGRES_PORT"]
    POSTGRES_USER: str = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB: str = os.environ["POSTGRES_DB"]
    POSTGRES_DB_TEST: str = os.getenv("POSTGRES_DB_TEST", "faq_db_test")
    FILE_SERVER_BUCKET_NAME: str = os.getenv("FILE_SERVER_BUCKET_NAME", "faq-image")
    FILE_SERVER_ENDPOINT: str = os.environ["FILE_SERVER_ENDPOINT"]
    FILE_SERVER_ACCESS_KEY: str = os.environ["FILE_SERVER_ACCESS_KEY"]
    FILE_SERVER_SECRET_KEY: str = os.environ["FILE_SERVER_SECRET_KEY"]
    FILE_SERVER_SECURE: bool = os.getenv("FILE_SERVER_SECURE", "true").lower() == "true"
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()
