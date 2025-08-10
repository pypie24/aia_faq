from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.category_schemas import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategorySchema,
)
from src.services.category_services import CategoryService
from src.api.v1.dependencies import get_category_service


router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreateSchema, service: CategoryService = Depends(get_category_service)
):
    return await service.create(data)


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(
    category_id: UUID, service: CategoryService = Depends(get_category_service)
):
    obj = await service.get(str(category_id))
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return obj


@router.put(
    "/{category_id}", response_model=CategorySchema, status_code=status.HTTP_200_OK
)
async def update_category(
    category_id: UUID,
    data: CategoryUpdateSchema,
    service: CategoryService = Depends(get_category_service),
):
    obj = await service.update(str(category_id), data)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return obj


@router.delete("/{category_id}", response_model=bool, status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: UUID, service: CategoryService = Depends(get_category_service)
):
    return await service.delete(str(category_id))


@router.get("/", response_model=list[CategorySchema], status_code=status.HTTP_200_OK)
async def list_categories(
    skip: int = 0,
    limit: int = 20,
    service: CategoryService = Depends(get_category_service),
):
    return await service.list(skip, limit)
