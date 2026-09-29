from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, and_, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import RecordStatus, TimestampMixin

if TYPE_CHECKING:
    from app.modules.brands.model import Brand
    from app.modules.products.model import Product


class Collection(TimestampMixin, Base):
    __tablename__ = "collections"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    brand_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("brands.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    slug: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    cover_media_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[RecordStatus] = mapped_column(
        SqlEnum(RecordStatus, name="record_status"),
        nullable=False,
        default=RecordStatus.DRAFT,
    )

    __table_args__ = (
        UniqueConstraint(
            "brand_id",
            "slug",
            name="uq_collections_brand_slug",
        ),
        UniqueConstraint("id", "brand_id", name="uq_collections_id_brand"),
    )

    brand: Mapped["Brand"] = relationship(
        "Brand",
        back_populates="collections",
    )

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="collection",
        primaryjoin=(
            "and_("
            "Collection.id == Product.collection_id, "
            "Collection.brand_id == Product.brand_id"
            ")"
        ),
        foreign_keys="Product.collection_id",
    )
