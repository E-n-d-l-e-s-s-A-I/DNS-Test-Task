import pytest

# from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.db.test_data.test_data_scripts import select_test_data
from app.db.database import database

from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    await select_test_data()


@pytest.fixture(scope="session")
async def ac():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async for db_session in database.session_dependency():
        yield db_session
