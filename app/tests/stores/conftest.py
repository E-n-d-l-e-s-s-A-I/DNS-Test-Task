import pytest

from app.api.stores.models import Store
from app.api.stores.schemas import StoreSchemaCreate, StoreSchemaUpdatePartial
from app.db.test_data.test_data_scripts import open_json


@pytest.fixture()
async def stores():
    return open_json(Store.__tablename__)


@pytest.fixture()
async def store_add_data() -> StoreSchemaCreate:
    return StoreSchemaCreate(
        name="В датасете такого не должно быть",
        city_id=1,
    )


@pytest.fixture()
async def store_add_data_with_not_existsting_city() -> StoreSchemaCreate:
    return StoreSchemaCreate(
        name="В датасете такого не должно быть",
        city_id=-1,
    )


@pytest.fixture()
async def store_update_data() -> StoreSchemaUpdatePartial:
    return StoreSchemaCreate(
        name="В датасете такого не должно быть",
        city_id=1,
    )
