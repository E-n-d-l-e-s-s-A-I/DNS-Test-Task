from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.products.models import Product

from .models import Sale, SaleProducts
from .schemas import (
    SaleProductSchemaCreate,
    SaleSchemaCreate,
    SaleProductSchemaUpdatePartial,
)
from app.api.products.repository import ProductRepository
from app.utils.repository import BaseRepository
from app.utils.exceptions import NotFoundException, DBIntegrityException


class SaleRepository(BaseRepository):
    model = Sale

    @classmethod
    async def get_objects(
        cls, *, session: AsyncSession
    ) -> list[Sale]:
        sales = await super().get_objects(
            session=session,
            options=(selectinload(Sale.products))
        )
        return sales

    @classmethod
    async def get_object(
        cls, *, session: AsyncSession, object_id: int
    ) -> Sale:
        return await super().get_object(
            session=session,
            object_id=object_id,
            options=(selectinload(Sale.products))
        )

    @classmethod
    async def create_object(
        cls, *, session: AsyncSession, data: SaleSchemaCreate
    ) -> int:
        # we need select products to get actual price
        products = await ProductRepository.get_products_by_ids(
            session=session,
            ids=data.produsts_ids
        )
        products_quantity = {product_info.product_id: product_info.quantity
                             for product_info in data.products
                             }

        if len(products) != len(data.produsts_ids):
            raise DBIntegrityException

        sale = Sale(store_id=data.store_id)
        for product in products:
            sale.products.append(SaleProducts(
                product_id=product.id,
                quantity=products_quantity[product.id],
                unit_price=product.price,
                )
            )

        session.add(sale)
        sale = await cls.refresh_object(
            session=session,
            model_object=sale,
        )
        return sale.id

    @classmethod
    async def get_products(
        cls, *, session: AsyncSession, sale_id: int
    ) -> list[Product]:
        sale = await super().get_object(
            session=session,
            object_id=sale_id,
            options=(
                selectinload(Sale.products).joinedload(SaleProducts.product)
            )
        )

        result = []

        # and add quantity and unit_price to product
        for product_detail in sale.products:
            product_detail.product.unit_price = product_detail.unit_price
            product_detail.product.quantity = product_detail.quantity
            result.append(product_detail.product)

        return result

    @classmethod
    async def add_product(
        cls,
        *,
        session: AsyncSession,
        sale_id: int,
        product_data: SaleProductSchemaCreate,
    ) -> Sale:
        sale = await super().get_object(
            session=session,
            object_id=sale_id,
            options=(
                selectinload(Sale.products)
            )
        )

        # we need select product to get actual price
        product = await ProductRepository.get_object(
            session=session,
            object_id=product_data.product_id,
        )

        sale.products.append(
            SaleProducts(
                product_id=product.id,
                quantity=product_data.quantity,
                unit_price=product.price,
            )
        )

        return await cls.refresh_object(
            session=session,
            model_object=sale,
        )

    @classmethod
    async def update_partial_product(
        cls,
        *,
        session: AsyncSession,
        sale_id: int,
        product_id: int,
        product_data: SaleProductSchemaUpdatePartial,
    ) -> SaleProducts:

        sale_product = await cls.get_sale_product(
            session=session,
            sale_id=sale_id,
            product_id=product_id,
        )

        for key, value in product_data.model_dump(exclude_unset=True).items():
            setattr(sale_product, key, value)

        return await cls.refresh_object(
            session=session,
            model_object=sale_product
        )

    @classmethod
    async def delete_product(
        cls,
        *,
        session: AsyncSession,
        sale_id: int,
        product_id: int,
    ) -> SaleProducts:

        sale_product = await cls.get_sale_product(
            session=session,
            sale_id=sale_id,
            product_id=product_id,
        )

        if sale_product is None:
            raise NotFoundException

        await session.delete(sale_product)
        await session.commit()
        return sale_product

    @classmethod
    async def get_sale_product(
        cls, session: AsyncSession, product_id: int, sale_id: int
    ) -> SaleProducts:
        query = select(SaleProducts).filter_by(
            product_id=product_id, sale_id=sale_id
        )
        result: Result = await session.execute(query)
        sale_product = result.scalar_one_or_none()

        if sale_product is None:
            raise NotFoundException
        return sale_product
