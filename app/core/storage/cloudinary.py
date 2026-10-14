import asyncio

import cloudinary
import cloudinary.api
import cloudinary.utils
from cloudinary.exceptions import NotFound

from app.core.config import settings
from app.core.contracts.storage.media import (
    AbstractMediaStorage,
    SignedUpload,
    VerifiedAsset,
)
from app.modules.media.exceptions import UnsupportedMediaTypeError
from app.modules.media.model import MediaType


class CloudinaryAssetVerificationError(Exception):
    pass


_FORMAT_TO_MIME = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
    "gif": "image/gif",
    "avif": "image/avif",
    "mp4": "video/mp4",
    "webm": "video/webm",
    "mov": "video/quicktime",
    "pdf": "application/pdf",
}


_CLOUDINARY_RESOURCE_TYPES = {
    MediaType.IMAGE: "image",
    MediaType.VIDEO: "video",
    MediaType.PDF: "raw",
}


class CloudinaryMediaStorage(AbstractMediaStorage):
    def __init__(self) -> None:
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True,
        )

    @staticmethod
    def _get_resource_type(media_type: MediaType) -> str:
        try:
            return _CLOUDINARY_RESOURCE_TYPES[media_type]
        except KeyError as exc:
            raise UnsupportedMediaTypeError(media_type) from exc

    async def create_signed_upload(
        self,
        *,
        public_id: str,
        media_type: MediaType,
        mime_type: str,
        expires_in: int,
    ) -> SignedUpload:
        timestamp = int(__import__("time").time())

        cloudinary_resource_type = self._get_resource_type(media_type=media_type)

        params_to_sign = {
            "public_id": public_id,
            "timestamp": timestamp,
            "upload_preset": settings.cloudinary_upload_preset,
        }

        signature = cloudinary.utils.api_sign_request(
            params_to_sign,
            settings.cloudinary_api_secret,
        )

        upload_url = (
            f"https://api.cloudinary.com/v1_1/"
            f"{settings.cloudinary_cloud_name}/"
            f"{cloudinary_resource_type}/upload"
        )

        upload_params = {
            "public_id": public_id,
            "timestamp": str(timestamp),
            "upload_preset": settings.cloudinary_upload_preset,
            "api_key": settings.cloudinary_api_key,
            "signature": signature,
        }

        return SignedUpload(
            upload_url=upload_url,
            upload_params=upload_params,
        )

    async def get_asset_metadata(
        self,
        *,
        public_id: str,
        media_type: MediaType,
    ) -> dict:

        cloudinary_resource_type = self._get_resource_type(media_type)

        return await asyncio.to_thread(
            cloudinary.api.resource, public_id, resource_type=cloudinary_resource_type
        )

    async def delete_asset(
        self,
        *,
        public_id: str,
        media_type: MediaType,
    ) -> None:

        cloudinary_resource_type = self._get_resource_type(media_type)
        await asyncio.to_thread(
            cloudinary.api.delete_resources,
            [public_id],
            resource_type=cloudinary_resource_type,
        )

    async def verify_asset(
        self,
        *,
        public_id: str,
        media_type: MediaType,
        expected_mime_type: str,
    ) -> VerifiedAsset:
        cloudinary_resource_type = self._get_resource_type(media_type)

        try:
            metadata = await self.get_asset_metadata(
                public_id=public_id,
                media_type=media_type,
            )
        except NotFound as exc:
            raise CloudinaryAssetVerificationError(
                f"Cloudinary asset not found: {public_id}"
            ) from exc

        actual_public_id = metadata.get("public_id")
        actual_resource_type = metadata.get("resource_type")
        actual_format = metadata.get("format")

        if actual_public_id != public_id:
            raise CloudinaryAssetVerificationError(
                f"Public ID mismatch: expected={public_id!r}, "
                f"actual={actual_public_id!r}"
            )

        if actual_resource_type != cloudinary_resource_type:
            raise CloudinaryAssetVerificationError(
                f"Resource type mismatch: expected={cloudinary_resource_type!r}, "
                f"actual={actual_resource_type!r}"
            )

        actual_mime_type = _FORMAT_TO_MIME.get(actual_format)

        if actual_mime_type is None and media_type == MediaType.PDF:
            actual_mime_type = "application/pdf"

        if actual_mime_type != expected_mime_type:
            raise CloudinaryAssetVerificationError(
                f"MIME type mismatch: expected={expected_mime_type!r}, "
                f"actual_format={actual_format!r}, "
                f"actual_mime_type={actual_mime_type!r}"
            )

        return VerifiedAsset(
            public_id=actual_public_id,
            resource_type=actual_resource_type,
            mime_type=actual_mime_type,
            file_size=metadata.get("bytes"),
            width=metadata.get("width"),
            height=metadata.get("height"),
            duration=metadata.get("duration"),
            secure_url=metadata.get("secure_url"),
        )
