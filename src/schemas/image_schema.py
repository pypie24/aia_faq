from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class ImageCreateSchema(BaseModel):
    name: str
    url: str
    alt_text: str
    content: bytes

    class Config:
        orm_mode = True


class ImageUpdateSchema(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    alt_text: Optional[str] = None
    content: Optional[bytes] = None

    class Config:
        orm_mode = True


class ImageSchema(BaseModel):
    id: UUID
    name: str
    url: str
    alt_text: str

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}


class ImageAssignmentCreateSchema(BaseModel):
    image_id: UUID
    entity_id: UUID
    entity_type: str
    sort_order: int

    class Config:
        orm_mode = True


class ImageAssignmentUpdateSchema(BaseModel):
    image_id: Optional[UUID] = None
    entity_id: Optional[UUID] = None
    entity_type: Optional[str] = None
    sort_order: Optional[int] = None

    class Config:
        orm_mode = True


class ImageAssignmentSchema(ImageAssignmentUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
