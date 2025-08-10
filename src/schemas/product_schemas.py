from uuid import UUID
from typing import Optional, Dict
from pydantic import BaseModel


class ProductLinesCreateSchema(BaseModel):
    name: str
    brand_id: UUID
    category_id: UUID
    release_years: int
    description: str
    url: str
    slug: str

    class Config:
        orm_mode = True


class ProductLinesUpdateSchema(BaseModel):
    name: Optional[str] = None
    brand_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    release_years: Optional[int] = None
    description: Optional[str] = None
    url: Optional[str] = None
    slug: Optional[str] = None

    class Config:
        orm_mode = True


class ProductLinesSchema(ProductLinesUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}


class ProductCreateSchema(BaseModel):
    name: str
    product_line_id: UUID
    release_date: str
    url: str
    slug: str

    class Config:
        orm_mode = True


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    product_line_id: Optional[UUID] = None
    release_date: Optional[str] = None
    url: Optional[str] = None
    slug: Optional[str] = None

    class Config:
        orm_mode = True


class ProductSchema(ProductUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}


class ProductVariantCreateSchema(BaseModel):
    product_id: UUID
    color: str
    price: float
    stock: int
    specs: Dict
    url: str
    slug: str

    class Config:
        orm_mode = True


class ProductVariantUpdateSchema(BaseModel):
    product_id: Optional[UUID] = None
    color: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    specs: Optional[Dict] = None
    url: Optional[str] = None
    slug: Optional[str] = None

    class Config:
        orm_mode = True


class ProductVariantSchema(ProductVariantUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
