from uuid import UUID
from typing import Optional, Dict

from src.schemas.base_schema import BaseSchema


class ProductLinesCreateSchema(BaseSchema):
    name: str
    brand_id: UUID
    category_id: UUID
    description: Optional[str] = None
    url: Optional[str] = None
    slug: Optional[str] = None

    class Config:
        orm_mode = True


class ProductLinesUpdateSchema(ProductLinesCreateSchema):
    name: Optional[str] = None
    brand_id: Optional[UUID] = None
    category_id: Optional[UUID] = None

    class Config:
        orm_mode = True


class ProductLinesSchema(ProductLinesUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}


class ProductCreateSchema(BaseSchema):
    name: str
    product_line_id: UUID
    release_date: Optional[str] = None
    sku: Optional[str] = None
    url: Optional[str] = None

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


class ProductVariantCreateSchema(BaseSchema):
    name: str
    price: Optional[float] = None
    stock: Optional[int] = None
    specs: Optional[Dict] = None
    url: Optional[str] = None

    class Config:
        orm_mode = True


class ProductVariantUpdateSchema(BaseSchema):
    product_id: Optional[UUID] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    specs: Optional[Dict] = None
    url: Optional[str] = None

    class Config:
        orm_mode = True


class ProductVariantSchema(ProductVariantUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
