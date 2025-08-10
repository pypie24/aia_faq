from sqlalchemy import JSON, UUID, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from src.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String, index=True, nullable=False, unique=True)
    description = Column(String, nullable=False)

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, description={self.description})>"


class Brand(BaseModel):
    __tablename__ = "brands"

    name = Column(String, index=True, nullable=False, unique=True)
    description = Column(String, nullable=False)

    def __repr__(self):
        return (
            f"<Brand(id={self.id}, name={self.name}, description={self.description})>"
        )


class Tag(BaseModel):
    __tablename__ = "tags"

    name = Column(String, index=True, nullable=False, unique=True)

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"


class ProductLines(BaseModel):
    __tablename__ = "product_lines"

    name = Column(String, index=True, nullable=False, unique=True)
    brand = Relationship("Brand", back_populates="product_lines", nullable=False)
    category = Relationship("Category", back_populates="product_lines", nullable=False)
    release_years = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    url = Column(String, nullable=False)
    slug = Column(String, nullable=False)

    def __repr__(self):
        return f"<ProductLine(id={self.id}, name={self.name}, description={self.description})>"


class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String, index=True, nullable=False, unique=True)
    product_line = Relationship(
        "ProductLines", back_populates="products", nullable=False
    )
    product_line_id = Column(UUID, ForeignKey("product_lines.id"), nullable=False)
    release_date = Column(Date, nullable=False)
    url = Column(String, nullable=False)
    slug = Column(String, nullable=False)


class ProductVariant(BaseModel):
    __tablename__ = "product_variants"

    product = Relationship("Product", back_populates="variants", nullable=False)
    product_id = Column(UUID, ForeignKey("products.id"), nullable=False)
    color = Column(String, nullable=False)
    price = Column(float, nullable=False)
    stock = Column(int, nullable=False)
    specs = Column(JSON, nullable=False)
    url = Column(String, nullable=False)
    slug = Column(String, nullable=False)

    def __repr__(self):
        return f"<ProductVariant(id={self.id}, product_id={self.product_id}, color={self.color}, price={self.price}, stock={self.stock}, specs={self.specs})>"


class Image(BaseModel):
    __tablename__ = "images"

    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    alt_text = Column(String, nullable=False)

    def __repr__(self):
        return f"<Image(id={self.id}, name={self.name}, url={self.url}, alt_text={self.alt_text})>"


class ImageAssignment(BaseModel):
    __tablename__ = "image_assignments"

    image_id = Column(UUID, ForeignKey("images.id"), nullable=False)
    entity_id = Column(UUID, nullable=False)
    entity_type = Column(String, nullable=False)
    sort_order = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<ImageAssignment(id={self.id}, image_id={self.image_id}, entity_id={self.entity_id}, entity_type={self.entity_type}, sort_order={self.sort_order})>"


class TagAssignment(BaseModel):
    __tablename__ = "tag_assignments"

    tag_id = Column(UUID, ForeignKey("tags.id"), nullable=False)
    entity_id = Column(UUID, nullable=False)
    entity_type = Column(String, nullable=False)
    sort_order = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<TagAssignment(id={self.id}, tag_id={self.tag_id}, entity_id={self.entity_id}, entity_type={self.entity_type}, sort_order={self.sort_order})>"
