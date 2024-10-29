import pytest
from fastapi import HTTPException

from app.api.products.models import Product
from app.api.products.repository import ProductRepository
from app.utils.exceptions import DBIntegrityException


async def test_get_objects(session, products):
    products_models = await ProductRepository.get_objects(session=session)

    products_from_rep = [
        product_model.to_dict() for product_model in products_models
    ]
    assert products_from_rep == products


async def test_get_object(session, products):
    product_model = await ProductRepository.get_object(
        session=session, object_id=1
    )
    product_from_rep = product_model.to_dict()
    assert product_from_rep in products


async def test_create_object(session, product_add_data):
    product_id = await ProductRepository.create_object(
        session=session,
        data=product_add_data,
    )

    assert isinstance(product_id, int)


async def test_dont_create_object_with_already_exists_name(
    session, product_add_data
):
    await ProductRepository.create_object(
        session=session,
        data=product_add_data,
    )

    with pytest.raises(HTTPException) as e:
        await ProductRepository.create_object(
            session=session,
            data=product_add_data,
        )
        assert isinstance(e, DBIntegrityException)


async def test_update_partial_object(session, product_update_data):
    product_model: Product = await ProductRepository.update_partial_object(
        session=session,
        object_id=1,
        data=product_update_data,
    )
    assert product_update_data.name == product_model.name
    assert product_update_data.price == product_model.price


async def test_dont_update_partial_object_to_already_exists_name(
    session, product_update_data
):
    await ProductRepository.update_partial_object(
        session=session,
        object_id=1,
        data=product_update_data,
        )

    with pytest.raises(HTTPException) as e:
        await ProductRepository.update_partial_object(
            session=session,
            object_id=2,
            data=product_update_data,
            )
        assert isinstance(e, DBIntegrityException)


async def test_delete_object(session, products):
    product_id = 1

    product_model = await ProductRepository.delete_object(
        session=session,
        object_id=product_id,
        )
    product_from_rep = product_model.to_dict()

    assert product_from_rep in products
    assert await session.get(Product, product_id) is None


async def test_dont_delete_not_existing_object(session):
    product_id = 1
    await ProductRepository.delete_object(
        session=session,
        object_id=product_id,
    )
    with pytest.raises(HTTPException) as e:
        await ProductRepository.delete_object(
            session=session,
            object_id=product_id,
        )
        assert isinstance(e, DBIntegrityException)
