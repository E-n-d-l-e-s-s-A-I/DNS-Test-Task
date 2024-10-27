from decimal import Decimal
from pydantic import BaseModel, field_validator

# from app.api.products.schemas import ProductSchema
from app.utils.validators import (
    price_validator,
    quantity_validator,
    ids_validator,
)


class SaleProductSchemaBase(BaseModel):
    quantity: int

    @field_validator("quantity")
    def validate_name(cls, value):
        return quantity_validator(value)


class SaleProductSchemaUpdatePartial(SaleProductSchemaBase):
    quantity: int | None = None


class SaleProductSchemaCreate(SaleProductSchemaBase):
    product_id: int


class SaleProductSchema(SaleProductSchemaBase):
    product_id: int
    unit_price: Decimal

    @field_validator("unit_price")
    def validate_price(cls, value):
        return price_validator(value)


class ProductSchemaWithUnitPrice(SaleProductSchemaBase):
    id: int
    name: str
    unit_price: Decimal

    @field_validator("unit_price")
    def validate_price(cls, value):
        return price_validator(value)


class SaleSchemaBase(BaseModel):
    store_id: int


class SaleSchema(SaleSchemaBase):
    id: int
    products: list[SaleProductSchema]
    total_amount: Decimal
    total_quantity: int


class SaleSchemaDetail(SaleSchemaBase):
    id: int
    products_details: list[ProductSchemaWithUnitPrice]
    total_amount: Decimal
    total_quantity: int


class SaleSchemaCreate(SaleSchemaBase):
    products: list[SaleProductSchemaCreate]

    @property
    def produsts_ids(self) -> list[int]:
        return [product.product_id for product in self.products]

    @field_validator("products")
    def validate_name(cls, value):
        ids_validator([product.product_id for product in value])
        return value


class SaleSchemaUpdatePartial(SaleSchemaBase):
    store_id: int | None = None
