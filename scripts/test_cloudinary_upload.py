import asyncio

from app.core.storage.cloudinary import CloudinaryMediaStorage


async def test_verification():
    storage = CloudinaryMediaStorage()
    public_id = "yifan/test/500feff4-fc9b-41ce-874e-6717eefd8c16"

    # 1. Fetch metadata directly from Cloudinary Admin API
    metadata = await storage.get_asset_metadata(
        public_id=public_id,
        resource_type="image",
    )
    print("Metadata retrieved:")
    print(f"Format: {metadata.get('format')}")
    print(f"Width x Height: {metadata.get('width')}x{metadata.get('height')}")
    print(f"URL: {metadata.get('secure_url')}")

    # 2. Run your verification logic
    verified = await storage.verify_asset(
        public_id=public_id,
        resource_type="image",
        expected_mime_type="image/jpeg", # Change to match your test image format
    )
    print("\n✅ Asset verification passed!")
    print(f"Verified URL: {verified.secure_url}")

if __name__ == "__main__":
    asyncio.run(test_verification())