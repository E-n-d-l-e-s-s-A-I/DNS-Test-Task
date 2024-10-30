import pytest
from fastapi import HTTPException

from app.api.stores.models import Store
from app.api.stores.repository import StoreRepository
from app.utils.exceptions import DBIntegrityException


async def test_get_objects(session, stores):
    stores_models: list[Store] = await StoreRepository.get_objects(
        session=session)

    stores_from_rep = [store_model.to_dict() for store_model in stores_models]
    assert stores_from_rep == stores


async def test_get_object(session, stores):
    store_model: Store = await StoreRepository.get_object(
        session=session, object_id=1)
    store_from_rep = store_model.to_dict()
    assert store_from_rep in stores


async def test_create_object(session, store_add_data):
    store_id = await StoreRepository.create_object(
        session=session,
        data=store_add_data,
    )

    assert isinstance(store_id, int)

    store: Store = await session.get(Store, store_id)

    assert store.name == store_add_data.name
    assert store.city_id == store_add_data.city_id


async def test_dont_create_object_with_already_exists_name(
    session, store_add_data
):
    await StoreRepository.create_object(
        session=session,
        data=store_add_data,
    )

    with pytest.raises(HTTPException) as e:
        await StoreRepository.create_object(
            session=session,
            data=store_add_data,
        )
        assert isinstance(e, DBIntegrityException)


async def test_dont_create_object_with_not_existsting_city_id(
    session, store_add_data_with_not_existsting_city
):
    with pytest.raises(HTTPException) as e:
        await StoreRepository.create_object(
            session=session,
            data=store_add_data_with_not_existsting_city,
        )
        assert isinstance(e, DBIntegrityException)


async def test_update_partial_object(session, store_add_data):
    store_id = 1
    await StoreRepository.update_partial_object(
        session=session,
        object_id=store_id,
        data=store_add_data,
    )

    store: Store = await session.get(Store, store_id)

    assert store.name == store_add_data.name
    assert store.city_id == store_add_data.city_id


async def test_dont_update_partial_object_to_already_exists_name(
    session, store_update_data
):

    await StoreRepository.update_partial_object(
        session=session,
        object_id=1,
        data=store_update_data,
    )

    with pytest.raises(HTTPException) as e:
        await StoreRepository.update_partial_object(
            session=session,
            object_id=2,
            data=store_update_data,
        )
        assert isinstance(e, DBIntegrityException)


async def test_dont_update_partial_object_to_not_exists_city_id(
    session, store_add_data_with_not_existsting_city
):

    with pytest.raises(HTTPException) as e:
        await StoreRepository.update_partial_object(
            session=session,
            object_id=2,
            data=store_add_data_with_not_existsting_city,
        )
        assert isinstance(e, DBIntegrityException)


async def test_delete_object(session, stores):
    store_id = 1

    store_model: Store = await StoreRepository.delete_object(
        session=session,
        object_id=store_id,
        )
    store_from_rep = store_model.to_dict()

    assert store_from_rep in stores
    assert await session.get(Store, store_id) is None


async def test_dont_delete_not_existing_object(session):
    store_id = 1
    await StoreRepository.delete_object(
        session=session,
        object_id=store_id,
    )
    with pytest.raises(HTTPException) as e:
        await StoreRepository.delete_object(
            session=session,
            object_id=store_id,
        )
        assert isinstance(e, DBIntegrityException)
