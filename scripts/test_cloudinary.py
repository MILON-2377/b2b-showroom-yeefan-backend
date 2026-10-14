import asyncio
from uuid import uuid4

import cloudinary.api

from app.core.config import settings
from app.core.storage.cloudinary import CloudinaryMediaStorage


async def main() -> None:
    storage = CloudinaryMediaStorage()

    print("Testing connection to Cloudinary...")

    public_id = f"yifan/test/{uuid4()}"

    try:
        # Use cloudinary's built-in ping endpoint via asyncio.to_thread
        ping_response = await asyncio.to_thread(cloudinary.api.ping)
        print("✅ Connection successful!")
        print(f"Ping response: {ping_response}")  # Should return {'status': 'ok'}

    except Exception as e:
        print("❌ Cloudinary connection failed!")
        print(f"Error details: {e}")

    upload = await storage.create_signed_upload(
        public_id=public_id,
        resource_type="image",
        mime_type="image/jpeg",
        upload_preset=settings.cloudinary_upload_preset,
        expires_in=900,
    )

    print("\n=== SIGNED UPLOAD ===")
    print("Upload URL:", upload.upload_url)
    print("Upload params:")
    print(upload.upload_params)

    print("\n=== PUBLIC ID ===")
    print(public_id)

    print(
        "\nNow upload an image using the URL + params above, "
        "then run the metadata test."
    )


if __name__ == "__main__":
    asyncio.run(main())
