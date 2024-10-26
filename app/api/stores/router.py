from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from .schemas import StoreSchema, StoreSchemaCreate, StoreSchemaUpdatePartial
from .repository import StoreRepository
from app.db.database import database
from app.utils.exceptions import (
    DBIntegrityException,
    NotFoundException,
    get_http_exceptions_description,
)
from app.utils.shemas import CreateResultSchema

router = APIRouter(
    prefix="/stores",
    tags=["Магазины"],
)


@router.get("")
async def get_stores(
    session: AsyncSession = Depends(database.session_dependancy),
) -> list[StoreSchema]:
    return await StoreRepository.get_objects(session=session)


@router.get(
    "/{store_id}",
    responses=get_http_exceptions_description(NotFoundException),
)
async def get_store(
    store_id: int, session: AsyncSession = Depends(database.session_dependancy)
) -> StoreSchema:
    return await StoreRepository.get_object(
        session=session, object_id=store_id
    )


@router.post(
    "",
    responses=get_http_exceptions_description(DBIntegrityException),
)
async def create_store(
    store_data: StoreSchemaCreate,
    session: AsyncSession = Depends(database.session_dependancy),
) -> CreateResultSchema:
    store_id = await StoreRepository.create_object(
        session=session, data=store_data
    )
    return CreateResultSchema(id=store_id)


@router.patch(
    "/{store_id}",
    responses=get_http_exceptions_description(
        NotFoundException,
        DBIntegrityException
    ),
)
async def update_partial_store(
    store_id: int,
    store_data: StoreSchemaUpdatePartial,
    session: AsyncSession = Depends(database.session_dependancy),
) -> StoreSchema:
    return await StoreRepository.update_partial_object(
        session=session, object_id=store_id, data=store_data
    )


@router.delete(
    "/{store_id}",
    responses=get_http_exceptions_description(NotFoundException),
)
async def delete_store(
    store_id: int,
    session: AsyncSession = Depends(database.session_dependancy),
) -> StoreSchema:
    return await StoreRepository.delete_object(
        session=session, object_id=store_id
    )
