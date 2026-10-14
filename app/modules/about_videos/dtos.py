from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.core.models import RecordStatus


@dataclass(frozen=True, slots=True)
class CreateAboutVideoDTO:
    title: str
    media_asset_id: UUID
    description: str | None = None
    sort_order: int = 0
    status: RecordStatus = RecordStatus.DRAFT


@dataclass(frozen=True, slots=True)
class UpdateAboutVideoDTO:
    title: str | None = None
    description: str | None = None
    media_asset_id: UUID | None = None
    sort_order: int | None = None
    status: RecordStatus | None = None


@dataclass(frozen=True, slots=True)
class AboutVideoDTO:
    id: UUID
    title: str
    description: str | None
    media_asset_id: UUID
    video_url: str
    sort_order: int
    status: RecordStatus
    created_at: datetime
    updated_at: datetime
