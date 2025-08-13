import re


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