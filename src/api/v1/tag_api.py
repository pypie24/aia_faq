from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.services.tag_services import TagService
from src.schemas.tag_schema import (
    TagSchema,
    TagCreateSchema,
    TagUpdateSchema,
)
from src.api.v1.dependencies import get_tag_service

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagSchema, status_code=status.HTTP_201_CREATED)
async def create_tag(
    data: TagCreateSchema, service: TagService = Depends(get_tag_service)
):
    return await service.create(data)


@router.get("/{tag_id}", response_model=TagSchema, status_code=status.HTTP_200_OK)
async def get_tag(tag_id: UUID, service: TagService = Depends(get_tag_service)):
    obj = await service.get(str(tag_id))
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return obj


@router.put("/{tag_id}", response_model=TagSchema, status_code=status.HTTP_200_OK)
async def update_tag(
    tag_id: UUID, data: TagUpdateSchema, service: TagService = Depends(get_tag_service)
):
    obj = await service.update(str(tag_id), data)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return obj


@router.delete("/{tag_id}", response_model=bool, status_code=status.HTTP_200_OK)
async def delete_tag(tag_id: UUID, service: TagService = Depends(get_tag_service)):
    return await service.delete(str(tag_id))


@router.get("/", response_model=list[TagSchema], status_code=status.HTTP_200_OK)
async def list_tags(
    skip: int = 0, limit: int = 20, service: TagService = Depends(get_tag_service)
):
    return await service.list(skip, limit)
