
from httpx import AsyncClient
import pytest


async def test_get_cities(ac: AsyncClient):
    response = await ac.get("/cities")
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("request_data", "status_code"),
    (
        pytest.param(
            {"name": "такого нет в датасете"},
            200,
        ),
        pytest.param(
            {"invalid_param": "такого нет в датасете"},
            422,
            id="invalid body param",
        ),
        pytest.param(
            {"name": 123},
            422,
            id="name is number",
        ),
    )
)
async def test_create_city(ac: AsyncClient, request_data, status_code):
    response = await ac.post("/cities", json=request_data)
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
    )
)
async def test_get_city(ac: AsyncClient, id, status_code):
    response = await ac.get(f"/cities/{id}")
    print(response._content)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "request_data", "status_code"),
    (
        pytest.param(
            1,
            {"name": "такого нет в датасете"},
            200,
        ),
        pytest.param(
            1,
            {"name": 123},
            422,
            id="name is number",
        ),
    )
)
async def test_update_partial_city(
    ac: AsyncClient, id, request_data, status_code
):
    response = await ac.patch(f"/cities/{id}", json=request_data)
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
    )
)
async def test_delete_city(ac: AsyncClient, id, status_code):
    response = await ac.delete(f"/cities/{id}")
    print(response._content)
    assert response.status_code == status_code
