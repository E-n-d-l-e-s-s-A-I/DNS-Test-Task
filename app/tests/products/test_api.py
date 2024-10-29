from httpx import AsyncClient
import pytest


async def test_get_products(ac: AsyncClient):
    response = await ac.get("/products")
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("request_data", "status_code"),
    (
        pytest.param(
            {
                "name": "такого нет в датасете",
                "price": 1,
            },
            200,
            id="price is int"
        ),
        pytest.param(
            {
                "name": "такого нет в датасете",
                "price": 1.1,
            },
            200,
            id="price with 1 decimal places"
        ),
        pytest.param(
            {
                "name": "такого нет в датасете",
                "price": 1.11,
            },
            200,
            id="price with 2 decimal places"
        ),
        pytest.param(
            {
                "name": "такого нет в датасете",
                "price": 1.111,
            },
            422,
            id="price with 3 decimal places"
        ),
        pytest.param(
            {
                "invalid_param": "такого нет в датасете",
                "price": 1,
            },
            422,
            id="invalid body param",
        ),
        pytest.param(
            {
                "name": 123,
                "price": "1",
            },
            422,
            id="price is str",
        ),
        pytest.param(
            {
                "name": 123,
                "price": 1,
            },
            422,
            id="name is number",
        ),
    ),
)
async def test_create_product(ac: AsyncClient, request_data, status_code):
    response = await ac.post("/products", json=request_data)
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
async def test_get_product(ac: AsyncClient, id, status_code):
    response = await ac.get(f"/products/{id}")
    print(response._content)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("request_data", "status_code"),
    (
        pytest.param(
            {
                "name": "такого нет в датасете",
                "price": 1,
            },
            200,
            id="price is int"
        ),
        pytest.param(
            {
                "name": "такого нет в датасете",
                "price": 1.1,
            },
            200,
            id="price with 1 decimal places"
        ),
        pytest.param(
            {
                "name": "такого нет в датасете",
                "price": 1.11,
            },
            200,
            id="price with 2 decimal places"
        ),
        pytest.param(
            {
                "name": "такого нет в датасете",
                "price": 1.111,
            },
            422,
            id="price with 3 decimal places"
        ),
        pytest.param(
            {
                "invalid_param": "такого нет в датасете",
                "price": 1,
            },
            422,
            id="invalid body param",
        ),
        pytest.param(
            {
                "name": 123,
                "price": "1",
            },
            422,
            id="price is str",
        ),
        pytest.param(
            {
                "name": 123,
                "price": 1,
            },
            422,
            id="name is number",
        ),
    ),
)
async def test_update_partial_product(
    ac: AsyncClient, request_data, status_code
):
    response = await ac.post("/products", json=request_data)
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
    response = await ac.get(f"/products/{id}")
    print(response._content)
    assert response.status_code == status_code
