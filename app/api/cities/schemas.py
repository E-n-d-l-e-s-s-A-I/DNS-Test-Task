from pydantic import BaseModel, field_validator

from app.utils.validators import name_validator


class CitySchemaBase(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, value):
        return name_validator(value)


class CitySchema(CitySchemaBase):
    id: int


class CitySchemaCreate(CitySchemaBase):
    pass


class CitySchemaUpdatePartial(CitySchemaBase):
    name: str | None = None
