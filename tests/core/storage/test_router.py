from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.storage.dependencies import get_object_storage
from app.core.storage.local import LocalObjectStorage
from app.core.storage.router import router


@pytest.fixture
def app(tmp_path: Path) -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    storage = LocalObjectStorage(tmp_path)

    async def override_storage():
        yield storage

    app.dependency_overrides[get_object_storage] = override_storage

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


def test_upload_file_returns_204(
    client: TestClient,
):
    response = client.put(
        "/local-storage/upload/products/media/product-123/image.jpg",
        content=b"hello world",
        headers={"content-type": "image/jpeg"},
    )

    assert response.status_code == 204
    assert response.content == b""


def test_upload_file_writes_object_to_storage(
    client: TestClient,
    tmp_path: Path,
):
    storage_key = "products/media/product-123/image.jpg"

    response = client.put(
        f"/local-storage/upload/{storage_key}",
        content=b"hello world",
        headers={"content-type": "image/jpeg"},
    )

    assert response.status_code == 204

    path = tmp_path / storage_key

    assert path.is_file()
    assert path.read_bytes() == b"hello world"


def test_upload_file_supports_nested_storage_key(
    client: TestClient,
    tmp_path: Path,
):
    storage_key = "products/media/product-123/gallery/2026/image-001.jpg"

    response = client.put(
        f"/local-storage/upload/{storage_key}",
        content=b"image content",
        headers={"content-type": "image/jpeg"},
    )

    assert response.status_code == 204

    path = tmp_path / storage_key

    assert path.is_file()
    assert path.read_bytes() == b"image content"


def test_upload_file_uses_default_content_type(
    client: TestClient,
    tmp_path: Path,
):
    storage_key = "products/media/product-123/file.bin"

    response = client.put(
        f"/local-storage/upload/{storage_key}",
        content=b"binary data",
    )

    assert response.status_code == 204

    path = tmp_path / storage_key

    assert path.is_file()
    assert path.read_bytes() == b"binary data"
