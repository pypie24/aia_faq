from sqlalchemy.future import select

from src.models.product_models import Category
from src.schemas.category_schemas import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
)
from src.services.base_services import BaseServiceDBSession
from src.utils.common import update_obj_from_dict


class CategoryService(BaseServiceDBSession):
    async def create(self, data: CategoryCreateSchema) -> Category:
        obj = Category(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: str) -> Category | None:
        result = await self.session.execute(
            select(Category).where(Category.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def update(self, obj_id: str, data: CategoryUpdateSchema) -> Category | None:
        result = await self.session.execute(
            select(Category).where(Category.id == obj_id)
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
            select(Category).where(Category.id == obj_id)
        )
        obj = result.scalar_one_or_none()
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def list(self, skip: int = 0, limit: int = 20) -> list[Category]:
        result = await self.session.execute(select(Category).offset(skip).limit(limit))
        return result.scalars().all()
