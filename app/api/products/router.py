from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from .schemas import (
    ProductSchema,
    ProductSchemaCreate,
    ProductSchemaUpdatePartial
)
from .repository import ProductRepository
from app.db.database import database
from app.utils.exceptions import (
    DBIntegrityException,
    NotFoundException,
    get_http_exceptions_description,
)
from app.utils.shemas import CreateResultSchema


router = APIRouter(
    prefix="/products",
    tags=["Товары"],
    dependencies=[Depends(database.session_dependency)],
)


@router.get("")
async def get_products(
    session: AsyncSession = Depends(database.session_dependency),
) -> list[ProductSchema]:
    return await ProductRepository.get_objects(session=session)


@router.get(
    "/{product_id}",
    responses=get_http_exceptions_description(NotFoundException),
)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(database.session_dependency),
) -> ProductSchema:
    return await ProductRepository.get_object(
        session=session, object_id=product_id
    )


@router.post(
    "",
    responses=get_http_exceptions_description(DBIntegrityException),
)
async def create_product(
    product_data: ProductSchemaCreate,
    session: AsyncSession = Depends(database.session_dependency),
) -> CreateResultSchema:
    product_id = await ProductRepository.create_object(
        session=session,
        data=product_data
    )
    return CreateResultSchema(id=product_id)


@router.patch(
    "/{product_id}",
    responses=get_http_exceptions_description(
        NotFoundException,
        DBIntegrityException
    ),
)
async def update_partial_product(
    product_id: int,
    product_data: ProductSchemaUpdatePartial,
    session: AsyncSession = Depends(database.session_dependency),
) -> ProductSchema:
    return await ProductRepository.update_partial_object(
        session=session, object_id=product_id, data=product_data
    )


@router.delete(
    "/{product_id}",
    responses=get_http_exceptions_description(NotFoundException),
)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(database.session_dependency),
) -> ProductSchema:
    return await ProductRepository.delete_object(
        session=session, object_id=product_id
    )
