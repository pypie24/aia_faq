from sqlalchemy.future import select

from src.models.product_models import (
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
from src.services.base_services import BaseServiceDBSession
from src.utils.common import update_obj_from_dict


class ProductLinesService(BaseServiceDBSession):
    async def create(self, data: ProductLinesCreateSchema) -> ProductLines:
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

    async def list(self, skip: int = 0, limit: int = 20) -> list[ProductLines]:
        result = await self.session.execute(
            select(ProductLines).offset(skip).limit(limit)
        )
        return result.scalars().all()


class ProductService(BaseServiceDBSession):
    async def create(self, data: ProductCreateSchema) -> Product:
        obj = Product(**data.model_dump())
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

    async def list(self, skip: int = 0, limit: int = 20) -> list[Product]:
        result = await self.session.execute(select(Product).offset(skip).limit(limit))
        return result.scalars().all()


class ProductVariantService(BaseServiceDBSession):
    async def create(self, data: ProductVariantCreateSchema) -> ProductVariant:
        obj = ProductVariant(**data.model_dump())
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
