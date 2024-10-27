from sqlalchemy.orm import Mapped, relationship

from app.db.abstract_models import UniqueNamed
from app.db.annotations_types import INT_PK
from app.api.stores.models import Store


class City(UniqueNamed):
    repr_cols = ("id", "name")

    id: Mapped[INT_PK]

    stores: Mapped[list["Store"]] = relationship(
        back_populates="city",
        cascade="all, delete"
    )
