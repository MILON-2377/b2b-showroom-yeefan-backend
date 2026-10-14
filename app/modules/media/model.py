from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.auth.models.user_profile import UserProfile
    from app.modules.categories.model import Category
    from app.modules.product_media.model import ProductMedia


class UploadSessionStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"


class MediaAssetStatus(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    FAILED = "FAILED"
    DELETION_PENDING = "DELETION_PENDING"
    DELETED = "DELETED"


class MediaType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    PDF = "PDF"


class MediaAsset(TimestampMixin, Base):
    __tablename__ = "media_assets"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    storage_provider: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    storage_key: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    secure_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    media_type: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    original_filename: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    file_size: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    width: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    height: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    duration: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[MediaAssetStatus] = mapped_column(
        SAEnum(MediaAssetStatus, name="media_asset_status"),
        nullable=False,
        default=MediaAssetStatus.PENDING,
    )

    __table_args__ = (
        UniqueConstraint(
            "storage_provider",
            "storage_key",
            name="uq_media_assets_provider_storage_key",
        ),
    )

    product_media: Mapped[list["ProductMedia"]] = relationship(
        "ProductMedia",
        back_populates="media_asset",
    )

    category_images: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="image_media",
        foreign_keys="Category.image_media_id",
    )

    upload_session: Mapped["UploadSession | None"] = relationship(
        back_populates="media_asset",
        uselist=False,
        cascade="all, delete-orphan",
    )

    user_profiles: Mapped[list["UserProfile"]] = relationship(
        "UserProfile",
        back_populates="avatar_media",
    )


class UploadSession(TimestampMixin, Base):
    __tablename__ = "upload_sessions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    media_asset_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "media_assets.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    status: Mapped[UploadSessionStatus] = mapped_column(
        SAEnum(
            UploadSessionStatus,
            name="upload_session_status",
        ),
        nullable=False,
        default=UploadSessionStatus.PENDING,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    media_asset: Mapped["MediaAsset"] = relationship(
        back_populates="upload_session",
    )
