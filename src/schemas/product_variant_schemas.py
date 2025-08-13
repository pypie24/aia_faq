from uuid import UUID
from typing import Optional, Dict

from src.schemas.base_schema import BaseSchema



class ProductVariantCreateSchema(BaseSchema):
    product_id: UUID
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
    slug: Optional[str] = None

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
