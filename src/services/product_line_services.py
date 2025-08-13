from uuid import UUID
from sqlalchemy.future import select

from src.models.product_models import (
    Category,
    ProductLines,
)
from src.schemas.product_line_schemas import (
    ProductLinesCreateSchema,
    ProductLinesUpdateSchema,
)
from src.models.product_models import Brand
from src.services.base_services import BaseServiceDBSession
from src.utils.common import building_slug, update_obj_from_dict


class ProductLinesService(BaseServiceDBSession):
    async def _generate_slug(self, name: str, category_id: UUID, brand_id: UUID) -> str:
        slugs = []
        category = await self.session.execute(
            select(Category).where(Category.id == category_id)
        )
        category = category.scalar_one_or_none()
        if category:
            building_slug(category.name, slugs)

        brand = await self.session.execute(select(Brand).where(Brand.id == brand_id))
        brand = brand.scalar_one_or_none()
        if brand:
            building_slug(brand.name, slugs)

        building_slug(brand.name, slugs)

        return "-".join(slugs)

    async def create(self, data: ProductLinesCreateSchema) -> ProductLines:
        data.slug = await self._generate_slug(
            data.name, data.category_id, data.brand_id
        )
        obj = ProductLines(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: str) -> ProductLines | None:
        result = await self.session.execute(
            select(ProductLines).where(ProductLines.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def update(
        self, obj_id: str, data: ProductLinesUpdateSchema
    ) -> ProductLines | None:
        result = await self.session.execute(
            select(ProductLines).where(ProductLines.id == obj_id)
        )
        obj = result.scalar_one_or_none()
        if obj is None:
            return None
        update_obj_from_dict(obj, data.model_dump(exclude_unset=True))
        obj.slug = await self._generate_slug(obj.name, obj.category_id, obj.brand_id)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: str) -> bool:
        result = await self.session.execute(
            select(ProductLines).where(ProductLines.id == obj_id)
        )
        obj = result.scalar_one_or_none()
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def list(
        self, category_id: UUID, brand_id: UUID, skip: int = 0, limit: int = 20
    ) -> list[ProductLines]:
        query = select(ProductLines).offset(skip).limit(limit)
        if brand_id:
            query = query.where(ProductLines.brand_id == brand_id)
        if category_id:
            query = query.where(ProductLines.category_id == category_id)
        result = await self.session.execute(query)
        return result.scalars().all()

