from fastapi import APIRouter, Depends

from src.api.dependencies import get_knowledge_service
from src.services.knowleadge_services import KnowledgeService
from src.schemas.knowledge_schemas import (
    KnowledgeCreateSchema,
    KnowledgeUpdateSchema,
    KnowledgeSchema,
)


router = APIRouter(prefix="/api/v1", tags=["knowledge"])


@router.get("/knowledge", response_model=list[KnowledgeSchema])
async def get_knowledges(
    skip: int = 0,
    limit: int = 20,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
):
    return await knowledge_service.list(skip=skip, limit=limit)


@router.post("/knowledge", response_model=KnowledgeSchema)
async def create_knowledge(
    knowledge_data: KnowledgeCreateSchema,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
):
    return await knowledge_service.create(knowledge_data)


@router.get("/knowledge/{knowledge_id}", response_model=KnowledgeSchema)
async def get_knowledge(
    knowledge_id: str,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
):
    return await knowledge_service.get(knowledge_id)


@router.put("/knowledge/{knowledge_id}", response_model=KnowledgeSchema)
async def update_knowledge(
    knowledge_id: str,
    knowledge_data: KnowledgeUpdateSchema,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
):
    return await knowledge_service.update(knowledge_id, knowledge_data)


@router.delete("/knowledge/{knowledge_id}", response_model=bool)
async def delete_knowledge(
    knowledge_id: str,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
):
    return await knowledge_service.delete(knowledge_id)
