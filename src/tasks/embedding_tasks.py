# app/tasks/embedding_tasks.py
import asyncio
import logging

from celery import shared_task
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.db import AsyncSessionLocal
from src.config import settings
from src.tasks.queue_uitils import push_to_queue, pop_all_from_queue
from src.tasks.celery_app import celery_app
from src.models.product_models import (
    ProductLines,
    Product,
    ProductVariant,
)
from src.utils.common import generate_product_text
from src.tools.client import embedding_client, chroma_client

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

collection = chroma_client.get_or_create_collection(settings.COLLECTION_NAME)
chat_history_collection = chroma_client.get_or_create_collection(settings.CHAT_HISTORY_COLLECTION)
semantic_cached_collection = chroma_client.get_or_create_collection(settings.SEMANTIC_CACHE_COLLECTION)

@shared_task
def enqueue_text(text_data: dict):
    push_to_queue(text_data)


@celery_app.task(name="src.tasks.embedding_tasks.process_embedding_queue")
def process_embedding_queue():
    items = pop_all_from_queue()
    if not items:
        log.info("No items")
        return

    for idx, batch in enumerate(items):
        documents = []
        ids = []
        metadatas = []
        embeddings = []

        for it in batch:
            documents.append(it["text"])
            ids.append(it["id"])
            metadatas.append({
                "brand": it["brand"],
                "category": it["category"],
                **{
                    f"tag_{key}": True for key in it["tags"]
                }
            })

        log.info(f"Processing batch {idx} with {len(documents)} texts")
        resp = embedding_client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=documents
        )
        embeddings = [d.embedding for d in resp.data]
        log.info(f"Processed embedding for: {len(embeddings)} vectors")
        collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

    return log.info(f"Processed {len(items)} items")


@celery_app.task(name="src.tasks.embedding_tasks.process_unembedding_queue")
def process_unembedding_queue():
    async def async_task():
        result = collection.get(include=[])
        all_ids = result.get("ids", [])
        variants = []

        async with AsyncSessionLocal() as session:
            results = await session.execute(
                select(ProductVariant)
                .filter(ProductVariant.id.notin_(all_ids))
                .options(
                    selectinload(ProductVariant.tags),
                    selectinload(ProductVariant.product)
                        .selectinload(Product.product_line)
                        .selectinload(ProductLines.brand),
                    selectinload(ProductVariant.product)
                        .selectinload(Product.product_line)
                        .selectinload(ProductLines.category),
                )
            )
            variants = results.scalars().unique().all()

        log.info(f"Processing {len(variants)} product variants for unembedding")
        for variant in variants:
            variant_text = generate_product_text(variant)
            enqueue_text(variant_text)

    asyncio.run(async_task())


def clear_collection(collection_embedding):
    ids = collection_embedding.get()["ids"]
    if ids:
        collection_embedding.delete(ids=ids)


@celery_app.task(name="src.tasks.embedding_tasks.clear_product_embedding")
def clear_product_embedding():
    clear_collection(collection)


@celery_app.task(name="src.tasks.embedding_tasks.clear_history_chat_embedding")
def clear_history_chat_embedding():
    clear_collection(chat_history_collection)


@celery_app.task(name="src.tasks.embedding_tasks.clear_semantic_cached_embedding")
def clear_semantic_cached_embedding():
    clear_collection(semantic_cached_collection)
