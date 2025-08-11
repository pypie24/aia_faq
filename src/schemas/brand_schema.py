from uuid import UUID
from typing import Optional

from src.schemas.base_schema import BaseSchema


class BrandCreateSchema(BaseSchema):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class BrandUpdateSchema(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class BrandSchema(BrandUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
