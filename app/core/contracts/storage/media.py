from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class SignedUpload:
    upload_url: str
    upload_params: dict[str, str]


@dataclass(frozen=True)
class VerifiedAsset:
    public_id: str
    resource_type: str
    mime_type: str | None
    file_size: int | None
    width: int | None
    height: int | None
    duration: int | None
    secure_url: str | None


from app.modules.media.model import MediaType


class AbstractMediaStorage(ABC):
    @abstractmethod
    async def create_signed_upload(
        self,
        *,
        public_id: str,
        media_type: MediaType,
        mime_type: str,
        expires_in: int,
    ) -> SignedUpload:
        raise NotImplementedError

    @abstractmethod
    async def get_asset_metadata(
        self,
        *,
        public_id: str,
        media_type: MediaType,
    ) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def delete_asset(
        self,
        *,
        public_id: str,
        media_type: MediaType,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def verify_asset(
        self,
        *,
        public_id: str,
        media_type: MediaType,
        expected_mime_type: str,
    ) -> VerifiedAsset:
        raise NotImplementedError
