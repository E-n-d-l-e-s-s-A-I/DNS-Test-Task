from decimal import Decimal
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from .schemas import (
    SaleProductSchema,
    SaleSchema,
    SaleSchemaCreate,
    SaleSchemaDetail,
    SaleSchemaUpdatePartial,
    SaleProductSchemaCreate,
    SaleProductSchemaUpdatePartial,

)
from .repository import SaleRepository
from app.db.database import database
from app.utils.exceptions import (
    DBIntegrityException,
    NotFoundException,
    InvalidParameterException,
    get_http_exceptions_description,
)
from app.utils.shemas import CreateResultSchema


router = APIRouter(
    prefix="/sales",
    tags=["Продажи"],
    dependencies=[Depends(database.session_dependency)],
)


@router.get(
    "",
    responses=get_http_exceptions_description(InvalidParameterException)
)
async def get_sales(
    session: AsyncSession = Depends(database.session_dependency),
    city_id: Optional[int] = None,
    store_id: Optional[int] = None,
    product_id: Optional[int] = None,
    days: Optional[int] = None,
    min_amount: Optional[Decimal] = None,
    max_amount: Optional[Decimal] = None,
    min_quantity: Optional[int] = None,
    max_quantity: Optional[int] = None,
) -> list[SaleSchema]:
    return await SaleRepository.get_objects(
        session=session,
        city_id=city_id,
        store_id=store_id,
        product_id=product_id,
        days=days,
        min_amount=min_amount,
        max_amount=max_amount,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
    )


@router.get(
    "/{sale_id}",
    responses=get_http_exceptions_description(NotFoundException),
)
async def get_sale(
    sale_id: int, session: AsyncSession = Depends(database.session_dependency)
) -> SaleSchema:
    return await SaleRepository.get_object(session=session, object_id=sale_id)


@router.post(
    "",
    responses=get_http_exceptions_description(DBIntegrityException),
)
async def create_sale(
    sale_data: SaleSchemaCreate,
    session: AsyncSession = Depends(database.session_dependency),
) -> CreateResultSchema:
    sale_id = await SaleRepository.create_object(
        session=session,
        data=sale_data
    )
    return CreateResultSchema(id=sale_id)


@router.patch(
    "/{sale_id}",
    responses=get_http_exceptions_description(
        NotFoundException,
        DBIntegrityException
    ),
)
async def update_partial_sale(
    sale_id: int,
    sale_data: SaleSchemaUpdatePartial,
    session: AsyncSession = Depends(database.session_dependency),
) -> SaleSchema:
    return await SaleRepository.update_partial_object(
        session=session, object_id=sale_id, data=sale_data
    )


@router.delete(
    "/{sale_id}",
    responses=get_http_exceptions_description(
        NotFoundException
    ),
)
async def delete_sale(
    sale_id: int,
    session: AsyncSession = Depends(database.session_dependency),
) -> SaleSchema:
    return await SaleRepository.delete_object(
        session=session,
        object_id=sale_id
    )


@router.get(
    "/{sale_id}/products",
    responses=get_http_exceptions_description(NotFoundException),
)
async def get_products(
    sale_id: int,
    session: AsyncSession = Depends(database.session_dependency),
) -> SaleSchemaDetail:
    return await SaleRepository.get_products(
        session=session,
        sale_id=sale_id,
    )


@router.post(
    "/{sale_id}/products",
    responses=get_http_exceptions_description(
        NotFoundException,
        DBIntegrityException
    ),
)
async def add_product(
    sale_id: int,
    product_data: SaleProductSchemaCreate,
    session: AsyncSession = Depends(database.session_dependency),
) -> SaleSchemaDetail:
    return await SaleRepository.add_product(
        session=session,
        sale_id=sale_id,
        product_data=product_data,
    )


@router.patch(
    "/{sale_id}/products/{product_id}",
    responses=get_http_exceptions_description(
        NotFoundException,
    ),
)
async def update_product_in_sale(
    sale_id: int,
    product_id: int,
    product_data: SaleProductSchemaUpdatePartial,
    session: AsyncSession = Depends(database.session_dependency),
) -> SaleProductSchema:
    return await SaleRepository.update_partial_product(
        session=session,
        sale_id=sale_id,
        product_id=product_id,
        product_data=product_data,
    )


@router.delete(
    "/{sale_id}/products/{product_id}",
    responses=get_http_exceptions_description(NotFoundException),
)
async def delete_product_in_sale(
    sale_id: int,
    product_id: int,
    session: AsyncSession = Depends(database.session_dependency),
) -> SaleProductSchema:
    return await SaleRepository.delete_product(
        session=session,
        sale_id=sale_id,
        product_id=product_id,
    )
