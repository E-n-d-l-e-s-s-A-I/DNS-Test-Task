from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    ("params", "status_code"),
    (
        pytest.param({}, 200, id="empty params"),
        pytest.param({"city_id": "abc"}, 422, id="city_id str param"),
        pytest.param({"store_id": "abc"}, 422, id="store_id str param"),
        pytest.param({"product_id": "abc"}, 422, id="product_id str param"),
        pytest.param({"days": "abc"}, 422, id="days str param"),
        pytest.param({"min_amount": "abc"}, 422, id="min_amount str param"),
        pytest.param({"max_amount": "abc"}, 422, id="max_amount str param"),
        pytest.param(
            {"min_quantity": "abc"}, 422, id="min_quantity str param"
        ),
        pytest.param(
            {"max_quantity": "abc"}, 422, id="max_quantity str param"
        ),
    ),
)
async def test_get_sales(ac: AsyncClient, params, status_code):
    response = await ac.get("/sales", params=params)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("request_data", "status_code"),
    (
        pytest.param(
            {
                "store_id": 1,
                "products": [
                    {
                        "quantity": 1,
                        "product_id": 1,
                    },
                ],
            },
            200,
            id="correct data",
        ),
        pytest.param(
            {
                "store_id": 1,
                "products": [
                    {
                        "quantity": 1,
                        "product_id": 1,
                    },
                    {
                        "quantity": 2,
                        "product_id": 2,
                    },
                ],
            },
            200,
            id="correct data, many products",
        ),
        pytest.param(
            {
                "invalid_param": "такого нет в датасете",
            },
            422,
            id="invalid body param",
        ),
        pytest.param(
            {
                "store_id": "abc",
                "products": [
                    {
                        "quantity": 1,
                        "product_id": 1,
                    },
                ],
            },
            422,
            id="store_id is str",
        ),
        pytest.param(
            {
                "store_id": 1,
                "products": [
                    {
                        "quantity": 1,
                        "product_id": "asd",
                    },
                ],
            },
            422,
            id="product is str",
        ),
        pytest.param(
            {
                "store_id": 1,
                "products": [
                    {
                        "quantity": "abc",
                        "product_id": 1,
                    },
                ],
            },
            422,
            id="quantity is str",
        ),
        pytest.param(
            {
                "store_id": 1,
                "products": [
                    {
                        "quantity": -1,
                        "product_id": 1,
                    },
                ],
            },
            422,
            id="negative quantity",
        ),
        pytest.param(
            {
                "store_id": 1,
                "products": [
                    {
                        "quantity": 0,
                        "product_id": 1,
                    },
                ],
            },
            422,
            id="zero quantity",
        ),
        pytest.param(
            {
                "store_id": 1,
                "products": [
                    {
                        "quantity": 1.1,
                        "product_id": 1,
                    },
                ],
            },
            422,
            id="float quantity",
        ),
        pytest.param(
            {
                "store_id": 1,
                "products": [
                    {
                        "quantity": 1,
                        "product_id": 1,
                    },
                    {
                        "quantity": 3,
                        "product_id": 1,
                    },
                ],
            },
            422,
            id="duplicate product_id",
        ),
    ),
)
async def test_create_sale(ac: AsyncClient, request_data, status_code):
    response = await ac.post("/sales", json=request_data)
    print(response.text)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "status_code"),
    (
        pytest.param(1, 200),
        pytest.param(-1, 404, id="id not in db"),
        pytest.param("asd", 422, id="id is str"),
        pytest.param(1.1, 422, id="id is float"),
        pytest.param([], 422, id="id is empty list"),
        pytest.param([1], 422, id="id is list"),
    ),
)
async def test_get_sale(ac: AsyncClient, id, status_code):
    response = await ac.get(f"/sales/{id}")
    print(response._content)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "request_data", "status_code"),
    (
        pytest.param(
            1,
            {
                "store_id": 1,
            },
            200,
            id="correct store_id",
        ),
        pytest.param(
            1,
            {
                "store_id": "abc",
            },
            422,
            id="store_id is str",
        ),
    ),
)
async def test_update_partial_sale(
    ac: AsyncClient, id, request_data, status_code
):
    response = await ac.patch(f"/sales/{id}", json=request_data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "status_code"),
    (
        pytest.param(1, 200),
        pytest.param(-1, 404, id="id not in db"),
        pytest.param("asd", 422, id="id is str"),
        pytest.param(1.1, 422, id="id is float"),
        pytest.param([], 422, id="id is empty list"),
        pytest.param([1], 422, id="id is list"),
    ),
)
async def test_delete_product(ac: AsyncClient, id, status_code):
    response = await ac.delete(f"/sales/{id}")
    print(response._content)
    assert response.status_code == status_code


async def test_get_products(ac: AsyncClient):
    id = 1
    response = await ac.get(f"/sales/{id}/products")
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("request_data", "is_422"),
    (
        pytest.param(
            {
                "quantity": 1,
                "product_id": 1,
            },
            False,
            id="correct request_data",
        ),
        pytest.param(
            {
                "quantity": 1,
                "product_id": "abc",
            },
            True,
            id="product_id is str",
        ),
        pytest.param(
            {
                "quantity": "abc",
                "product_id": 1,
            },
            True,
            id="quantity is str",
        ),
        pytest.param(
            {
                "quantity": 0,
                "product_id": 1,
            },
            True,
            id="zero quantity",
        ),
        pytest.param(
            {
                "quantity": 0,
                "product_id": 1,
            },
            True,
            id="negative quantity",
        ),
        pytest.param(
            {
                "quantity": 1.1,
                "product_id": 1,
            },
            True,
            id="float quantity",
        ),
    ),
)
async def test_add_product(ac: AsyncClient, request_data, is_422):
    id = 1
    response = await ac.post(f"/sales/{id}/products", json=request_data)
    assert (response.status_code == 422) or not is_422


@pytest.mark.parametrize(
    ("request_data", "is_422"),
    (
        pytest.param(
            {
                "quantity": 1,
            },
            False,
            id="correct request_data",
        ),
        pytest.param(
            {
                "quantity": "abc",
            },
            True,
            id="quantity is str",
        ),
        pytest.param(
            {
                "quantity": 0,
            },
            True,
            id="zero quantity",
        ),
        pytest.param(
            {
                "quantity": 0,
            },
            True,
            id="negative quantity",
        ),
        pytest.param(
            {
                "quantity": 1.1,
            },
            True,
            id="float quantity",
        ),
    ),
)
async def test_update_product_in_sale(ac: AsyncClient, request_data, is_422):
    id = 1
    response = await ac.patch(f"/sales/{id}/products/{id}", json=request_data)
    assert (response.status_code == 422) or not is_422


@pytest.mark.parametrize(
    ("id", "status_code"),
    (
        pytest.param(1, 200),
        pytest.param(-1, 404, id="id not in db"),
        pytest.param("asd", 422, id="id is str"),
        pytest.param(1.1, 422, id="id is float"),
        pytest.param([], 422, id="id is empty list"),
        pytest.param([1], 422, id="id is list"),
    ),
)
async def test_delete_product_in_sale(ac: AsyncClient, id, status_code):
    response = await ac.delete(f"/sales/{id}/products/{id}")
    print(response._content)
    assert response.status_code == status_code
