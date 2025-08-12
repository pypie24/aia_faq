from uuid import UUID
from sqlalchemy.future import select

from src.models.product_models import (
    Category,
    ProductLines,
    Product,
    ProductVariant,
)
from src.schemas.product_schemas import (
    ProductLinesCreateSchema,
    ProductLinesUpdateSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductVariantCreateSchema,
    ProductVariantUpdateSchema,
)
from src.models.product_models import Brand
from src.services.base_services import BaseServiceDBSession
from src.utils.common import update_obj_from_dict


class ProductLinesService(BaseServiceDBSession):
    async def _generate_slug(self, name: str, category_id: UUID, brand_id: UUID) -> str:
        slug = []
        category = await self.session.execute(
            select(Category).where(Category.id == category_id)
        )
        category = category.scalar_one_or_none()
        if category:
            slug.append(category.name.lower().replace(" ", "-"))

        brand = await self.session.execute(select(Brand).where(Brand.id == brand_id))
        brand = brand.scalar_one_or_none()
        if brand:
            slug.append(brand.name.lower().replace(" ", "-"))

        slug.append(name.lower().replace(" ", "-"))

        return "-".join(slug)

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


class ProductService(BaseServiceDBSession):
    async def _generate_slug(self, name: str, product_line_id: UUID) -> str:
        slug = []
        product_line = await self.session.execute(
            select(ProductLines).where(ProductLines.id == product_line_id)
        )
        product_line = product_line.scalar_one_or_none()
        if product_line:
            slug.append(product_line.name.lower().replace(" ", "-"))

        slug.append(name.lower().replace(" ", "-"))

        return "-".join(slug)

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


class ProductVariantService(BaseServiceDBSession):
    async def _generate_slug(self, name: str, product_id: UUID) -> str:
        slug = []
        product = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = product.scalar_one_or_none()
        if product:
            slug.append(product.name.lower().replace(" ", "-"))

        slug.append(name.lower().replace(" ", "-"))

        return "-".join(slug)

    async def create(self, product_id: UUID, data: ProductVariantCreateSchema) -> ProductVariant:
        obj = ProductVariant(**data.model_dump())
        obj.product_id = product_id
        obj.slug = await self._generate_slug(obj.name, product_id)
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

    async def list(self, skip: int = 0, limit: int = 20) -> list[ProductVariant]:
        result = await self.session.execute(
            select(ProductVariant).offset(skip).limit(limit)
        )
        return result.scalars().all()
