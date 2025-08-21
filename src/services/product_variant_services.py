from uuid import UUID, uuid4
from typing import Any, List
import logging

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.models.product_models import (
    Product,
    ProductVariant,
    Tag,
    Image
)
from src.schemas.product_variant_schemas import (
    ProductVariantCreateSchema,
    ProductVariantUpdateSchema,
    ImageUpdateSchema
)

from src.services.base_services import BaseServiceDBSession
from src.utils.common import building_slug, update_obj_from_dict, is_valid_uuid4
from src.tasks.embedding_tasks import enqueue_text
from src.tools.client import minio_client
from src.config import settings

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class ProductVariantService(BaseServiceDBSession):
    async def _generate_slug(self, name: str, product_id: UUID) -> str:
        slugs = []
        product = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = product.scalar_one_or_none()
        if product:
            building_slug(product.name, slugs)

        building_slug(name, slugs)

        return "-".join(slugs)

    async def create(self, data: ProductVariantCreateSchema) -> ProductVariant:
        obj = ProductVariant(**data.model_dump())
        obj.slug = await self._generate_slug(obj.name)
        obj.url = f"/product-variants/{obj.slug}"
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: str) -> ProductVariant | None:
        if is_valid_uuid4(obj_id):
            result = await self.session.execute(
                select(ProductVariant).where(ProductVariant.id == obj_id).options(
                    selectinload(ProductVariant.images)
                )
            )
        else:
            result = await self.session.execute(
                select(ProductVariant).where(ProductVariant.slug == obj_id).options(
                    selectinload(ProductVariant.images)
                )
            )
        return result.scalar_one_or_none()

    async def update(
        self, obj_id: str, data: ProductVariantUpdateSchema
    ) -> ProductVariant | None:
        result = await self.session.execute(
            select(ProductVariant).where(ProductVariant.id == obj_id)
        )
        obj = result.scalar_one_or_none()
        if obj is None:
            return None
        update_obj_from_dict(obj, data.model_dump(exclude_unset=True))
        obj.slug = await self._generate_slug(obj.name, obj.product_id)
        obj.url = f"/product-variants/{obj.slug}"
        await self.session.commit()
        await self.session.refresh(obj)

        variant_data = await self.generate_product_data(obj)
        # add to queue flower queue
        enqueue_text(variant_data)
        return obj

    async def delete(self, obj_id: str) -> bool:
        result = await self.session.execute(
            select(ProductVariant).where(ProductVariant.id == obj_id)
        )
        obj = result.scalar_one_or_none()
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def list(
            self,
            brand_id: UUID = None,
            category_id: UUID = None,
            product_id: UUID = None,
            min_price: float = None,
            max_price: float = None,
            tags: list[UUID] = None,
            skip: int = 0,
            limit: int = 20
        ) -> list[ProductVariant]:
        query = select(ProductVariant)
        if brand_id:
            query = query.where(ProductVariant.product.product_line.brand_id == brand_id)
        if category_id:
            query = query.where(ProductVariant.product.product_line.category_id == category_id)
        if product_id:
            query = query.where(ProductVariant.product_id == product_id)
        if min_price is not None:
            query = query.where(ProductVariant.price >= min_price)
        if max_price is not None:
            query = query.where(ProductVariant.price <= max_price)
        if tags:
            query = query.where(ProductVariant.tags.any(Tag.id.in_(tags)))
        result = await self.session.execute(
            query.offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def upload_images(self, variant_id: str, files: List[Any]) -> List[str]:
        variant = await self.get(variant_id)
        if not variant:
            raise HTTPException(status_code=404, detail="ProductVariant not found")

        images = []
        for file in files:
            file_name = "variants/" + variant.slug + f"_{uuid4()}.jpg"
            minio_client.put_object(
                settings.FILE_SERVER_BUCKET_NAME,
                file_name,
                file.file,
                file.size
            )
            public_url = f"http://127.0.0.1:9000/{settings.FILE_SERVER_BUCKET_NAME}/{file_name}"
            image = Image(url=public_url, product_variant_id=variant.id)
            self.session.add(image)
            images.append(image)

        await self.session.commit()
        await self.session.refresh(variant, ["images"])
        return variant.images

    async def update_image(self, variant_id: str, image_id: str, data: ImageUpdateSchema) -> Image | None:
        result = await self.session.execute(
            select(Image).where(Image.id == image_id, Image.product_variant_id == variant_id)
        )
        image = result.scalar_one_or_none()
        if image is None:
            return None
        update_obj_from_dict(image, data.model_dump(exclude_unset=True))
        await self.session.commit()
        await self.session.refresh(image)
        return image
    
    async def delete_image(self, variant_id: str, image_id: str) -> bool:
        result = await self.session.execute(
            select(Image).where(Image.id == image_id, Image.product_variant_id == variant_id)
        )
        image = result.scalar_one_or_none()
        if image is None:
            return False
        
        await self.session.delete(image)
        await self.session.commit()
        image_url = image.url.split("/")[-1]
        file_name = f"variants/{image_url}"
        log.info(f"Deleting image from MinIO: {file_name}")
        minio_client.remove_object(
            settings.FILE_SERVER_BUCKET_NAME,
            file_name
        )
        return True
