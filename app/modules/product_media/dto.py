from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UploadIntent:
    media_asset_id: UUID
    upload_session_id: UUID
    storage_key: str
    upload_url: str
