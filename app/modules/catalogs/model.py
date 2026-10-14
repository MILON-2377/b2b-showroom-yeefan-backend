from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, String, Text, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import RecordStatus, TimestampMixin

if TYPE_CHECKING:
    from app.modules.collections.model import Collection
    from app.modules.media.model import MediaAsset


class Catalog(Base, TimestampMixin):
    __tablename__ = "catalogs"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    collection_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "collections.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    pdf_media_asset_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "media_assets.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    cover_media_asset_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "media_assets.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    collection: Mapped["Collection"] = relationship(
        "Collection",
        back_populates="catalog",
    )

    status: Mapped[RecordStatus] = mapped_column(
        SqlEnum(RecordStatus, name="record_status"),
        nullable=False,
        default=RecordStatus.DRAFT,
        server_default=RecordStatus.DRAFT.value,
        index=True,
    )

    pdf_media_asset: Mapped["MediaAsset"] = relationship(
        "MediaAsset",
        foreign_keys=[pdf_media_asset_id],
    )

    cover_media_asset: Mapped["MediaAsset"] = relationship(
        "MediaAsset",
        foreign_keys=[cover_media_asset_id],
    )
