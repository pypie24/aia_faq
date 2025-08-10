from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.brand_schema import BrandCreateSchema, BrandUpdateSchema, BrandSchema
from src.services.brand_services import BrandService
from src.api.v1.dependencies import get_brand_service


router = APIRouter(prefix="/brands", tags=["brands"])


@router.post("/", response_model=BrandSchema, status_code=status.HTTP_201_CREATED)
async def create_brand(
    data: BrandCreateSchema, service: BrandService = Depends(get_brand_service)
):
    return await service.create(data)


@router.get("/{brand_id}", response_model=BrandSchema, status_code=status.HTTP_200_OK)
async def get_brand(brand_id: UUID, service: BrandService = Depends(get_brand_service)):
    obj = await service.get(str(brand_id))
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found"
        )
    return obj


@router.put("/{brand_id}", response_model=BrandSchema, status_code=status.HTTP_200_OK)
async def update_brand(
    brand_id: UUID,
    data: BrandUpdateSchema,
    service: BrandService = Depends(get_brand_service),
):
    obj = await service.update(str(brand_id), data)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found"
        )
    return obj


@router.delete("/{brand_id}", response_model=bool, status_code=status.HTTP_200_OK)
async def delete_brand(
    brand_id: UUID, service: BrandService = Depends(get_brand_service)
):
    return await service.delete(str(brand_id))


@router.get("/", response_model=list[BrandSchema], status_code=status.HTTP_200_OK)
async def list_brands(
    skip: int = 0, limit: int = 20, service: BrandService = Depends(get_brand_service)
):
    return await service.list(skip, limit)
