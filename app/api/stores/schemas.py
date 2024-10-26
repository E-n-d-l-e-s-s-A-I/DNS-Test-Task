from pydantic import BaseModel, field_validator

from app.utils.validators import name_validator


class StoreSchemaBase(BaseModel):
    name: str
    city_id: int

    @field_validator("name")
    def validate_name(cls, value):
        return name_validator(value)


class StoreSchema(StoreSchemaBase):
    id: int


class StoreSchemaCreate(StoreSchemaBase):
    pass


class StoreSchemaUpdatePartial(StoreSchemaBase):
    name: str | None = None
    city_id: int | None = None
