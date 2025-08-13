from uuid import UUID
from typing import Optional

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
