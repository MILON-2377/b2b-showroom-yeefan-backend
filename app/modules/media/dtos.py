from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.media.model import MediaAssetStatus, MediaType


@dataclass(frozen=True)
class UploadIntent:
    media_asset_id: UUID
    upload_session_id: UUID
    storage_key: str
    upload_url: str
    upload_params: dict[str, str]


@dataclass(frozen=True)
class MediaAssetDeletionItem:
    id: UUID
    storage_key: str
    media_type: str


@dataclass(frozen=True)
class CreateUploadIntentDTO:
    storage_provider: str
    entity_id: UUID
    namespace: str
    media_type: MediaType
    mime_type: str
    original_filename: str | None = None
    expires_in: int = 900


@dataclass(frozen=True)
class CreateProductMediaDTO:
    media_asset_id: UUID
    alt_text: str | None = None
    sort_order: int = 0
    is_primary: bool = False


@dataclass(frozen=True)
class MediaAssetDTO:
    id: UUID
    storage_provider: str
    storage_key: str
    media_type: MediaType
    mime_type: str
    original_filename: str | None
    status: MediaAssetStatus
    secure_url: str | None
    file_size: int | None
    width: int | None
    height: int | None
    duration: float | None
    created_at: datetime
    updated_at: datetime
