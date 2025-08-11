from fastapi.params import Depends

from src.services.product_services import (
    ProductLinesService,
    ProductService,
    ProductVariantService,
)
from src.services.category_services import CategoryService
from src.services.brand_services import BrandService
from src.services.tag_services import TagService
from src.services.image_services import ImageService
from src.db import get_db


def get_brand_service(session=Depends(get_db)):
    return BrandService(session)


def get_category_service(session=Depends(get_db)):
    return CategoryService(session)


def get_product_lines_service(session=Depends(get_db)):
    return ProductLinesService(session)


def get_product_service(session=Depends(get_db)):
    return ProductService(session)


def get_product_variant_service(session=Depends(get_db)):
    return ProductVariantService(session)


def get_tag_service(session=Depends(get_db)):
    return TagService(session)


def get_image_service(session=Depends(get_db)):
    return ImageService(session)
