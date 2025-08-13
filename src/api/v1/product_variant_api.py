from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.product_variant_schemas import (
    ProductVariantSchema,
    ProductVariantCreateSchema,
    ProductVariantUpdateSchema,
)
from src.services.product_variant_services import ProductVariantService
from src.api.v1.dependencies import get_product_variant_service

router = APIRouter(prefix="/product_variants", tags=["product variants"])


# ProductVariant Endpoints
@router.post("/", response_model=ProductVariantSchema)
async def create_product_variant(
    data: ProductVariantCreateSchema,
    service: ProductVariantService = Depends(get_product_variant_service),
):
    return await service.create(data)


@router.get("/{variant_id}", response_model=ProductVariantSchema)
async def get_product_variant(
    variant_id: UUID,
    service: ProductVariantService = Depends(get_product_variant_service),
):
    obj = await service.get(str(variant_id))
    if not obj:
        raise HTTPException(status_code=404, detail="ProductVariant not found")
    return obj


@router.put("/{variant_id}", response_model=ProductVariantSchema)
async def update_product_variant(
    variant_id: UUID,
    data: ProductVariantUpdateSchema,
    service: ProductVariantService = Depends(get_product_variant_service),
):
    obj = await service.update(str(variant_id), data)
    if not obj:
        raise HTTPException(status_code=404, detail="ProductVariant not found")
    return obj


@router.delete("/{variant_id}", response_model=bool)
async def delete_product_variant(
    variant_id: UUID,
    service: ProductVariantService = Depends(get_product_variant_service),
):
    return await service.delete(str(variant_id))


@router.get("/", response_model=list[ProductVariantSchema])
async def list_product_variants(
    brand_id: UUID = None,
    category_id: UUID = None,
    product_id: UUID = None,
    min_price: float = None,
    max_price: float = None,
    tags: list[UUID] = None,
    skip: int = 0,
    limit: int = 20,
    service: ProductVariantService = Depends(get_product_variant_service),
):
    return await service.list(brand_id, category_id, product_id, min_price, max_price, tags, skip, limit)
