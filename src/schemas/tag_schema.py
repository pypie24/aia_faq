from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class TagCreateSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class TagUpdateSchema(BaseModel):
    name: Optional[str] = None

    class Config:
        orm_mode = True


class TagSchema(TagUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}


class TagAssignmentCreateSchema(BaseModel):
    tag_id: UUID
    entity_id: UUID
    entity_type: str
    sort_order: int

    class Config:
        orm_mode = True


class TagAssignmentUpdateSchema(BaseModel):
    tag_id: Optional[UUID] = None
    entity_id: Optional[UUID] = None
    entity_type: Optional[str] = None
    sort_order: Optional[int] = None

    class Config:
        orm_mode = True


class TagAssignmentSchema(TagAssignmentUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
