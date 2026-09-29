from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest

import app.core.database.models
from app.core.storage.types import ObjectMetadata
from app.modules.media.model import (
    MediaAsset,
    MediaAssetStatus,
    UploadSession,
    UploadSessionStatus,
)
from app.modules.product_media.model import ProductMedia
from app.modules.product_media.service import ProductMediaService


class FakeMediaAssetRepository:
    def __init__(self):
        self.items = []

    def add(self, entity):
        if entity.id is None:
            entity.id = uuid4()

        self.items.append(entity)

    async def get_by_id(self, media_asset_id):
        for item in self.items:
            if item.id == media_asset_id:
                return item

        return None


class FakeUploadSessionRepository:
    def __init__(self):
        self.items = []

    async def get_by_id(self, upload_session_id):
        for item in self.items:
            if item.id == upload_session_id:
                return item

        return None

    def add(self, entity):
        if entity.id is None:
            entity.id = uuid4()

        self.items.append(entity)


class FakeProductMediaRepository:
    def __init__(self):
        self.items = []

    def add(self, entity):
        if entity.id is None:
            entity.id = uuid4()

        self.items.append(entity)


class FakeUnitOfWork:
    def __init__(self):
        self.media_assets = FakeMediaAssetRepository()
        self.upload_sessions = FakeUploadSessionRepository()
        self.product_media = FakeProductMediaRepository()

        self.flush_called = False
        self.commit_called = False
        self.rollback_called = False

    async def flush(self):
        self.flush_called = True

    async def commit(self):
        self.commit_called = True

    async def rollback(self):
        self.rollback_called = True


class FakeStorage:
    def __init__(self):
        self.calls = []
        self.metadata_calls = []

    async def create_presigned_upload_url(
        self,
        *,
        storage_key,
        mime_type,
        expires_in,
    ):
        self.calls.append(
            {
                "storage_key": storage_key,
                "mime_type": mime_type,
                "expires_in": expires_in,
            }
        )

        return f"/upload/{storage_key}"

    async def get_object_metadata(self, *, storage_key):
        self.metadata_calls.append(storage_key)

        return ObjectMetadata(
            storage_key=storage_key,
            mime_type="image/jpeg",
            size=123456,
        )


@pytest.mark.asyncio
async def test_create_upload_intent_creates_media_asset_and_upload_session():
    uow = FakeUnitOfWork()
    storage = FakeStorage()

    service = ProductMediaService(
        uow=uow,
        storage=storage,
    )

    product_id = uuid4()

    result = await service.create_upload_intent(
        storage_provider="local",
        product_id=product_id,
        media_type="IMAGE",
        mime_type="image/jpeg",
        original_filename="dress.jpg",
    )

    assert isinstance(result.media_asset_id, UUID)
    assert isinstance(result.upload_session_id, UUID)

    assert len(uow.media_assets.items) == 1
    assert len(uow.upload_sessions.items) == 1

    media_asset = uow.media_assets.items[0]
    upload_session = uow.upload_sessions.items[0]

    assert media_asset.id == result.media_asset_id
    assert media_asset.status == MediaAssetStatus.PENDING
    assert media_asset.storage_provider == "local"
    assert media_asset.mime_type == "image/jpeg"
    assert media_asset.original_filename == "dress.jpg"

    assert upload_session.id == result.upload_session_id
    assert upload_session.media_asset_id == media_asset.id
    assert upload_session.status == UploadSessionStatus.PENDING

    assert result.storage_key == media_asset.storage_key
    assert result.upload_url == (f"/upload/{media_asset.storage_key}")

    assert uow.flush_called is True
    assert uow.commit_called is True


@pytest.mark.asyncio
async def test_create_upload_intent_requests_storage_url_with_expected_values():
    uow = FakeUnitOfWork()
    storage = FakeStorage()

    service = ProductMediaService(
        uow=uow,
        storage=storage,
    )

    product_id = uuid4()

    result = await service.create_upload_intent(
        storage_provider="local",
        product_id=product_id,
        media_type="IMAGE",
        mime_type="image/png",
        original_filename="front.png",
        expires_in=600,
    )

    assert len(storage.calls) == 1

    call = storage.calls[0]

    assert call["storage_key"] == result.storage_key
    assert call["mime_type"] == "image/png"
    assert call["expires_in"] == 600


class FailingStorage(FakeStorage):
    async def create_presigned_upload_url(
        self,
        *,
        storage_key,
        mime_type,
        expires_in,
    ):
        raise RuntimeError("storage unavailable")


@pytest.mark.asyncio
async def test_create_upload_intent_propagates_storage_failure():
    uow = FakeUnitOfWork()
    storage = FailingStorage()

    service = ProductMediaService(
        uow=uow,
        storage=storage,
    )

    with pytest.raises(
        RuntimeError,
        match="storage unavailable",
    ):
        await service.create_upload_intent(
            storage_provider="local",
            product_id=uuid4(),
            media_type="IMAGE",
            mime_type="image/jpeg",
            original_filename="dress.jpg",
        )

    assert uow.commit_called is False


async def get_object_metadata(self, *, storage_key):
    self.metadata_calls = getattr(self, "metadata_calls", [])
    self.metadata_calls.append(storage_key)

    return ObjectMetadata(
        storage_key=storage_key,
        mime_type="image/jpeg",
        size=123456,
    )


@pytest.mark.asyncio
async def test_finalize_upload_marks_asset_ready_and_creates_product_media():
    uow = FakeUnitOfWork()
    storage = FakeStorage()

    product_id = uuid4()

    media_asset = MediaAsset(
        storage_provider="local",
        storage_key="products/media/test.jpg",
        media_type="IMAGE",
        mime_type="image/jpeg",
        original_filename="test.jpg",
        status=MediaAssetStatus.PENDING,
    )
    uow.media_assets.add(media_asset)

    upload_session = UploadSession(
        product_id=product_id,
        media_asset_id=media_asset.id,
        status=UploadSessionStatus.PENDING,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
    )
    uow.upload_sessions.add(upload_session)

    service = ProductMediaService(
        uow=uow,
        storage=storage,
    )

    result = await service.finalize_upload(
        upload_session_id=upload_session.id,
        alt_text="Front view",
        sort_order=0,
        is_primary=True,
    )

    assert isinstance(result, ProductMedia)

    assert result.product_id == product_id
    assert result.media_asset_id == media_asset.id
    assert result.alt_text == "Front view"
    assert result.sort_order == 0
    assert result.is_primary is True

    assert media_asset.status == MediaAssetStatus.READY
    assert media_asset.file_size == 123456

    assert upload_session.status == UploadSessionStatus.COMPLETED

    assert uow.commit_called is True


class MissingObjectStorage(FakeStorage):
    async def get_object_metadata(self, *, storage_key):
        return None


@pytest.mark.asyncio
async def test_finalize_upload_fails_when_object_does_not_exist():
    uow = FakeUnitOfWork()
    storage = MissingObjectStorage()

    product_id = uuid4()

    media_asset = MediaAsset(
        storage_provider="local",
        storage_key="products/media/missing.jpg",
        media_type="IMAGE",
        mime_type="image/jpeg",
        status=MediaAssetStatus.PENDING,
    )
    uow.media_assets.add(media_asset)

    upload_session = UploadSession(
        product_id=product_id,
        media_asset_id=media_asset.id,
        status=UploadSessionStatus.PENDING,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
    )
    uow.upload_sessions.add(upload_session)

    service = ProductMediaService(
        uow=uow,
        storage=storage,
    )

    with pytest.raises(
        ValueError,
        match="Uploaded object not found",
    ):
        await service.finalize_upload(
            upload_session_id=upload_session.id,
        )

    assert media_asset.status == MediaAssetStatus.PENDING
    assert upload_session.status == UploadSessionStatus.PENDING
    assert uow.commit_called is False


import mimetypes


class WrongMimeStorage(FakeStorage):
    async def get_object_metadata(
        self,
        *,
        storage_key,
    ):
        self.metadata_calls.append(storage_key)

        return ObjectMetadata(
            storage_key=storage_key,
            mime_type="image/png",
            size=123456,
        )


@pytest.mark.asyncio
async def test_finalize_upload_fails_when_mime_type_does_not_match():
    uow = FakeUnitOfWork()
    storage = WrongMimeStorage()

    product_id = uuid4()

    media_asset = MediaAsset(
        storage_provider="local",
        storage_key="products/media/test.jpg",
        media_type="IMAGE",
        mime_type="image/jpeg",
        original_filename="test.jpg",
        status=MediaAssetStatus.PENDING,
    )
    uow.media_assets.add(media_asset)

    upload_session = UploadSession(
        product_id=product_id,
        media_asset_id=media_asset.id,
        status=UploadSessionStatus.PENDING,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
    )
    uow.upload_sessions.add(upload_session)

    service = ProductMediaService(
        uow=uow,
        storage=storage,
    )

    with pytest.raises(
        ValueError,
        match="MIME type does not match",
    ):
        await service.finalize_upload(
            upload_session_id=upload_session.id,
        )

    assert media_asset.status == MediaAssetStatus.PENDING
    assert upload_session.status == UploadSessionStatus.PENDING
    assert len(uow.product_media.items) == 0
    assert uow.commit_called is False
