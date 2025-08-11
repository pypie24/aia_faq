from pydantic import BaseModel, model_validator


class BaseSchema(BaseModel):
    @model_validator(mode="before")
    def validate_data(cls, values):
        if isinstance(values, dict):
            for key, value in values.items():
                if isinstance(value, str):
                    values[key] = value.strip()
        return values
