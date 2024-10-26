from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends


from .schemas import (
    SaleProductSchema,
    SaleSchema,
    SaleSchemaCreate,
    SaleSchemaUpdatePartial,
    SaleProductSchemaCreate,
    SaleProductSchemaUpdatePartial,
    ProductSchemaWithUnitPrice
)
from .repository import SaleRepository
from app.db.database import database
from app.utils.exceptions import (
    DBIntegrityException,
    NotFoundException,
    get_http_exceptions_description,
)
from app.utils.shemas import CreateResultSchema


router = APIRouter(
    prefix="/sales",
    tags=["Продажи"],
)


@router.get("")
async def get_sales(
    session: AsyncSession = Depends(database.session_dependancy),
) -> list[SaleSchema]:
    return await SaleRepository.get_objects(session=session)


@router.get(
    "/{sale_id}",
    responses=get_http_exceptions_description(NotFoundException),
)
async def get_sale(
    sale_id: int, session: AsyncSession = Depends(database.session_dependancy)
) -> SaleSchema:
    return await SaleRepository.get_object(session=session, object_id=sale_id)


@router.post(
    "",
    responses=get_http_exceptions_description(DBIntegrityException),
)
async def create_sale(
    sale_data: SaleSchemaCreate,
    session: AsyncSession = Depends(database.session_dependancy),
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
    session: AsyncSession = Depends(database.session_dependancy),
) -> SaleSchema:
    return await SaleRepository.update_partial_object(
        session=session, object_id=sale_id, data=sale_data
    )


@router.delete(
    "/{sale_id}",
    responses=get_http_exceptions_description(
        NotFoundException,
        DBIntegrityException
    ),
)
async def delete_sale(
    sale_id: int,
    session: AsyncSession = Depends(database.session_dependancy),
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
    session: AsyncSession = Depends(database.session_dependancy),
) -> list[ProductSchemaWithUnitPrice]:
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
    session: AsyncSession = Depends(database.session_dependancy),
) -> SaleSchema:
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
    session: AsyncSession = Depends(database.session_dependancy),
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
    session: AsyncSession = Depends(database.session_dependancy),
) -> SaleProductSchema:
    return await SaleRepository.delete_product(
        session=session,
        sale_id=sale_id,
        product_id=product_id,
    )
