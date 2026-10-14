import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.product_sizes.models.size_measurement import SizeMeasurement
    from app.modules.products.model import Product


class ProductSize(Base, TimestampMixin):
    __tablename__ = "product_sizes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "name",
            name="uq_product_size",
        ),
        CheckConstraint(
            "sort_order >= 0",
            name="ck_product_size_sort_order_non_negative",
        ),
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="sizes",
    )

    measurement: Mapped["SizeMeasurement | None"] = relationship(
        "SizeMeasurement",
        back_populates="product_size",
        cascade="all, delete-orphan",
        uselist=False,
    )
