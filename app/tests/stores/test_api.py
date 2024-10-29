from httpx import AsyncClient
import pytest


async def test_get_stores(ac: AsyncClient):
    response = await ac.get("/stores")
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("request_data", "status_code"),
    (
        pytest.param(
            {
                "name": "такого нет в датасете",
                "city_id": 1,
            },
            200,
        ),
        pytest.param(
            {
                "invalid_param": "такого нет в датасете",
                "city_id": 1,
            },
            422,
            id="invalid body param",
        ),
        pytest.param(
            {
                "name": 123,
                "city_id": 1,
            },
            422,
            id="name is number",
        ),
        pytest.param(
            {
                "name": "такого нет в датасете",
                "city_id": "abc",
            },
            422,
            id="city id is str",
        ),
    ),
)
async def test_create_store(ac: AsyncClient, request_data, status_code):
    response = await ac.post("/stores", json=request_data)
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
async def test_get_store(ac: AsyncClient, id, status_code):
    response = await ac.get(f"/stores/{id}")
    print(response._content)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("request_data", "status_code"),
    (
        pytest.param(
            {
                "name": "такого нет в датасете",
                "city_id": 1,
            },
            200,
        ),
        pytest.param(
            {
                "invalid_param": "такого нет в датасете",
                "city_id": 1,
            },
            422,
            id="invalid body param",
        ),
        pytest.param(
            {
                "name": 123,
                "city_id": 1,
            },
            422,
            id="name is number",
        ),
        pytest.param(
            {
                "name": "такого нет в датасете",
                "city_id": "abc",
            },
            422,
            id="city id is str",
        ),
    ),
)
async def test_update_partial_store(
    ac: AsyncClient, request_data, status_code
):
    response = await ac.post("/stores", json=request_data)
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
async def test_delete_store(ac: AsyncClient, id, status_code):
    response = await ac.get(f"/stores/{id}")
    print(response._content)
    assert response.status_code == status_code
