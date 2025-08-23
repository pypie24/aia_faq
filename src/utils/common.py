import uuid
from uuid import UUID
import re
import itertools
from typing import Generator


def update_obj_from_dict(obj: object, data: dict) -> object:
    for key, val in data.items():
        if hasattr(obj, key):
            setattr(obj, key, val)
    return obj


def strtobool(value: str) -> bool:
    return value.lower() in ("true", "1", "t", "y", "yes")


def slugify(text: str) -> str:
    text = text.strip().lower()
    # replace slash with hyphen
    text = text.replace("/", "-")
    # replace spaces and underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)
    # Remove non-alphanumeric/hyphen characters
    text = re.sub(r"[^a-z0-9-]", "", text)
    # Remove double hyphens
    text = re.sub(r"-+", "-", text)
    # Strip leading/trailing hyphens
    text = text.strip("-")
    return text


def building_slug(text: str, texts: list[str]) -> str:
    if slugify(text) not in texts:
        texts.append(slugify(text))


def generate_batch_chunk(data: list, batch_size: int) -> Generator[list]:
    """Split a list into chunks of a specified size."""
    iter_data = iter(data)
    while chunk := list(itertools.islice(iter_data, batch_size)):
        yield chunk


def flatten_spec(spec: dict, parent_key: str = "") -> list[str]:
    """Recursively flattens a spec dictionary into readable sentences."""
    lines = []
    indent = "\t" if parent_key else ""
    for key, value in spec.items():
        if parent_key:
            full_key = f"{indent}{key}"
        else:
            full_key = key
        if isinstance(value, dict):
            lines.append(f"{full_key}:")
            # Increase indentation for nested dicts
            nested = flatten_spec(value, parent_key=full_key)
            lines.extend([f"{indent}{line}" for line in nested])
        elif isinstance(value, list):
            value_str = ", ".join(map(str, value))
            lines.append(f"{full_key}: {value_str}")
        else:
            lines.append(f"{full_key}: {value}")
    return lines


def generate_product_text(product_variant_model: object) -> str:
    brand_name = product_variant_model.product.product_line.brand.name
    category_name = product_variant_model.product.product_line.category.name
    tags = [tag.name for tag in product_variant_model.tags]
    flattened_specs = flatten_spec({
        "specs": product_variant_model.specs
    })
    product_variant_desc = f"""
        Product Line Description: {product_variant_model.product.product_line.description}
        Product Description: {product_variant_model.product.description}
        Prices: {product_variant_model.price}
        URL: {product_variant_model.url}
        Specs: {flattened_specs}
    """
    return {
        "id": str(product_variant_model.id),
        "brand": brand_name,
        "category": category_name,
        "price": product_variant_model.price,
        "tags": tags,
        "text": product_variant_desc
    }


def is_valid_uuid4(value: str | UUID) -> bool:
    value = str(value).strip()
    try:
        val = uuid.UUID(value, version=4)
    except ValueError:
        return False
    return val.version == 4 and str(val) == value.lower()
