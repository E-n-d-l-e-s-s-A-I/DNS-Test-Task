from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.abstract_models import UniqueNamed
from app.db.annotations_types import INT_PK

from app.api.sales.models import Sale


class Store(UniqueNamed):
    repr_cols = ("id", "name")

    id: Mapped[INT_PK]
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.id", ondelete="CASCADE"),
    )

    city: Mapped["City"] = relationship(back_populates="stores")
    sales: Mapped[list["Sale"]] = relationship(
        back_populates="store",
        cascade="all, delete"
    )
