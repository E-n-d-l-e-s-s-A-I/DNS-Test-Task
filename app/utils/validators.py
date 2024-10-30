"""Module defines validators for pydantic schemas."""

from decimal import Decimal

from app.config import settings


def name_validator(name: str) -> str:
    if len(name) > settings.DB_STR_MAX_LEN:
        raise ValueError(
            f"name length must not  be more than "
            f"{settings.DB_STR_MAX_LEN} characters"
        )
    return name


def price_validator(price: Decimal) -> Decimal:
    _, _, exponent = price.as_tuple()
    if abs(exponent) > 2:
        raise ValueError("price must not contain more than two decimal places")
    if price <= 0:
        raise ValueError("price must be greater greater  0")
    return price


def quantity_validator(quantity: int) -> str:
    if quantity <= 0:
        raise ValueError("quantity must be more 0")
    return quantity


def ids_validator(ids: list[int]) -> str:
    if len(set(ids)) != len(ids):
        raise ValueError("all ids in list must be uniqe")
    return ids
