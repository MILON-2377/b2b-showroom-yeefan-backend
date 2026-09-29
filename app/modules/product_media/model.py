from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.media.model import MediaAsset
    from app.modules.products.model import Product


class ProductMedia(TimestampMixin, Base):
    __tablename__ = "product_media"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    product_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    media_asset_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("media_assets.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    alt_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    __table_args__ = (
        CheckConstraint(
            "sort_order >= 0",
            name="ck_product_media_sort_order_non_negative",
        ),
        Index(
            "uq_product_media_primary",
            "product_id",
            unique=True,
            postgresql_where=text("is_primary = true"),
        ),
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="media",
    )

    media_asset: Mapped["MediaAsset"] = relationship(
        "MediaAsset",
        back_populates="product_media",
    )
