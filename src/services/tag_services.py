from sqlalchemy.future import select

from src.models.product_models import Tag, TagAssignment
from src.schemas.product_schemas import (
    TagCreateSchema,
    TagUpdateSchema,
    TagAssignmentCreateSchema,
    TagAssignmentUpdateSchema,
)
from src.services.base_services import BaseServiceDBSession
from src.utils.common import update_obj_from_dict


class TagService(BaseServiceDBSession):
    async def create(self, data: TagCreateSchema) -> Tag:
        obj = Tag(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: str) -> Tag | None:
        result = await self.session.execute(select(Tag).where(Tag.id == obj_id))
        return result.scalar_one_or_none()

    async def update(self, obj_id: str, data: TagUpdateSchema) -> Tag | None:
        result = await self.session.execute(select(Tag).where(Tag.id == obj_id))
        obj = result.scalar_one_or_none()
        if obj is None:
            return None
        update_obj_from_dict(obj, data.model_dump(exclude_unset=True))
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: str) -> bool:
        result = await self.session.execute(select(Tag).where(Tag.id == obj_id))
        obj = result.scalar_one_or_none()
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def list(self, skip: int = 0, limit: int = 20) -> list[Tag]:
        result = await self.session.execute(select(Tag).offset(skip).limit(limit))
        return result.scalars().all()


class TagAssignmentService(BaseServiceDBSession):
    async def create(self, data: TagAssignmentCreateSchema) -> TagAssignment:
        obj = TagAssignment(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: str) -> TagAssignment | None:
        result = await self.session.execute(
            select(TagAssignment).where(TagAssignment.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def update(
        self, obj_id: str, data: TagAssignmentUpdateSchema
    ) -> TagAssignment | None:
        result = await self.session.execute(
            select(TagAssignment).where(TagAssignment.id == obj_id)
        )
        obj = result.scalar_one_or_none()
        if obj is None:
            return None
        update_obj_from_dict(obj, data.model_dump(exclude_unset=True))
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: str) -> bool:
        result = await self.session.execute(
            select(TagAssignment).where(TagAssignment.id == obj_id)
        )
        obj = result.scalar_one_or_none()
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def list(self, skip: int = 0, limit: int = 20) -> list[TagAssignment]:
        result = await self.session.execute(
            select(TagAssignment).offset(skip).limit(limit)
        )
        return result.scalars().all()
