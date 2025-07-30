from uuid import UUID
from typing import Optional

from pydantic import BaseModel


class KnowledgeCreateSchema(BaseModel):
    question: str
    response: str

    class Config:
        orm_mode = True


class KnowledgeUpdateSchema(BaseModel):
    question: Optional[str] = None
    response: Optional[str] = None

    class Config:
        orm_mode = True


class KnowledgeSchema(KnowledgeUpdateSchema):
    id: UUID

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
