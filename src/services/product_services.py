from uuid import UUID
from sqlalchemy.future import select

from src.models.product_models import (
    ProductLines,
    Product,
)
from src.schemas.product_schemas import (
    ProductCreateSchema,
    ProductUpdateSchema,
)
from src.models.product_models import Brand
from src.services.base_services import BaseServiceDBSession
from src.utils.common import building_slug, update_obj_from_dict



class ProductService(BaseServiceDBSession):
    async def _generate_slug(self, name: str, product_line_id: UUID) -> str:
        slugs = []
        product_line = await self.session.execute(
            select(ProductLines).where(ProductLines.id == product_line_id)
        )
        product_line = product_line.scalar_one_or_none()
        if product_line:
            building_slug(product_line.name, slugs)

        building_slug(name, slugs)

        return "-".join(slugs)

    async def create(self, data: ProductCreateSchema) -> Product:
        obj = Product(**data.model_dump())
        obj.slug = await self._generate_slug(obj.name, obj.product_line_id)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: str) -> Product | None:
        result = await self.session.execute(select(Product).where(Product.id == obj_id))
        return result.scalar_one_or_none()

    async def update(self, obj_id: str, data: ProductUpdateSchema) -> Product | None:
        result = await self.session.execute(select(Product).where(Product.id == obj_id))
        obj = result.scalar_one_or_none()
        if obj is None:
            return None
        update_obj_from_dict(obj, data.model_dump(exclude_unset=True))
        obj.slug = await self._generate_slug(obj.name, obj.product_line_id)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: str) -> bool:
        result = await self.session.execute(select(Product).where(Product.id == obj_id))
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
        product_line_id: UUID = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Product]:
        query = select(Product).offset(skip).limit(limit)
        if brand_id:
            query = query.where(Product.product_line.brand_id == brand_id)
        if category_id:
            query = query.where(Product.product_line.category_id == category_id)
        if product_line_id:
            query = query.where(Product.product_line_id == product_line_id)
        result = await self.session.execute(query)
        return result.scalars().all()
