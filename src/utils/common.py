import json
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
    for key, value in spec.items():
        full_key = f"{parent_key} {key}".strip().replace("_", " ").capitalize()
        if isinstance(value, dict):
            lines.extend(flatten_spec(value, full_key))
        elif isinstance(value, list):
            if value and isinstance(value[0], dict):
                for idx, item in enumerate(value, 1):
                    lines.extend(flatten_spec(item, f"{full_key} {idx}"))
            else:
                lines.append(f"{full_key}: {', '.join(map(str, value))}")
        else:
            lines.append(f"{full_key}: {value}")
    return lines


def generate_product_text(product_variant_model: object) -> str:
    brand_name = product_variant_model.product.product_line.brand.name
    category_name = product_variant_model.product.product_line.category.name
    product_variant_desc = product_variant_model.product.description or product_variant_model.product.product_line.description or ""
    tags = [tag.name for tag in product_variant_model.tags]
    specs = json.loads(product_variant_model.specs)
    flattened_specs = flatten_spec(specs)
    return {
        "id": product_variant_model.id,
        "brand": brand_name,
        "category": category_name,
        "description": product_variant_desc,
        "price": product_variant_model.price,
        "tags": tags,
        "specs": flattened_specs
    }
