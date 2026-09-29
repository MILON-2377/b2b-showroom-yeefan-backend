from collections.abc import AsyncIterator
from pathlib import Path

import pytest

from app.core.storage.local import LocalObjectStorage


async def byte_stream(*chunks: bytes) -> AsyncIterator[bytes]:
    for chunk in chunks:
        yield chunk


@pytest.mark.asyncio
async def test_create_object_creates_new_object(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    storage_key = "products/media/product-123/image.jpg"

    await storage.create_object(
        storage_key=storage_key,
        data=byte_stream(b"hello ", b"world"),
        mime_type="image/jpeg",
    )

    path = tmp_path / storage_key

    assert path.is_file()
    assert path.read_bytes() == b"hello world"


@pytest.mark.asyncio
async def test_create_object_fails_if_object_already_exists(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    storage_key = "products/media/product-123/image.jpg"
    path = tmp_path / storage_key

    path.parent.mkdir(parents=True)
    path.write_bytes(b"existing")

    with pytest.raises(FileExistsError):
        await storage.create_object(
            storage_key=storage_key,
            data=byte_stream(b"new"),
            mime_type="image/jpeg",
        )

    assert path.read_bytes() == b"existing"


@pytest.mark.asyncio
async def test_upload_object_creates_object(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    storage_key = "products/media/product-123/image.jpg"

    await storage.upload_object(
        storage_key=storage_key,
        data=byte_stream(b"uploaded"),
        mime_type="image/jpeg",
    )

    path = tmp_path / storage_key

    assert path.is_file()
    assert path.read_bytes() == b"uploaded"


@pytest.mark.asyncio
async def test_upload_object_replaces_existing_object(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    storage_key = "products/media/product-123/image.jpg"
    path = tmp_path / storage_key

    path.parent.mkdir(parents=True)
    path.write_bytes(b"old content")

    await storage.upload_object(
        storage_key=storage_key,
        data=byte_stream(b"new content"),
        mime_type="image/jpeg",
    )

    assert path.read_bytes() == b"new content"


@pytest.mark.asyncio
async def test_update_object_replaces_existing_object(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    storage_key = "products/media/product-123/image.jpg"
    path = tmp_path / storage_key

    path.parent.mkdir(parents=True)
    path.write_bytes(b"old content")

    await storage.update_object(
        storage_key=storage_key,
        data=byte_stream(b"updated content"),
        mime_type="image/jpeg",
    )

    assert path.read_bytes() == b"updated content"


@pytest.mark.asyncio
async def test_update_object_fails_if_object_does_not_exist(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    storage_key = "products/media/product-123/missing.jpg"

    with pytest.raises(FileNotFoundError):
        await storage.update_object(
            storage_key=storage_key,
            data=byte_stream(b"content"),
            mime_type="image/jpeg",
        )


@pytest.mark.asyncio
async def test_get_object_streams_contents(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    storage_key = "products/media/product-123/image.jpg"
    path = tmp_path / storage_key

    path.parent.mkdir(parents=True)
    path.write_bytes(b"hello world")

    chunks = []

    async for chunk in storage.get_object(
        storage_key=storage_key,
    ):
        chunks.append(chunk)

    assert b"".join(chunks) == b"hello world"


@pytest.mark.asyncio
async def test_get_object_fails_if_object_does_not_exist(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    with pytest.raises(FileNotFoundError):
        async for _ in storage.get_object(
            storage_key="products/media/missing.jpg",
        ):
            pass


@pytest.mark.asyncio
async def test_get_object_metadata_returns_none_when_missing(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    result = await storage.get_object_metadata(
        storage_key="products/media/missing.jpg",
    )

    assert result is None


@pytest.mark.asyncio
async def test_get_object_metadata_returns_metadata(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    storage_key = "products/media/product-123/image.jpg"
    path = tmp_path / storage_key

    path.parent.mkdir(parents=True)
    path.write_bytes(b"hello world")

    result = await storage.get_object_metadata(
        storage_key=storage_key,
    )

    assert result is not None
    assert result.storage_key == storage_key
    assert result.mime_type == "application/octet-stream"
    assert result.size == 11


@pytest.mark.asyncio
async def test_delete_object_removes_existing_object(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    storage_key = "products/media/product-123/image.jpg"
    path = tmp_path / storage_key

    path.parent.mkdir(parents=True)
    path.write_bytes(b"content")

    await storage.delete_object(
        storage_key=storage_key,
    )

    assert not path.exists()


@pytest.mark.asyncio
async def test_delete_object_is_safe_when_missing(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    await storage.delete_object(
        storage_key="products/media/missing.jpg",
    )


@pytest.mark.asyncio
async def test_create_presigned_upload_url_creates_parent_directory(
    tmp_path: Path,
):
    storage = LocalObjectStorage(tmp_path)

    storage_key = "products/media/product-123/image.jpg"

    url = await storage.create_presigned_upload_url(
        storage_key=storage_key,
        mime_type="image/jpeg",
        expires_in=900,
    )

    assert url == f"/local-storage/upload/{storage_key}"

    expected_directory = tmp_path / "products" / "media" / "product-123"

    assert expected_directory.is_dir()
