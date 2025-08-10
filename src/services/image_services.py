from sqlalchemy.future import select
import boto3

from src.models.product_models import Image, ImageAssignment
from src.schemas.image_schema import (
    ImageCreateSchema,
    ImageUpdateSchema,
    ImageAssignmentCreateSchema,
    ImageAssignmentUpdateSchema,
)
from src.services.base_services import BaseServiceDBSession
from src.utils.common import update_obj_from_dict


class ImageService(BaseServiceDBSession):
    async def create(self, data: ImageCreateSchema) -> Image:
        obj = Image(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: str) -> Image | None:
        result = await self.session.execute(select(Image).where(Image.id == obj_id))
        return result.scalar_one_or_none()

    async def update(self, obj_id: str, data: ImageUpdateSchema) -> Image | None:
        result = await self.session.execute(select(Image).where(Image.id == obj_id))
        obj = result.scalar_one_or_none()
        if obj is None:
            return None
        update_obj_from_dict(obj, data.model_dump(exclude_unset=True))
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: str) -> bool:
        result = await self.session.execute(select(Image).where(Image.id == obj_id))
        obj = result.scalar_one_or_none()
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def list(self, skip: int = 0, limit: int = 20) -> list[Image]:
        result = await self.session.execute(select(Image).offset(skip).limit(limit))
        return result.scalars().all()


class ImageAssignmentService(BaseServiceDBSession):
    async def create(self, data: ImageAssignmentCreateSchema) -> ImageAssignment:
        obj = ImageAssignment(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: str) -> ImageAssignment | None:
        result = await self.session.execute(
            select(ImageAssignment).where(ImageAssignment.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def update(
        self, obj_id: str, data: ImageAssignmentUpdateSchema
    ) -> ImageAssignment | None:
        result = await self.session.execute(
            select(ImageAssignment).where(ImageAssignment.id == obj_id)
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
            select(ImageAssignment).where(ImageAssignment.id == obj_id)
        )
        obj = result.scalar_one_or_none()
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def list(self, skip: int = 0, limit: int = 20) -> list[ImageAssignment]:
        result = await self.session.execute(
            select(ImageAssignment).offset(skip).limit(limit)
        )
        return result.scalars().all()
