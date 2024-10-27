from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from .schemas import CitySchema, CitySchemaCreate, CitySchemaUpdatePartial
from .repository import CityRepository
from app.db.database import database
from app.utils.exceptions import (
    DBIntegrityException,
    NotFoundException,
    get_http_exceptions_description,
)
from app.utils.shemas import CreateResultSchema


router = APIRouter(
    prefix="/cities",
    tags=["Города"],
    dependencies=[Depends(database.session_dependency)],
)


@router.get("")
async def get_cities(
    session: AsyncSession = Depends(database.session_dependency),
) -> list[CitySchema]:
    return await CityRepository.get_objects(session=session)


@router.get(
    "/{city_id}",
    responses=get_http_exceptions_description(NotFoundException),
)
async def get_city(
    city_id: int, session: AsyncSession = Depends(database.session_dependency)
) -> CitySchema:
    return await CityRepository.get_object(session=session, object_id=city_id)


@router.post(
    "",
    responses=get_http_exceptions_description(DBIntegrityException),
)
async def create_city(
    city_data: CitySchemaCreate,
    session: AsyncSession = Depends(database.session_dependency),
) -> CreateResultSchema:
    city_id = await CityRepository.create_object(
        session=session, data=city_data
    )
    return CreateResultSchema(id=city_id)


@router.patch(
    "/{city_id}",
    responses=get_http_exceptions_description(
        NotFoundException,
        DBIntegrityException
    ),
)
async def update_partial_city(
    city_id: int,
    city_data: CitySchemaUpdatePartial,
    session: AsyncSession = Depends(database.session_dependency),
) -> CitySchema:
    return await CityRepository.update_partial_object(
        session=session, object_id=city_id, data=city_data
    )


@router.delete(
    "/{city_id}",
    responses=get_http_exceptions_description(NotFoundException),
)
async def delete_city(
    city_id: int,
    session: AsyncSession = Depends(database.session_dependency),
) -> CitySchema:
    return await CityRepository.delete_object(
        session=session, object_id=city_id
    )
