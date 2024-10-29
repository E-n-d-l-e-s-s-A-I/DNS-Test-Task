import pytest

from app.api.cities.models import City
from app.api.cities.schemas import CitySchemaCreate, CitySchemaUpdatePartial
from app.db.test_data.test_data_scripts import open_json


@pytest.fixture()
async def cities():
    return open_json(City.__tablename__)


@pytest.fixture()
async def city_add_data() -> CitySchemaCreate:
    return CitySchemaCreate(
        name="В датасете такого не должно быть",
    )


@pytest.fixture()
async def city_update_data() -> CitySchemaUpdatePartial:
    return CitySchemaUpdatePartial(
        name="В датасете такого не должно быть",
    )
