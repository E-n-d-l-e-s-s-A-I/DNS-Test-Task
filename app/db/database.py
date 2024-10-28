from asyncio import current_task
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    async_scoped_session,
)

from app.config import settings


if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_KWARGS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_KWARGS = {}


class Database:

    def __init__(self, url: str, echo: bool = False, **kwaqrgs) -> None:
        self.engine = create_async_engine(url, echo=echo, **kwaqrgs)

        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            self.async_session_maker,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


database = Database(DATABASE_URL, settings.ECHO, **DATABASE_KWARGS)
