from sqlalchemy.future import select

from sqlalchemy.ext.asyncio import AsyncSession
from src.models.knowledge_models import Knowledge
from src.schemas.knowledge_schemas import (
    KnowledgeCreateSchema,
    KnowledgeUpdateSchema,
    KnowledgeSchema,
)

from src.utils.common import update_obj_from_dict


class KnowledgeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, knowledge_data: KnowledgeCreateSchema) -> Knowledge:
        knowledge = Knowledge(**knowledge_data.model_dump())
        self.db.add(knowledge)
        await self.db.commit()
        await self.db.refresh(knowledge)
        return knowledge

    async def get(self, knowledge_id: str) -> Knowledge | None:
        result = await self.db.execute(
            select(Knowledge).where(Knowledge.id == knowledge_id)
        )
        knowledge = result.scalar_one_or_none()
        if knowledge is None:
            return None
        return knowledge

    async def update(
        self, knowledge_id: str, knowledge_data: KnowledgeUpdateSchema
    ) -> Knowledge | None:
        result = await self.db.execute(
            select(Knowledge).where(Knowledge.id == knowledge_id)
        )
        knowledge = result.scalar_one_or_none()
        if knowledge is None:
            return None

        update_obj_from_dict(knowledge, knowledge_data.model_dump(exclude_unset=True))

        await self.db.commit()
        await self.db.refresh(knowledge)
        return KnowledgeSchema.model_validate(knowledge)

    async def delete(self, knowledge_id: str) -> bool:
        result = await self.db.execute(
            select(Knowledge).where(Knowledge.id == knowledge_id)
        )
        knowledge = result.scalar_one_or_none()
        if knowledge is None:
            return False

        await self.db.delete(knowledge)
        await self.db.commit()
        return True

    async def list(self, skip: int = 0, limit: int = 20) -> list[Knowledge]:
        result = await self.db.execute(select(Knowledge).offset(skip).limit(limit))
        knowledge_list = result.scalars().all()
        return knowledge_list
