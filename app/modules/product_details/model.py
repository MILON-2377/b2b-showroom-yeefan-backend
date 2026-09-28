from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.products.model import Product


class ProductDetail(TimestampMixin, Base):
    __tablename__ = "product_details"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    product_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    garment_type: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    silhouette: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    length: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    fabric: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    secondary_fabric: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    lining: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    neckline: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    back_style: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    waistline: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sleeve_type: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sleeve_length: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    train: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    embellishment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    closure: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    internal_support: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="details",
    )
