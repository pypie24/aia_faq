from uuid import UUID
from typing import Optional

from src.schemas.base_schema import BaseSchema


class ProductCreateSchema(BaseSchema):
    name: str
    product_line_id: UUID
    release_date: Optional[str] = None
    sku: Optional[str] = None
    url: Optional[str] = None
    images: list[str] = []

    class Config:
        orm_mode = True


class ProductUpdateSchema(ProductCreateSchema):
    name: Optional[str] = None
    product_line_id: Optional[UUID] = None

    class Config:
        orm_mode = True


class ProductSchema(ProductUpdateSchema):
    id: UUID
    slug: Optional[str] = None

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
