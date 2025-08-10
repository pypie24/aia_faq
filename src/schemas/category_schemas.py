from uuid import UUID
from typing import Optional, Dict
from pydantic import BaseModel


class CategoryCreateSchema(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class CategorySchema(CategoryUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
