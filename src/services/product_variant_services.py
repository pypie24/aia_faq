from uuid import UUID
from sqlalchemy.future import select

from src.models.product_models import (
    Product,
    ProductVariant,
    Tag,
)
from src.schemas.product_variant_schemas import (
    ProductVariantCreateSchema,
    ProductVariantUpdateSchema,
)

from src.services.base_services import BaseServiceDBSession
from src.utils.common import building_slug, update_obj_from_dict


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
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: str) -> ProductVariant | None:
        result = await self.session.execute(
            select(ProductVariant).where(ProductVariant.id == obj_id)
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
        await self.session.commit()
        await self.session.refresh(obj)
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
