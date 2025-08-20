import logging

from fastapi import APIRouter, Depends
from sqlalchemy.future import select

from src.config import settings
from src.db import get_db, get_redis, AsyncSession, Redis
from src.models.product_models import Brand, Category, Tag
from src.tools.client import (
    embedding_client,
)
from src.services.chat_services import (
    RAG,
    OpenAiClient,
    Reflection,
    GuardedRAGAgent
)
from src.schemas.chat_schemas import ChatRequest, ChatResponse
from src.tools.cache import redis_cache


log = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])
rag = RAG(
    collection_name=settings.COLLECTION_NAME,
)

llm = OpenAiClient()

reflection = Reflection(
    llm=llm,
    chat_history_collection=settings.CHAT_HISTORY_COLLECTION,
    semantic_cache_collection=settings.SEMANTIC_CACHE_COLLECTION
)

agent_router = GuardedRAGAgent(
    rag=rag,
    embedding_client=embedding_client,
    embedding_model=settings.OPENAI_EMBEDDING_MODEL,
    fallback_reflection=reflection,
    similarity_threshold=0.8,
    max_last_items=settings.MAX_HISTORY_ITEMS
)


@router.post("/", response_model=ChatResponse)
async def chatbot(
    data: ChatRequest,
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db)
):
    query = data.message
    session_id = str(data.session_id)

    log.debug(f"[API DEBUG] Incoming query: {query}, session_id: {session_id}")

    # Gọi agent invoke (multi-turn + query rewrite + RAG + fallback)
    # get product keyword from cached if exist else call get new
    tags = await product_keywords(redis=redis, session=session)
    result = agent_router.invoke(query=query, tags=tags, session_id=session_id)

    # Debug chi tiết
    log.debug(f"[API DEBUG] Agent output (first 300 chars): {result['output'][:300]}")
    if hasattr(agent_router, 'last_rewritten_query'):
        log.debug(f"[API DEBUG] Rewritten standalone query: {agent_router.last_rewritten_query}")

    return {"role": "assistant", "content": result["output"]}


# add cached ttl
@redis_cache(ttl=300)
@router.get("/keywords", response_model=list[str])
async def product_keywords(
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(get_db)
):
    """
    Lấy danh sách từ khóa sản phẩm.
    """
    log.info("[API Log] get keywords from db")
    brands = await session.execute(select(Brand.name))
    brands_name = brands.scalars().all()
    categories = await session.execute(select(Category.name))
    categories_name = categories.scalars().all()
    tags = await session.execute(select(Tag.name))
    tags_name = tags.scalars().all()
    return brands_name + categories_name + tags_name
