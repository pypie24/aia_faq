from fastapi import UploadFile
from sqlalchemy.future import select

from src.models.product_models import Image
from src.schemas.image_schema import (
    ImageCreateSchema,
    ImageUpdateSchema,
)
from src.services.base_services import BaseServiceDBSession
from src.services.file_services import image_uploader
from src.utils.common import update_obj_from_dict


class ImageService(BaseServiceDBSession):
    def __init__(self):
        super().__init__()
        self.image_uploader = image_uploader

    async def create(self, data: ImageCreateSchema, file: UploadFile) -> Image:
        image_url = self.image_uploader.upload_file(file, data.name)
        obj = Image(**data.model_dump(), url=image_url)
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
