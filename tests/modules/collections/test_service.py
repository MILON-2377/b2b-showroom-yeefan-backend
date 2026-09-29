from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

import app.core.database.models
from app.core.models import RecordStatus
from app.modules.collections.service import CollectionService


@pytest.fixture
def uow():
    uow = Mock()

    uow.brands = Mock()
    uow.brands.get_by_id = AsyncMock()

    uow.collections = Mock()
    uow.collections.exists_by_slug = AsyncMock()
    uow.collections.get_by_id = AsyncMock()
    uow.collections.get_by_slug = AsyncMock()
    uow.collections.list = AsyncMock()
    uow.collections.add = AsyncMock()
    uow.collections.delete = AsyncMock()

    uow.commit = AsyncMock()

    return uow


@pytest.mark.asyncio
async def test_create_collection(uow):
    brand_id = uuid4()

    brand = Mock(id=brand_id)
    uow.brands.get_by_id.return_value = brand
    uow.collections.exists_by_slug.return_value = False

    service = CollectionService(uow)

    collection = await service.create(
        brand_id=brand_id,
        name="Spring & Summer 2024",
        description="New collection",
        cover_media_url="https://example.com/cover.jpg",
    )

    assert collection.brand_id == brand_id
    assert collection.name == "Spring & Summer 2024"
    assert collection.slug == "spring-summer-2024"
    assert collection.description == "New collection"
    assert collection.cover_media_url == "https://example.com/cover.jpg"
    assert collection.status == RecordStatus.DRAFT

    uow.brands.get_by_id.assert_awaited_once_with(brand_id)

    uow.collections.exists_by_slug.assert_awaited_once_with(
        brand_id,
        "spring-summer-2024",
    )

    uow.collections.add.assert_awaited_once_with(collection)
    uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_collection_fails_when_brand_does_not_exist(uow):
    brand_id = uuid4()

    uow.brands.get_by_id.return_value = None

    service = CollectionService(uow)

    with pytest.raises(
        ValueError,
        match=f"Brand '{brand_id}' not found",
    ):
        await service.create(
            brand_id=brand_id,
            name="Spring & Summer 2024",
        )

    uow.collections.add.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_by_id(uow):
    collection_id = uuid4()
    collection = Mock(id=collection_id)

    uow.collections.get_by_id.return_value = collection

    service = CollectionService(uow)

    result = await service.get_by_id(collection_id)

    assert result is collection
    uow.collections.get_by_id.assert_awaited_once_with(collection_id)


@pytest.mark.asyncio
async def test_get_by_slug(uow):
    brand_id = uuid4()
    collection = Mock()

    uow.collections.get_by_slug.return_value = collection

    service = CollectionService(uow)

    result = await service.get_by_slug(
        brand_id,
        "spring-summer-2024",
    )

    assert result is collection
    uow.collections.get_by_slug.assert_awaited_once_with(
        brand_id,
        "spring-summer-2024",
    )


@pytest.mark.asyncio
async def test_list(uow):
    brand_id = uuid4()
    collections = [Mock(), Mock()]

    uow.collections.list.return_value = collections

    service = CollectionService(uow)

    result = await service.list(brand_id)

    assert result == collections
    uow.collections.list.assert_awaited_once_with(
        brand_id,
        status=None,
    )


@pytest.mark.asyncio
async def test_list_with_status(uow):
    brand_id = uuid4()
    collections = [Mock()]

    uow.collections.list.return_value = collections

    service = CollectionService(uow)

    result = await service.list(
        brand_id,
        status=RecordStatus.PUBLISHED,
    )

    assert result == collections
    uow.collections.list.assert_awaited_once_with(
        brand_id,
        status=RecordStatus.PUBLISHED,
    )


@pytest.mark.asyncio
async def test_delete(uow):
    collection_id = uuid4()
    collection = Mock(id=collection_id)

    uow.collections.get_by_id.return_value = collection

    service = CollectionService(uow)

    await service.delete(collection_id)

    uow.collections.get_by_id.assert_awaited_once_with(collection_id)
    uow.collections.delete.assert_awaited_once_with(collection)
    uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_fails_when_collection_does_not_exist(uow):
    collection_id = uuid4()

    uow.collections.get_by_id.return_value = None

    service = CollectionService(uow)

    with pytest.raises(
        ValueError,
        match=f"Collection '{collection_id}' not found",
    ):
        await service.delete(collection_id)

    uow.collections.delete.assert_not_awaited()
    uow.commit.assert_not_awaited()
