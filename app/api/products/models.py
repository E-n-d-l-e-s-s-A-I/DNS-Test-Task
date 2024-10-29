from sqlalchemy import DECIMAL, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.abstract_models import UniqueNamed
from app.db.annotations_types import INT_PK


class Product(UniqueNamed):
    __table_args__ = (
        CheckConstraint("price > 0", name="check_price_positive"),
    )

    repr_cols = ("id", "name", "price")

    id: Mapped[INT_PK]
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))

    sales_details: Mapped[list["SaleProducts"]] = relationship(
        back_populates="product",
        cascade="all, delete"
    )
