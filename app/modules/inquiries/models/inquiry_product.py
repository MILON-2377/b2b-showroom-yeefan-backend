from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.inquiries.models.inquiry import Inquiry
    from app.modules.products.model import Product




class InquiryProduct(Base, TimestampMixin):
    __tablename__ = "inquiry_products"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    inquiry_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("inquiries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    quantity_requested: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "inquiry_id",
            "product_id",
            name="uq_inquiry_product",
        ),
        CheckConstraint(
            "quantity_requested > 0",
            name="ck_inquiry_product_quantity_positive",
        ),
    )

    # ORM relationships
    inquiry: Mapped["Inquiry"] = relationship(
        "Inquiry",
        back_populates="inquiry_products",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="inquiry_products",
    )
