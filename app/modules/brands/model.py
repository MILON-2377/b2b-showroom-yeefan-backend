from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import RecordStatus, TimestampMixin

if TYPE_CHECKING:
    from app.modules.collections.model import Collection
    from app.modules.products.model import Product


class Brand(TimestampMixin, Base):
    __tablename__ = "brands"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    slug: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    logo_media_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[RecordStatus] = mapped_column(
        SqlEnum(RecordStatus, name="record_status"),
        nullable=False,
        default=RecordStatus.DRAFT,
    )

    collections: Mapped[list["Collection"]] = relationship(
        "Collection", back_populates="brand"
    )

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="brand",
    )
