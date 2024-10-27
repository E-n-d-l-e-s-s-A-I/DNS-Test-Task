from decimal import Decimal

from pydantic import BaseModel, field_validator

from app.utils.validators import price_validator, name_validator


class ProductSchemaBase(BaseModel):
    name: str
    price: Decimal

    @field_validator("price")
    def validate_price(cls, value):
        return price_validator(value)

    @field_validator("name")
    def validate_name(cls, value):
        return name_validator(value)


class ProductSchema(ProductSchemaBase):
    id: int


class ProductSchemaCreate(ProductSchemaBase):
    pass


class ProductSchemaUpdatePartial(ProductSchemaBase):
    name: str | None = None
    price: Decimal | None = None
