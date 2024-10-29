
from httpx import AsyncClient
import pytest


async def test_get_cities(ac: AsyncClient):
    response = await ac.get("/cities")
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("id", "status_code"),
    (
        (1, 200),
        (-1, 404),
        ("asd", 422),
    )
)
async def test_get_city(ac: AsyncClient, id, status_code):
    response = await ac.get(f"/cities/{id}")
    print(response._content)
    assert response.status_code == status_code
