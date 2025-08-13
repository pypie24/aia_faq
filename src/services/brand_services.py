from sqlalchemy.future import select

from src.models.product_models import Brand
from src.schemas.brand_schemas import (
    BrandCreateSchema,
    BrandUpdateSchema,
)
from src.services.base_services import BaseServiceDBSession
from src.utils.common import update_obj_from_dict


class BrandService(BaseServiceDBSession):
    async def create(self, data: BrandCreateSchema) -> Brand:
        obj = Brand(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: str) -> Brand | None:
        result = await self.session.execute(select(Brand).where(Brand.id == obj_id))
        return result.scalar_one_or_none()

    async def update(self, obj_id: str, data: BrandUpdateSchema) -> Brand | None:
        result = await self.session.execute(select(Brand).where(Brand.id == obj_id))
        obj = result.scalar_one_or_none()
        if obj is None:
            return None
        update_obj_from_dict(obj, data.model_dump(exclude_unset=True))
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: str) -> bool:
        result = await self.session.execute(select(Brand).where(Brand.id == obj_id))
        obj = result.scalar_one_or_none()
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def list(self, skip: int = 0, limit: int = 20) -> list[Brand]:
        result = await self.session.execute(select(Brand).offset(skip).limit(limit))
        return result.scalars().all()
