from uuid import UUID
from typing import Optional

from src.schemas.base_schema import BaseSchema


class ImageCreateSchema(BaseSchema):
    name: str
    content: Optional[bytes] = None
    alt_text: Optional[str] = None

    class Config:
        orm_mode = True


class ImageUpdateSchema(BaseSchema):
    name: Optional[str] = None
    url: Optional[str] = None
    alt_text: Optional[str] = None
    content: Optional[bytes] = None

    class Config:
        orm_mode = True


class ImageSchema(BaseSchema):
    id: UUID
    name: str
    url: str
    alt_text: str

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
