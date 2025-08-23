# app/tasks/embedding_tasks.py
import json

from openai import OpenAI
from google import genai
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

minio_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": "s3:*",
            "Resource": f"arn:aws:s3:::{settings.FILE_SERVER_BUCKET_NAME}/*"
        }
    ]
}

minio_client.set_bucket_policy(
    settings.FILE_SERVER_BUCKET_NAME, json.dumps(minio_policy)
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

gemini_client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
)
