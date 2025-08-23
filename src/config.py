import os
import logging
from functools import lru_cache

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    DEBUG: bool = True if os.getenv("DEBUG", "False") == "True" else False
    VERSION: str = os.getenv("VERSION", "0.1.0")
    TITLE: str = os.getenv("TITLE", "FastAPI")
    OPENAI_ENDPOINT: str = os.environ["OPENAI_ENDPOINT"]
    OPENAI_LLM_API_KEY: str = os.environ["OPENAI_LLM_API_KEY"]
    OPENAI_LLM_MODEL: str = os.environ["OPENAI_LLM_MODEL"]
    OPENAI_EMBEDDING_API_KEY: str = os.environ["OPENAI_EMBEDDING_API_KEY"]
    OPENAI_EMBEDDING_MODEL: str = os.environ["OPENAI_EMBEDDING_MODEL"]
    OPENAI_API_VERSION: str = os.environ["OPENAI_API_VERSION"]
    GEMINI_API_KEY: str = os.environ["GEMINI_API_KEY"]
    GEMINI_MODEL: str = os.environ["GEMINI_MODEL"]
    ENVIRONMENT: str = os.environ["ENVIRONMENT"]
    POSTGRES_HOST: str = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT: str = os.environ["POSTGRES_PORT"]
    POSTGRES_USER: str = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB: str = os.environ["POSTGRES_DB"]
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "product_variants")
    CHAT_HISTORY_COLLECTION: str = os.getenv("CHAT_HISTORY_COLLECTION", "chat_history")
    SEMANTIC_CACHE_COLLECTION: str = os.getenv("SEMANTIC_CACHE_COLLECTION", "semantic_cache")
    MAX_HISTORY_ITEMS: int = int(os.getenv("MAX_HISTORY_ITEMS", 100))
    FILE_SERVER_BUCKET_NAME: str = os.getenv("FILE_SERVER_BUCKET_NAME", "faq-image")
    FILE_SERVER_ENDPOINT: str = os.environ["FILE_SERVER_ENDPOINT"]
    FILE_SERVER_ACCESS_KEY: str = os.environ["FILE_SERVER_ACCESS_KEY"]
    FILE_SERVER_SECRET_KEY: str = os.environ["FILE_SERVER_SECRET_KEY"]
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


settings = Settings()
