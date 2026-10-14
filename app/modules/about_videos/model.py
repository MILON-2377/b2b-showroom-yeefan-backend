from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text, func, text
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import RecordStatus, TimestampMixin
from app.modules.media.model import MediaAsset


class AboutVideo(TimestampMixin, Base):
    __tablename__ = "about_videos"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    media_asset_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "media_assets.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )

    status: Mapped[RecordStatus] = mapped_column(
        PG_ENUM(
            RecordStatus,
            name="record_status",
            create_type=False,
        ),
        nullable=False,
        default=RecordStatus.DRAFT,
        server_default=text("'DRAFT'"),
    )

    media_asset: Mapped["MediaAsset"] = relationship()
