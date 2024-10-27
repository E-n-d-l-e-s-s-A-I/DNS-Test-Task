from abc import abstractmethod
from typing import Any

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel


from app.db.abstract_models import Base
from app.utils.exceptions import DBIntegrityException, NotFoundException


class BaseRepository:
    model: Base

    @classmethod
    async def get_objects(
        cls, *, session: AsyncSession, options: Any = None, filters
    ) -> list[Any]:

        query = select(cls.model).order_by(cls.model.id)
        query = cls.apply_options_to_query(query, options)
        for filter in filters:
            query = query.filter(filter)

        result: Result = await session.execute(query)
        model_objects = result.scalars().all()
        return list(model_objects)

    @classmethod
    async def get_object(
        cls,
        *,
        session: AsyncSession,
        object_id: int,
        options: Any = None,
    ):

        query = select(cls.model).filter_by(id=object_id)
        query = cls.apply_options_to_query(query, options)
        result: Result = await session.execute(query)

        model_object = result.scalar_one_or_none()

        if model_object is None:
            raise NotFoundException

        return model_object

    @classmethod
    async def create_object(
        cls, *, session: AsyncSession, data: BaseModel
    ) -> int:
        model_object = cls.model(**data.model_dump())
        session.add(model_object)

        model_object = await cls.refresh_object(
            session=session, model_object=model_object
        )
        return model_object.id

    @classmethod
    async def update_partial_object(
        cls, *, session: AsyncSession, object_id: int, data: BaseModel
    ):
        model_object = await cls.get_object(
            session=session, object_id=object_id
        )
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(model_object, key, value)

        return await cls.refresh_object(
            session=session,
            model_object=model_object
        )

    @classmethod
    async def delete_object(
        cls, *, session: AsyncSession, object_id: int
    ):
        model_object = await cls.get_object(
            session=session, object_id=object_id
        )
        await session.delete(model_object)
        await session.commit()
        return model_object

    @classmethod
    async def refresh_object(
        cls, *, session: AsyncSession, model_object: Any
    ):
        try:
            await session.commit()
            await session.refresh(model_object)
            return model_object
        except IntegrityError as e:
            print(e._message)
            await session.rollback()
            raise DBIntegrityException

    @abstractmethod
    def apply_options_to_query(query, options):
        if options:
            query = query.options(options)
        return query
