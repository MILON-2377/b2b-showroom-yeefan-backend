from uuid import uuid4

from fastapi import APIRouter, File, UploadFile

from app.core.config import settings
from app.core.storage.cloudinary import CloudinaryMediaStorage

router = APIRouter(prefix="/storage", tags=["Storage"])


@router.post("/test-upload")
async def test_cloudinary_upload(
    file: UploadFile = File(...),
):
    storage = CloudinaryMediaStorage()

    public_id = f"yifan/test/{uuid4()}"

    # For this test, only support images.
    resource_type = "image"

    upload = await storage.create_signed_upload(
        public_id=public_id,
        resource_type=resource_type,
        upload_preset=settings.cloudinary_upload_preset,
        mime_type=file.content_type or "application/octet-stream",
        expires_in=900,
    )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "public_id": public_id,
        "upload_url": upload.upload_url,
        "upload_params": upload.upload_params,
    }
