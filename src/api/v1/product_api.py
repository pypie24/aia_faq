from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.product_schemas import (
    ProductLinesSchema,
    ProductLinesCreateSchema,
    ProductLinesUpdateSchema,
    ProductSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductVariantSchema,
    ProductVariantCreateSchema,
    ProductVariantUpdateSchema,
)
from src.services.product_services import (
    ProductLinesService,
    ProductService,
    ProductVariantService,
)
from src.api.v1.dependencies import (
    get_product_lines_service,
    get_product_service,
    get_product_variant_service,
)

router = APIRouter(prefix="/products", tags=["products"])


# ProductLines Endpoints
@router.post("/lines", response_model=ProductLinesSchema)
async def create_product_line(
    data: ProductLinesCreateSchema,
    service: ProductLinesService = Depends(get_product_lines_service),
):
    return await service.create(data)


@router.get("/lines/{line_id}", response_model=ProductLinesSchema)
async def get_product_line(
    line_id: UUID, service: ProductLinesService = Depends(get_product_lines_service)
):
    obj = await service.get(str(line_id))
    if not obj:
        raise HTTPException(status_code=404, detail="ProductLine not found")
    return obj


@router.put("/lines/{line_id}", response_model=ProductLinesSchema)
async def update_product_line(
    line_id: UUID,
    data: ProductLinesUpdateSchema,
    service: ProductLinesService = Depends(get_product_lines_service),
):
    obj = await service.update(str(line_id), data)
    if not obj:
        raise HTTPException(status_code=404, detail="ProductLine not found")
    return obj


@router.delete("/lines/{line_id}", response_model=bool)
async def delete_product_line(
    line_id: UUID, service: ProductLinesService = Depends(get_product_lines_service)
):
    return await service.delete(str(line_id))


@router.get("/lines", response_model=list[ProductLinesSchema])
async def list_product_lines(
    category_id: UUID = None,
    brand_id: UUID = None,
    skip: int = 0,
    limit: int = 20,
    service: ProductLinesService = Depends(get_product_lines_service),
):
    return await service.list(category_id, brand_id, skip, limit)


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
    skip: int = 0,
    limit: int = 20,
    service: ProductService = Depends(get_product_service),
):
    return await service.list(skip, limit)


# ProductVariant Endpoints
@router.post("/{product_id}/variants", response_model=ProductVariantSchema)
async def create_product_variant(
    product_id: UUID,
    data: ProductVariantCreateSchema,
    service: ProductVariantService = Depends(get_product_variant_service),
):
    return await service.create(product_id, data)


@router.get("/{product_id}/variants/{variant_id}", response_model=ProductVariantSchema)
async def get_product_variant(
    product_id: UUID,
    variant_id: UUID,
    service: ProductVariantService = Depends(get_product_variant_service),
):
    obj = await service.get(str(variant_id))
    if not obj:
        raise HTTPException(status_code=404, detail="ProductVariant not found")
    return obj


@router.put("/{product_id}/variants/{variant_id}", response_model=ProductVariantSchema)
async def update_product_variant(
    product_id: UUID,
    variant_id: UUID,
    data: ProductVariantUpdateSchema,
    service: ProductVariantService = Depends(get_product_variant_service),
):
    obj = await service.update(str(variant_id), data)
    if not obj:
        raise HTTPException(status_code=404, detail="ProductVariant not found")
    return obj


@router.delete("/{product_id}/variants/{variant_id}", response_model=bool)
async def delete_product_variant(
    product_id: UUID,
    variant_id: UUID,
    service: ProductVariantService = Depends(get_product_variant_service),
):
    return await service.delete(str(variant_id))


@router.get("/{product_id}/variants", response_model=list[ProductVariantSchema])
async def list_product_variants(
    product_id: UUID,
    skip: int = 0,
    limit: int = 20,
    service: ProductVariantService = Depends(get_product_variant_service),
):
    return await service.list(product_id, skip, limit)
