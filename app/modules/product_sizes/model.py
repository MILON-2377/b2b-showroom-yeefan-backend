import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.product_customizations.model import ProductCustomization
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

    customization: Mapped["ProductCustomization | None"] = relationship(
        "ProductCustomization",
        back_populates="product",
        cascade="all, delete-orphan",
        uselist=False,
    )
