import uuid
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.products.model import Product


class CustomizationOptionType(str, Enum):
    FABRIC = "FABRIC"
    COLOR = "COLOR"
    NECKLINE = "NECKLINE"
    SLEEVES = "SLEEVES"
    BACK = "BACK"
    TRAIN = "TRAIN"
    EMBELLISHMENT = "EMBELLISHMENT"
    MEASUREMENTS = "MEASUREMENTS"
    LENGTH = "LENGTH"
    SILHOUETTE = "SILHOUETTE"
    FULL_CUSTOM_DESIGN = "FULL_CUSTOM_DESIGN"


class ProductCustomization(Base, TimestampMixin):
    __tablename__ = "product_customizations"

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

    is_customizable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="customization",
    )

    options: Mapped[list["ProductCustomizationOption"]] = relationship(
        "ProductCustomizationOption",
        back_populates="customization",
        cascade="all, delete-orphan",
    )


class ProductCustomizationOption(Base, TimestampMixin):
    __tablename__ = "product_customization_options"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    customization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "product_customizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    option_type: Mapped[CustomizationOptionType] = mapped_column(
        SAEnum(
            CustomizationOptionType,
            name="customization_option_type",
        ),
        nullable=False,
    )

    details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    __table_args__ = (
        UniqueConstraint(
            "customization_id",
            "option_type",
            name="uq_product_customization_option",
        ),
        CheckConstraint(
            "sort_order >= 0",
            name="ck_product_customization_option_sort_order_non_negative",
        ),
    )
    customization: Mapped["ProductCustomization"] = relationship(
        "ProductCustomization",
        back_populates="options",
    )
