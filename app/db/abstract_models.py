"""Module defines abstract SQLAlchemy models"""

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped, mapped_column, DeclarativeBase, declared_attr
)

from app.config import settings


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    repr_cols = tuple()  # names of displayed attributes

    def __repr__(self) -> str:
        repr_cols_with_vals = [
            f"{col}={getattr(self, col)}"
            for col in self.repr_cols
        ]

        return f"<{self.__class__.__name__} {', '.join(repr_cols_with_vals)}>"


class UniqueNamed(Base):
    __abstract__ = True
    name: Mapped[str] = mapped_column(
        String(settings.DB_STR_MAX_LEN), unique=True, nullable=False
    )
