from sqlalchemy import (
    DECIMAL,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    func,
    select
)
from sqlalchemy.ext.hybrid import hybrid_property
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

    @hybrid_property
    def total_amount(self):
        if not self.products:
            return 0
        return sum(product.total_price for product in self.products)

    @total_amount.expression
    def total_amount(cls):
        return (
            select(
                func.coalesce(
                    func.sum(SaleProducts.unit_price * SaleProducts.quantity),
                    0,
                )
            )
            .where(SaleProducts.sale_id == cls.id)
            .correlate(cls)
            .label("total_amount")
        )

    @hybrid_property
    def total_quantity(self):
        if not self.products:
            return 0
        return sum(product.quantity for product in self.products)

    @total_quantity.expression
    def total_quantity(cls):
        return (
            select(
                func.coalesce(
                    func.sum(SaleProducts.quantity),
                    0,
                )
            )
            .where(SaleProducts.sale_id == cls.id)
            .correlate(cls)
            .label("total_quantity")
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

    @hybrid_property
    def total_price(self):
        return self.unit_price * self.quantity
