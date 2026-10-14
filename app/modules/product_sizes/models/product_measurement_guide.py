import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.products.model import Product


class ProductMeasurementGuide(Base, TimestampMixin):
    __tablename__ = "product_measurement_guides"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    measurement_unit: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="cm",
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="measurement_guide",
    )
