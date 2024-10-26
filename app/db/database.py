from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    async_scoped_session,
)

from app.config import settings


class database:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(url, echo=echo)

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

    async def session_dependancy(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


database = database(settings.DATABASE_URL, settings.ECHO)
