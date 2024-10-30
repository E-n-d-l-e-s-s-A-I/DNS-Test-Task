from datetime import timedelta, datetime
from typing import Any

import pytest
from fastapi import HTTPException
from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload, joinedload

from app.api.products.repository import ProductRepository
from app.api.products.schemas import ProductSchemaUpdatePartial
from app.api.sales.models import Sale, SaleProducts
from app.api.sales.repository import SaleRepository
from app.utils.exceptions import DBIntegrityException


async def test_get_objects(session, sales):
    sales_models: list[Sale] = await SaleRepository.get_objects(
        session=session
    )

    sales_from_rep = [sale_model.to_dict() for sale_model in sales_models]
    assert sales_from_rep == sales


async def test_get_object(session, sales):
    sale_model: Sale = await SaleRepository.get_object(
        session=session, object_id=1
    )
    sale_from_rep = sale_model.to_dict()
    assert sale_from_rep in sales


async def test_create_object(session, sale_add_data):
    sale_id = await SaleRepository.create_object(
        session=session,
        data=sale_add_data,
    )

    assert isinstance(sale_id, int)

    query = select(Sale).filter_by(id=sale_id).options(
        selectinload(Sale.products), joinedload(Sale.store)
    )
    result: Result = await session.execute(query)
    sale: Sale = result.scalars().unique().one_or_none()

    assert sale.store_id == sale_add_data.store_id

    sale_products = list(map(lambda x: x.product_id, sale.products))
    add_data_products = list(
        map(lambda x: x.product_id, sale_add_data.products)
    )
    assert sale_products == add_data_products


async def test_dont_create_object_with_not_existsting_store_id(
    session, sale_add_data_with_not_existsting_city
):
    with pytest.raises(HTTPException) as e:
        await SaleRepository.create_object(
            session=session,
            data=sale_add_data_with_not_existsting_city,
        )
        assert isinstance(e, DBIntegrityException)


async def test_dont_create_object_with_not_existsting_product_id(
    session, sale_add_data_with_not_existsting_product
):
    with pytest.raises(HTTPException) as e:
        await SaleRepository.create_object(
            session=session,
            data=sale_add_data_with_not_existsting_product,
        )
        assert isinstance(e, DBIntegrityException)


async def test_update_partial_object(session, sale_update_data):
    sale_id = 1
    sale_model: Sale = await SaleRepository.update_partial_object(
        session=session,
        object_id=sale_id,
        data=sale_update_data,
    )

    sale = await session.get(Sale, sale_id)

    assert sale.store_id == sale_model.store_id


async def test_dont_update_partial_object_to_not_exists_store_id(
    session, sale_update_data_with_not_existsting_store
):
    with pytest.raises(HTTPException) as e:
        await SaleRepository.update_partial_object(
            session=session,
            object_id=1,
            data=sale_update_data_with_not_existsting_store,
        )
        assert isinstance(e, DBIntegrityException)


async def test_delete_object(session, sales):
    sale_id = 1

    sale_model: Sale = await SaleRepository.delete_object(
        session=session,
        object_id=sale_id,
    )
    sale_from_rep = sale_model.to_dict()

    assert sale_from_rep in sales
    assert await session.get(Sale, sale_id) is None


async def test_dont_delete_not_existing_object(session):
    sale_id = 1
    await SaleRepository.delete_object(
        session=session,
        object_id=sale_id,
    )
    with pytest.raises(HTTPException) as e:
        await SaleRepository.delete_object(
            session=session,
            object_id=sale_id,
        )
        assert isinstance(e, DBIntegrityException)


async def test_get_products(session, sales_products):
    sale_id = 1
    sale_poducts = list(filter(
        lambda x: x["sale_id"] == sale_id, sales_products)
    )

    sale = await SaleRepository.get_products(
        session=session,
        sale_id=sale_id,
    )
    for product in sale.products_details:
        sale_product = filter(
            lambda x: x["product_id"] == product.id, sale_poducts
        )
        assert len(list(sale_product)) == 1


async def test_add_product(session, sale_add_data, product_add_data):
    # test depends on test_create_object

    sale_id = await SaleRepository.create_object(
        session=session,
        data=sale_add_data,
    )

    await SaleRepository.add_product(
        session=session,
        sale_id=sale_id,
        product_data=product_add_data,
    )

    query = select(SaleProducts).filter_by(
        sale_id=sale_id, product_id=product_add_data.product_id
    )
    result: Result = await session.execute(query)
    assert result.scalars().one_or_none()


async def test_dont_add_not_existing_product(
    session, sale_add_data, product_add_data_with_not_existsting_product
):
    # test depends on test_create_object

    sale_id = await SaleRepository.create_object(
        session=session,
        data=sale_add_data,
    )

    with pytest.raises(HTTPException) as e:
        await SaleRepository.add_product(
            session=session,
            sale_id=sale_id,
            product_data=product_add_data_with_not_existsting_product,
        )
        assert isinstance(e, DBIntegrityException)


async def test_update_partial_product(session, product_update_data):
    # test depends on test_get_object
    sale_id = 1
    product_id = 1

    product: SaleProducts = await SaleRepository.update_partial_product(
        session=session,
        sale_id=sale_id,
        product_id=product_id,
        product_data=product_update_data,
    )

    assert product.quantity == product_update_data.quantity

    updated_sale: Sale = await SaleRepository.get_object(
        session=session,
        object_id=sale_id,
    )

    updated_product = list(
        filter(lambda x: x.product_id == product_id, updated_sale.products)
    )

    assert len(updated_product) == 1
    assert updated_product[0].quantity == product_update_data.quantity


async def test_delete_product(
    session,
):
    # test depends on test_get_object
    sale_id = 1
    product_id = 1

    await SaleRepository.delete_product(
        session=session,
        sale_id=sale_id,
        product_id=product_id,
    )

    updated_sale: Sale = await SaleRepository.get_object(
        session=session,
        object_id=sale_id,
    )

    updated_product = list(
        filter(lambda x: x.product_id == product_id, updated_sale.products)
    )

    assert len(updated_product) == 0


async def test_save_product_price(session, sales_products):
    # test depends on test_update_partial_object and get_sale_product
    sale_id = 1
    product_id = 1
    new_price = 123.11

    sale_product = list(filter(
        lambda x: x["sale_id"] == sale_id and x["product_id"] == product_id,
        sales_products
    ))[0]

    old_price = sale_product["unit_price"]

    assert old_price

    await ProductRepository.update_partial_object(
        session=session,
        object_id=product_id,
        data=ProductSchemaUpdatePartial(price=new_price),
    )
    assert old_price != new_price

    new_product: SaleProducts = await SaleRepository.get_sale_product(
        session=session, sale_id=sale_id, product_id=product_id
    )

    assert new_product.unit_price == old_price


@pytest.mark.parametrize(
    ("filters"),
    (
        pytest.param({}, id="empty params"),
        pytest.param(
            {
                "city_id": 1,
            },
            id="city_id one param",
        ),
        pytest.param(
            {
                "store_id": 1,
            },
            id="store_id one param",
        ),
        pytest.param(
            {
                "product_id": 1,
            },
            id="product_id one param",
        ),
        pytest.param(
            {
                "days": 1,
            },
            id="days one param",
        ),
        pytest.param(
            {
                "min_amount": 1000,
            },
            id="min_amount one param",
        ),
        pytest.param(
            {
                "max_amount": 500,
            },
            id="max_amount one param",
        ),
        pytest.param(
            {
                "min_quantity": 3,
            },
            id="max_quantity one param",
        ),
        pytest.param(
            {
                "max_quantity": 3,
            },
            id="max_quantity one param",
        ),
        pytest.param(
            {
                "city_id": 1,
                "store_id": 1,
                "product_id": 1,
            },
            id="city_id, store_id, product_id combination",
        ),
        pytest.param(
            {
                "city_id": -1,
                "store_id": 1,
                "product_id": 1,
            },
            id="negative id",
        ),
        pytest.param(
            {
                "city_id": 1,
                "store_id": -1,
                "product_id": 1,
            },
            id="negative id",
        ),
        pytest.param(
            {
                "city_id": 1,
                "store_id": 1,
                "product_id": -1,
            },
            id="negative id",
        ),
        pytest.param(
            {
                "days": -1,
            },
            id="nagative days",
        ),
        pytest.param(
            {
                "min_amount": -1,
                "max_amount": 500,
            },
            id="nagative amount",
        ),
        pytest.param(
            {
                "min_amount": -1,
                "max_amount": -1,
            },
            id="nagative amount",
        ),
        pytest.param(
            {
                "min_amount": 1000,
                "max_amount": 500,
            },
            id="mutually exclusive amount",
        ),
        pytest.param(
            {
                "min_quantity": -1,
                "max_quantity": 2,
            },
            id="nagative quantity",
        ),
        pytest.param(
            {
                "min_quantity": 1,
                "max_quantity": -1,
            },
            id="nagative quantity",
        ),
        pytest.param(
            {
                "min_quantity": 2,
                "max_quantity": 1,
            },
            id="mutually exclusive quantity",
        ),
        pytest.param(
            {
                "min_quantity": 2,
                "max_quantity": 5,
                "product_id": 1,
            },
            id="quantity and product_id combine",
        ),
        pytest.param(
            {
                "min_amount": 1000,
                "max_amount": 500,
                "product_id": 1,
            },
            id="amount and product_id combine",
        ),
    ),
)
async def test_parametrize_query(session, filters):
    sales_sql_filtered: list[Sale] = await SaleRepository.get_objects(
        session=session,
        **filters,
    )
    sales_python_filtered: list[Sale] = await filter_on_python(
        session=session, filters=filters)

    assert sales_sql_filtered == sales_python_filtered


filters_conditions = {
    "city_id": lambda filter_val, sale: sale.store.city_id == filter_val,
    "store_id": lambda filter_val, sale: sale.store_id == filter_val,
    "product_id": lambda filter_val, sale: (
        filter_val in list(map(lambda x: x.product_id, sale.products))
    ),
    "days": lambda filter_val, sale: (
        sale.created_at >= datetime.utcnow() - timedelta(days=filter_val)
    ),
    "min_amount": lambda filter_val, sale: (sale.total_amount >= filter_val),
    "max_amount": lambda filter_val, sale: (sale.total_amount <= filter_val),
    "min_quantity": lambda filter_val, sale: (
        sale.total_quantity >= filter_val
    ),
    "max_quantity": lambda filter_val, sale: (
        sale.total_quantity <= filter_val
    ),
}


def filter_sale(sale: Sale, filters: dict[str, Any]) -> bool:
    for filter, value in filters.items():
        condition = filters_conditions[filter]
        if not condition(value, sale):
            return False
    return True


async def filter_on_python(session, filters: dict[str, Any]) -> list[Sale]:
    query = select(Sale).options(
        selectinload(Sale.products), joinedload(Sale.store)
    )
    result: Result = await session.execute(query)
    sales: list[Sale] = result.scalars().unique().all()

    filtered_sales: list[Sale] = []

    for sale in sales:
        if filter_sale(sale, filters):
            filtered_sales.append(sale)

    return filtered_sales
