from sqlalchemy import Column, String

from src.models.base import BaseModel


class Knowledge(BaseModel):
    __tablename__ = "knowledge"

    question = Column(String, index=True, nullable=False, unique=True)
    response = Column(String, nullable=False)

    def __repr__(self):
        return f"<Knowledge(id={self.id}, question={self.question}, response={self.response})>"
