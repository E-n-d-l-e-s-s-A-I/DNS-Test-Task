from datetime import datetime, timedelta

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
from app.api.stores.models import Store
from app.utils.repository import BaseRepository
from app.utils.exceptions import (
    NotFoundException,
    DBIntegrityException,
    InvalidParameterException
)


class SaleRepository(BaseRepository):
    model = Sale

    filters_conditions = {
        "city_id": lambda city_id: Store.city_id == city_id,
        "store_id": lambda store_id: Sale.store_id == store_id,
        "product_id": lambda product_id: SaleProducts.product_id == product_id,
        "days": lambda days: (
            Sale.created_at >= (
                datetime.utcnow() - timedelta(days=days)
            )
        ),
        "min_amount": lambda min_amount: Sale.total_amount >= min_amount,
        "max_amount": lambda max_amount: Sale.total_amount <= max_amount,
        "min_quantity": lambda min_quantity: (
            Sale.total_quantity >= min_quantity
        ),
        "max_quantity": lambda max_quantity: (
            Sale.total_quantity <= max_quantity
        ),
    }

    filters_joins = {
        ("product_id",): Sale.products,
        ("city_id",): Sale.store,
    }

    @classmethod
    async def get_objects(
        cls,
        *,
        session: AsyncSession,
        **filters
    ) -> list[Sale]:
        # breakpoint()

        # remove none filters kwargs
        filters = {k: v for k, v in filters.items() if v is not None}

        query = select(Sale).order_by(Sale.id)

        # join others tables, if necessary
        for filter_keys, join_relation in cls.filters_joins.items():
            if set(filter_keys) & filters.keys():
                query = query.join(join_relation)

        # apply filters
        for filter_key, filter_value in filters.items():
            try:
                query = query.filter(
                    cls.filters_conditions[filter_key](filter_value)
                )
            except KeyError:
                raise InvalidParameterException

        # make query
        query = query.options(selectinload(Sale.products))
        result: Result = await session.execute(query)
        sales = list(result.scalars().unique().all())
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
            session=session, ids=data.products_ids
        )
        products_quantity = {product_info.product_id: product_info.quantity
                             for product_info in data.products
                             }

        # if any of input products not found
        if len(products) != len(data.products_ids):
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
        sale: Sale = await cls.refresh_object(
            session=session,
            model_object=sale,
        )
        return sale.id

    @classmethod
    async def get_products(
        cls, *, session: AsyncSession, sale_id: int
    ) -> Sale:
        sale: Sale = await super().get_object(
            session=session,
            object_id=sale_id,
            options=(
                selectinload(Sale.products).joinedload(SaleProducts.product)
            )
        )

        sale.products_details = cls.get_products_details(sale)
        return sale

    @classmethod
    async def add_product(
        cls,
        *,
        session: AsyncSession,
        sale_id: int,
        product_data: SaleProductSchemaCreate,
    ) -> Sale:
        sale: Sale = await super().get_object(
            session=session,
            object_id=sale_id,
            options=(
                selectinload(Sale.products)
                .joinedload(SaleProducts.product)
            )
        )

        # we need select product to get actual price
        product: Product = await ProductRepository.get_object(
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

        sale: Sale = await cls.refresh_object(
            session=session,
            model_object=sale,
        )

        sale.products_details = cls.get_products_details(sale)
        return sale

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

    @classmethod
    def get_products_details(
        cls, sale: Sale
    ) -> list[Product]:
        result = []

        # and add quantity and unit_price to product
        for product_detail in sale.products:
            product_detail.product.unit_price = product_detail.unit_price
            product_detail.product.quantity = product_detail.quantity
            result.append(product_detail.product)

        return result
