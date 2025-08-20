from typing import Optional
from uuid import UUID

from pydantic import BaseModel



class ChatRequest(BaseModel):
    session_id: UUID
    message: str


class ChatResponse(BaseModel):
    session_id: Optional[UUID] = None
    role: str
    content: str
