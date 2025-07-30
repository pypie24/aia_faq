from uuid import uuid4

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from src.db import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(
        "created_at",
        sqlalchemy.DateTime(timezone=True),
        server_default=sqlalchemy.func.now(),
        nullable=False,
    )
    updated_at = Column(
        "updated_at",
        sqlalchemy.DateTime(timezone=True),
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
        nullable=False,
    )
