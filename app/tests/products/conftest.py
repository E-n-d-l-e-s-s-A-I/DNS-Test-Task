import pytest

from app.api.products.models import Product
from app.api.products.schemas import (
    ProductSchemaCreate, ProductSchemaUpdatePartial
)
from app.db.test_data.test_data_scripts import open_json


@pytest.fixture()
async def products():
    return open_json(Product.__tablename__)


@pytest.fixture()
async def product_add_data() -> ProductSchemaCreate:
    return ProductSchemaCreate(
        name="В датасете такого не должно быть",
        price=1,
    )


@pytest.fixture()
async def product_update_data() -> ProductSchemaUpdatePartial:
    return ProductSchemaUpdatePartial(
        name="В датасете такого не должно быть",
        price=1,
    )
