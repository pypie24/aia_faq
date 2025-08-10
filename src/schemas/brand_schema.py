from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class BrandCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class BrandUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class BrandSchema(BrandUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
