import pytest

from app.api.sales.models import Sale, SaleProducts
from app.api.sales.schemas import (
    SaleSchemaCreate,
    SaleProductSchemaCreate,
    SaleSchemaUpdatePartial,
    SaleProductSchemaUpdatePartial
)
from app.db.test_data.test_data_scripts import open_json


@pytest.fixture()
async def sales():
    return open_json(Sale.__tablename__)


@pytest.fixture()
async def sales_products():
    return open_json(SaleProducts.__tablename__)


@pytest.fixture()
async def sale_add_data() -> SaleSchemaCreate:
    return SaleSchemaCreate(
        store_id=1,
        products=[
            SaleProductSchemaCreate(quantity=1, product_id=1),
        ]
    )


@pytest.fixture()
async def sale_add_data_with_not_existsting_city() -> SaleSchemaCreate:
    return SaleSchemaCreate(
        store_id=-1,
        products=[
            SaleProductSchemaCreate(quantity=1, product_id=1),
        ]
    )


@pytest.fixture()
async def sale_add_data_with_not_existsting_product() -> SaleSchemaCreate:
    return SaleSchemaCreate(
        store_id=1,
        products=[
            SaleProductSchemaCreate(quantity=1, product_id=-1),
        ]
    )


@pytest.fixture()
async def sale_update_data() -> SaleSchemaUpdatePartial:
    return SaleSchemaUpdatePartial(
        store_id=1
    )


@pytest.fixture()
async def sale_update_data_with_not_existsting_store(
) -> SaleSchemaUpdatePartial:
    return SaleSchemaUpdatePartial(
        store_id=-1
    )


@pytest.fixture()
async def product_add_data(
) -> SaleProductSchemaCreate:
    return SaleProductSchemaCreate(
        quantity=1,
        product_id=2,
    )


@pytest.fixture()
async def product_add_data_with_not_existsting_product(
) -> SaleProductSchemaCreate:
    return SaleProductSchemaCreate(
        quantity=1,
        product_id=-1,
    )


@pytest.fixture()
async def product_update_data(
) -> SaleProductSchemaUpdatePartial:
    return SaleProductSchemaUpdatePartial(
        quantity=121,
    )
