from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.product_schemas import (
    ProductSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
)
from src.services.product_services import ProductService
from src.api.v1.dependencies import get_product_service

router = APIRouter(prefix="/products", tags=["products"])


# Product Endpoints
@router.post("/", response_model=ProductSchema)
async def create_product(
    data: ProductCreateSchema, service: ProductService = Depends(get_product_service)
):
    return await service.create(data)


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: UUID, service: ProductService = Depends(get_product_service)
):
    obj = await service.get(str(product_id))
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    return obj


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: UUID,
    data: ProductUpdateSchema,
    service: ProductService = Depends(get_product_service),
):
    obj = await service.update(str(product_id), data)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    return obj


@router.delete("/{product_id}", response_model=bool)
async def delete_product(
    product_id: UUID, service: ProductService = Depends(get_product_service)
):
    return await service.delete(str(product_id))


@router.get("/", response_model=list[ProductSchema])
async def list_products(
    brand_id: UUID = None,
    category_id: UUID = None,
    product_line_id: UUID = None,
    skip: int = 0,
    limit: int = 20,
    service: ProductService = Depends(get_product_service),
):
    return await service.list(brand_id, category_id, product_line_id, skip, limit)
