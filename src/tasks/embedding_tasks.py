# app/tasks/embedding_tasks.py
import asyncio
import logging

from openai import OpenAI
import chromadb
from celery import shared_task

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from src.db import get_db
from src.config import settings
from src.tasks.queue_uitils import push_to_queue, pop_all_from_queue
from src.models.product_models import ProductVariant
from src.utils.common import generate_product_text


chroma_client = chromadb.HttpClient(host="chromadb", port=8000)
embedding_client = OpenAI(
    base_url=settings.OPENAI_ENDPOINT,
    api_key=settings.OPENAI_EMBEDDING_API_KEY,
)

@shared_task
def enqueue_text(text_data: dict):
    push_to_queue(text_data)


@shared_task
def process_embedding_queue():
    items = pop_all_from_queue()
    if not items:
        log.info("No items")
        return

    for batch in items:
        texts = []
        ids = []
        metadatas = []

        for it in batch:
            texts.append(it["text"])
            ids.append(it["id"])
            metadatas.append({
                "brand": it["brand"],
                "category": it["category"],
                "tags": it["tags"]
            })

        resp = embedding_client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=texts
        )
        vectors = [d["embedding"] for d in resp["data"]]
        collection = chroma_client.get_or_create_collection("product_variants")
        collection.add(ids=ids, documents=texts, embeddings=vectors, metadatas=metadatas)

    return log.info(f"Processed {len(items)} items")


@shared_task
def process_unembedding_queue():
    async def async_task():
        collection = chroma_client.get_or_create_collection("product_variants")
        results = collection.get(include=[])
        all_ids = [doc["id"] for doc in results]

        async with get_db() as session:
            product_variants = await session.query(ProductVariant).filter(ProductVariant.id.notin_(all_ids))
            for variant in product_variants:
                enqueue_text(generate_product_text(variant))

    asyncio.run(async_task())
