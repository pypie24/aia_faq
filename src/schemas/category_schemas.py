from uuid import UUID
from typing import Optional

from src.schemas.base_schema import BaseSchema


class CategoryCreateSchema(BaseSchema):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class CategoryUpdateSchema(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class CategorySchema(CategoryUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
