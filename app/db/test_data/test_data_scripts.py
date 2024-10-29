import asyncio
import json

from sqlalchemy import insert

from app.db.abstract_models import Base
from app.db.database import database
from app.api.cities.models import City
from app.api.stores.models import Store
from app.api.products.models import Product
from app.api.sales.models import Sale, SaleProducts


# order is important
models = (City, Store, Product, Sale, SaleProducts)


def open_json(model_name: str):
    with open(
        f"app/db/test_data/{model_name}.json",
        encoding="utf-8"
    ) as file:
        return json.load(file)


async def select_test_data():
    async with database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    async with database.async_session_maker() as session:
        for model in models:
            data = open_json(model.__tablename__)
            add_query = insert(model).values(data)
            await session.execute(add_query)

        await session.commit()

if __name__ == "__main__":
    asyncio.run(select_test_data())
    print("данные успешно вставлены")
