import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.product_sizes.models.product_size import ProductSize


class SizeMeasurement(Base, TimestampMixin):
    __tablename__ = "size_measurements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    product_size_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product_sizes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    bust: Mapped[float | None] = mapped_column(
        Numeric(6, 2),
        nullable=True,
    )

    waist: Mapped[float | None] = mapped_column(
        Numeric(6, 2),
        nullable=True,
    )

    hips: Mapped[float | None] = mapped_column(
        Numeric(6, 2),
        nullable=True,
    )

    hollow_to_hem: Mapped[float | None] = mapped_column(
        Numeric(6, 2),
        nullable=True,
    )

    unit: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="cm",
    )

    __table_args__ = (
        UniqueConstraint(
            "product_size_id",
            name="uq_size_measurement",
        ),
    )

    product_size: Mapped["ProductSize"] = relationship(
        "ProductSize",
        back_populates="measurement",
    )
