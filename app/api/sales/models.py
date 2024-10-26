from sqlalchemy import DECIMAL, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.annotations_types import INT_PK, CREATED_AT_DATETIME
from app.db.abstract_models import Base


class Sale(Base):
    repr_cols = ("id",)

    id: Mapped[INT_PK]
    created_at: Mapped[CREATED_AT_DATETIME]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("store.id", ondelete="CASCADE")
    )
    store: Mapped["Store"] = relationship(back_populates="sales")

    products: Mapped[list["SaleProducts"]] = relationship(
        back_populates="sale",
        cascade="all, delete",
    )


class SaleProducts(Base):
    __tablename__ = "sale_products"
    __table_args__ = (
        UniqueConstraint(
            "sale_id",
            "product_id",
            name="idx_unique_sale_product",
        ),
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('unit_price > 0', name='check_unit_price_positive'),
    )

    repr_cols = ("id", "sale_id", "product_id", "quantity")

    id: Mapped[INT_PK]
    sale_id: Mapped[int] = mapped_column(
        ForeignKey("sale.id", ondelete="CASCADE"),
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE"),
    )

    quantity: Mapped[int] = mapped_column(
        default=1,
        server_default="1",
    )
    unit_price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))

    sale: Mapped["Sale"] = relationship(back_populates="products")
    product: Mapped["Product"] = relationship(back_populates="sales_details")
