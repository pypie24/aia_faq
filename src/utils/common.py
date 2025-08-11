import re
import uuid


def update_obj_from_dict(obj: object, data: dict) -> object:
    for key, val in data.items():
        if hasattr(obj, key):
            setattr(obj, key, val)
    return obj


def strtobool(value: str) -> bool:
    return value.lower() in ("true", "1", "t", "y", "yes")


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    # Remove non-alphanumeric/hyphen characters
    text = re.sub(r"[^a-z0-9-]", "", text)
    # Remove double hyphens
    text = re.sub(r"-+", "-", text)
    # Strip leading/trailing hyphens
    text = text.strip("-")
    return text


def slugify_unique(text: str) -> str:
    base_slug = slugify(text)
    unique_part = str(uuid.uuid4())[:8]  # short random part
    return f"{base_slug}-{unique_part}"
