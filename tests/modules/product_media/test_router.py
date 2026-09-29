from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import app.core.database.models
from app.modules.product_media.dependencies import (
    get_product_media_service,
)
from app.modules.product_media.dto import UploadIntent
from app.modules.product_media.model import ProductMedia
from app.modules.product_media.router import router


class FakeProductMediaService:
    def __init__(self):
        self.upload_intent_calls = []
        self.finalize_calls = []

        self.upload_intent_result = UploadIntent(
            media_asset_id=uuid4(),
            upload_session_id=uuid4(),
            storage_key="products/media/test/image.jpg",
            upload_url="/local-storage/upload/products/media/test/image.jpg",
        )

        self.finalize_result = None

    async def create_upload_intent(
        self,
        *,
        storage_provider: str,
        product_id: UUID,
        media_type: str,
        mime_type: str,
        original_filename: str | None = None,
        expires_in: int = 900,
    ) -> UploadIntent:
        self.upload_intent_calls.append(
            {
                "storage_provider": storage_provider,
                "product_id": product_id,
                "media_type": media_type,
                "mime_type": mime_type,
                "original_filename": original_filename,
                "expires_in": expires_in,
            }
        )

        return self.upload_intent_result

    async def finalize_upload(
        self,
        *,
        upload_session_id: UUID,
        alt_text: str | None = None,
        sort_order: int = 0,
        is_primary: bool = False,
    ):
        self.finalize_calls.append(
            {
                "upload_session_id": upload_session_id,
                "alt_text": alt_text,
                "sort_order": sort_order,
                "is_primary": is_primary,
            }
        )

        return self.finalize_result


@pytest.fixture
def fake_service():
    return FakeProductMediaService()


@pytest.fixture
def client(fake_service):
    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_product_media_service] = lambda: fake_service

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_create_upload_intent(client, fake_service):
    product_id = uuid4()

    response = client.post(
        f"/products/{product_id}/media/upload-intent",
        json={
            "media_type": "IMAGE",
            "mime_type": "image/jpeg",
            "original_filename": "front.jpg",
            "expires_in": 900,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["media_asset_id"] == str(
        fake_service.upload_intent_result.media_asset_id
    )
    assert data["upload_session_id"] == str(
        fake_service.upload_intent_result.upload_session_id
    )
    assert data["storage_key"] == ("products/media/test/image.jpg")
    assert data["upload_url"] == ("/local-storage/upload/products/media/test/image.jpg")

    assert fake_service.upload_intent_calls == [
        {
            "storage_provider": "local",
            "product_id": product_id,
            "media_type": "IMAGE",
            "mime_type": "image/jpeg",
            "original_filename": "front.jpg",
            "expires_in": 900,
        }
    ]


def test_create_upload_intent_uses_default_expiration(
    client,
    fake_service,
):
    product_id = uuid4()

    response = client.post(
        f"/products/{product_id}/media/upload-intent",
        json={
            "media_type": "IMAGE",
            "mime_type": "image/jpeg",
        },
    )

    assert response.status_code == 201

    assert fake_service.upload_intent_calls[0]["expires_in"] == 900


def test_create_upload_intent_rejects_invalid_expiration(
    client,
    fake_service,
):
    product_id = uuid4()

    response = client.post(
        f"/products/{product_id}/media/upload-intent",
        json={
            "media_type": "IMAGE",
            "mime_type": "image/jpeg",
            "expires_in": 0,
        },
    )

    assert response.status_code == 422
    assert fake_service.upload_intent_calls == []


def test_create_upload_intent_rejects_expiration_over_maximum(
    client,
    fake_service,
):
    product_id = uuid4()

    response = client.post(
        f"/products/{product_id}/media/upload-intent",
        json={
            "media_type": "IMAGE",
            "mime_type": "image/jpeg",
            "expires_in": 3601,
        },
    )

    assert response.status_code == 422
    assert fake_service.upload_intent_calls == []


def test_finalize_upload(client, fake_service):
    product_id = uuid4()
    media_asset_id = uuid4()
    upload_session_id = uuid4()
    product_media_id = uuid4()

    fake_service.finalize_result = ProductMedia(
        id=product_media_id,
        product_id=product_id,
        media_asset_id=media_asset_id,
        alt_text="Front view",
        sort_order=0,
        is_primary=True,
    )

    response = client.post(
        f"/products/media/uploads/{upload_session_id}/finalize",
        json={
            "alt_text": "Front view",
            "sort_order": 0,
            "is_primary": True,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data == {
        "id": str(product_media_id),
        "product_id": str(product_id),
        "media_asset_id": str(media_asset_id),
        "alt_text": "Front view",
        "sort_order": 0,
        "is_primary": True,
    }

    assert fake_service.finalize_calls == [
        {
            "upload_session_id": upload_session_id,
            "alt_text": "Front view",
            "sort_order": 0,
            "is_primary": True,
        }
    ]


def test_finalize_upload_rejects_negative_sort_order(
    client,
    fake_service,
):
    upload_session_id = uuid4()

    response = client.post(
        f"/products/media/uploads/{upload_session_id}/finalize",
        json={
            "alt_text": "Front view",
            "sort_order": -1,
            "is_primary": False,
        },
    )

    assert response.status_code == 422
    assert fake_service.finalize_calls == []


def test_finalize_upload_uses_defaults(
    client,
    fake_service,
):
    product_id = uuid4()
    media_asset_id = uuid4()
    upload_session_id = uuid4()
    product_media_id = uuid4()

    fake_service.finalize_result = ProductMedia(
        id=product_media_id,
        product_id=product_id,
        media_asset_id=media_asset_id,
        alt_text=None,
        sort_order=0,
        is_primary=False,
    )

    response = client.post(
        f"/products/media/uploads/{upload_session_id}/finalize",
        json={},
    )

    assert response.status_code == 201

    assert fake_service.finalize_calls == [
        {
            "upload_session_id": upload_session_id,
            "alt_text": None,
            "sort_order": 0,
            "is_primary": False,
        }
    ]
