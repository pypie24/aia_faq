from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.product_line_schemas import (
    ProductLinesSchema,
    ProductLinesCreateSchema,
    ProductLinesUpdateSchema,
)
from src.services.product_line_services import ProductLinesService
from src.api.v1.dependencies import get_product_lines_service

router = APIRouter(prefix="/product_lines", tags=["product lines"])


# ProductLines Endpoints
@router.post("/", response_model=ProductLinesSchema)
async def create_product_line(
    data: ProductLinesCreateSchema,
    service: ProductLinesService = Depends(get_product_lines_service),
):
    return await service.create(data)


@router.get("/{line_id}", response_model=ProductLinesSchema)
async def get_product_line(
    line_id: UUID, service: ProductLinesService = Depends(get_product_lines_service)
):
    obj = await service.get(str(line_id))
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ProductLine not found")
    return obj


@router.put("/{line_id}", response_model=ProductLinesSchema)
async def update_product_line(
    line_id: UUID,
    data: ProductLinesUpdateSchema,
    service: ProductLinesService = Depends(get_product_lines_service),
):
    obj = await service.update(str(line_id), data)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ProductLine not found")
    return obj


@router.delete("/{line_id}", response_model=bool)
async def delete_product_line(
    line_id: UUID, service: ProductLinesService = Depends(get_product_lines_service)
):
    return await service.delete(str(line_id))


@router.get("/", response_model=list[ProductLinesSchema])
async def list_product_lines(
    category_id: UUID = None,
    brand_id: UUID = None,
    skip: int = 0,
    limit: int = 20,
    service: ProductLinesService = Depends(get_product_lines_service),
):
    return await service.list(category_id, brand_id, skip, limit)
