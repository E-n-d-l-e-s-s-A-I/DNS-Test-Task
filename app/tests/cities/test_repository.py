import pytest
from fastapi import HTTPException

from app.api.cities.models import City
from app.api.cities.repository import CityRepository
from app.utils.exceptions import DBIntegrityException


async def test_get_objects(session, cities):
    cities_models: list[City] = await CityRepository.get_objects(
        session=session)

    cites_from_rep = [
        city_model.to_dict() for city_model in cities_models
        ]
    assert cites_from_rep == cities


async def test_get_object(session, cities):
    city_model: City = await CityRepository.get_object(
        session=session, object_id=1
    )
    city_from_rep = city_model.to_dict()
    assert city_from_rep in cities


async def test_create_object(session, city_add_data):
    city_id = await CityRepository.create_object(
        session=session,
        data=city_add_data,
        )

    assert isinstance(city_id, int)

    city: City = await session.get(City, city_id)
    assert city.name == city_add_data.name


async def test_dont_create_object_with_already_exists_name(
    session, city_add_data
):
    await CityRepository.create_object(
        session=session,
        data=city_add_data,
        )

    with pytest.raises(HTTPException) as e:
        await CityRepository.create_object(
            session=session,
            data=city_add_data,
            )
        assert isinstance(e, DBIntegrityException)


async def test_update_partial_object(session, city_update_data):
    city_id = 1
    await CityRepository.update_partial_object(
        session=session,
        object_id=city_id,
        data=city_update_data,
        )
    city: City = await session.get(City, city_id)
    assert city.name == city_update_data.name


async def test_dont_update_partial_object_to_already_exists_name(
    session, city_update_data
):
    await CityRepository.update_partial_object(
        session=session,
        object_id=1,
        data=city_update_data,
        )

    with pytest.raises(HTTPException) as e:
        await CityRepository.update_partial_object(
            session=session,
            object_id=2,
            data=city_update_data,
            )
        assert isinstance(e, DBIntegrityException)


async def test_delete_object(session, cities):
    city_id = 1

    city_model: City = await CityRepository.delete_object(
        session=session,
        object_id=city_id,
        )
    city_from_rep = city_model.to_dict()

    assert city_from_rep in cities
    assert await session.get(City, city_id) is None


async def test_dont_delete_not_existing_object(session):
    city_id = 1
    await CityRepository.delete_object(
        session=session,
        object_id=city_id,
    )
    with pytest.raises(HTTPException) as e:
        await CityRepository.delete_object(
            session=session,
            object_id=city_id,
        )
        assert isinstance(e, DBIntegrityException)
