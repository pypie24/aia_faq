# app/tasks/embedding_tasks.py
import logging

from openai import OpenAI
import chromadb
from minio import Minio


from src.config import settings


chroma_client = chromadb.HttpClient(host="chromadb", port=8000)
minio_client = Minio(
    settings.FILE_SERVER_ENDPOINT,
    access_key=settings.FILE_SERVER_ACCESS_KEY,
    secret_key=settings.FILE_SERVER_SECRET_KEY,
    secure=False
)

if not minio_client.bucket_exists(settings.FILE_SERVER_BUCKET_NAME):
    minio_client.make_bucket(settings.FILE_SERVER_BUCKET_NAME)


embedding_client = OpenAI(
    base_url=settings.OPENAI_ENDPOINT,
    api_key=settings.OPENAI_EMBEDDING_API_KEY,
)

llm_client = OpenAI(
    base_url=settings.OPENAI_ENDPOINT,
    api_key=settings.OPENAI_LLM_API_KEY,
)
