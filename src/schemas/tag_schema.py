from uuid import UUID
from typing import Optional

from src.schemas.base_schema import BaseSchema


class TagCreateSchema(BaseSchema):
    name: str

    class Config:
        orm_mode = True


class TagUpdateSchema(BaseSchema):
    name: Optional[str] = None

    class Config:
        orm_mode = True


class TagSchema(TagUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
