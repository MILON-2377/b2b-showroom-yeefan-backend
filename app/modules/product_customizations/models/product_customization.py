import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.product_customizations.models.product_customization_option import (
        ProductCustomizationOption,
    )
    from app.modules.products.model import Product


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
