from sqlalchemy import (
    JSON,
    UUID,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Float,
)
from sqlalchemy.orm import Relationship
from src.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String, index=True, nullable=False, unique=True)
    product_lines = Relationship("ProductLines", back_populates="category")
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, description={self.description})>"


class Brand(BaseModel):
    __tablename__ = "brands"

    name = Column(String, index=True, nullable=False, unique=True)
    product_lines = Relationship("ProductLines", back_populates="brand")
    description = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<Brand(id={self.id}, name={self.name}, description={self.description})>"
        )


class ProductLines(BaseModel):
    __tablename__ = "product_lines"

    name = Column(String, index=True, nullable=False, unique=True)
    brand = Relationship("Brand", back_populates="product_lines")
    brand_id = Column(UUID, ForeignKey("brands.id"), nullable=False)
    category = Relationship("Category", back_populates="product_lines")
    category_id = Column(UUID, ForeignKey("categories.id"), nullable=False)
    products = Relationship("Product", back_populates="product_line")
    release_years = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    url = Column(String, nullable=True)
    slug = Column(String, nullable=True)

    def __repr__(self):
        return f"<ProductLine(id={self.id}, name={self.name}, description={self.description})>"


class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String, index=True, nullable=False, unique=True)
    product_line = Relationship("ProductLines", back_populates="products")
    product_line_id = Column(UUID, ForeignKey("product_lines.id"), nullable=False)
    sku = Column(String, nullable=True, unique=True)
    variants = Relationship("ProductVariant", back_populates="product")
    release_date = Column(Date, nullable=True)
    url = Column(String, nullable=True)
    slug = Column(String, nullable=True)


class ProductVariant(BaseModel):
    __tablename__ = "product_variants"

    product = Relationship("Product", back_populates="variants")
    product_id = Column(UUID, ForeignKey("products.id"), nullable=False)
    name = Column(String, nullable=False)
    variant_sku = Column(String, nullable=True, unique=True)
    price = Column(Float, nullable=True)
    stock = Column(Integer, nullable=True)
    specs = Column(JSON, nullable=True)
    url = Column(String, nullable=True)
    slug = Column(String, nullable=True)
    tags = Relationship(
        "Tag", secondary="product_variant_tags", back_populates="variants"
    )

    def __repr__(self):
        return (
            f"<ProductVariant(id={self.id}, product_id={self.product_id}, "
            f"name={self.name}, color={self.color}, price={self.price}, stock={self.stock})>"
        )


class Tag(BaseModel):
    __tablename__ = "tags"

    name = Column(String(255), unique=True, nullable=False)
    variants = Relationship(
        "ProductVariant", secondary="product_variant_tags", back_populates="tags"
    )


class ProductVariantTag(BaseModel):
    __tablename__ = "product_variant_tags"

    variant_id = Column(
        UUID, ForeignKey("product_variants.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id = Column(UUID, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
