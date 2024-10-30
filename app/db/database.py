from asyncio import current_task
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    async_scoped_session,
)

from app.config import settings

# Determine the appropriate database URL
# and configuration based on the application mode
if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_KWARGS = {"savemode": True, "poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_KWARGS = {}


class Database:
    """
    Class configures and provides access to
    the asynchronous SQLAlchemy database engine and sessions.
    """
    def __init__(
        self, url:
            str,
            echo:
            bool = False,
            savemode: bool = False,
            **kwaqrgs
    ) -> None:
        self.engine = create_async_engine(url, echo=echo, **kwaqrgs)
        self.savemode = savemode
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
        async with database.engine.connect() as connection:
            async with connection.begin() as transaction:
                scoped_session = self.get_scoped_session()
                async with (
                    scoped_session(bind=connection) as session
                ):
                    yield session
                    if transaction.is_active and self.savemode:
                        await transaction.rollback()


database = Database(DATABASE_URL, settings.ECHO, **DATABASE_KWARGS)
