from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product
from app.utils.repository import BaseRepository


class ProductRepository(BaseRepository):
    model = Product

    @classmethod
    async def get_products_by_ids(
        cls, *, session: AsyncSession, ids: list[int]
    ) -> list[Product]:
        query = select(Product).filter(Product.id.in_(ids))
        result: Result = await session.execute(query)
        return result.scalars().all()
