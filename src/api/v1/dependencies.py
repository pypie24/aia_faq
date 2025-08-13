from fastapi.params import Depends

from src.services.product_line_services import ProductLinesService
from src.services.product_variant_services import ProductVariantService
from src.services.product_services import ProductService
from src.services.category_services import CategoryService
from src.services.brand_services import BrandService
from src.services.tag_services import TagService
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
