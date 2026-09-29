from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

import app.core.database.models
from app.core.models import RecordStatus
from app.modules.categories.service import CategoryService


@pytest.fixture
def uow():
    uow = Mock()

    uow.categories = Mock()
    uow.categories.exists_by_slug = AsyncMock()
    uow.categories.get_by_id = AsyncMock()
    uow.categories.get_by_slug = AsyncMock()
    uow.categories.list = AsyncMock()
    uow.categories.add = AsyncMock()
    uow.categories.delete = AsyncMock()

    uow.commit = AsyncMock()

    return uow


@pytest.mark.asyncio
async def test_create_category(uow):
    uow.categories.exists_by_slug.return_value = False

    service = CategoryService(uow)

    category = await service.create(
        name="Wedding Dress",
        description="Bridal wedding dresses",
    )

    assert category.name == "Wedding Dress"
    assert category.slug == "wedding-dress"
    assert category.description == "Bridal wedding dresses"
    assert category.status == RecordStatus.DRAFT

    uow.categories.exists_by_slug.assert_awaited_once_with("wedding-dress")
    uow.categories.add.assert_awaited_once_with(category)
    uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_category_fails_when_slug_exists(uow):
    uow.categories.exists_by_slug.return_value = True

    service = CategoryService(uow)

    with pytest.raises(
        ValueError,
        match="Category slug 'wedding-dress' already exists",
    ):
        await service.create(
            name="Wedding Dress",
        )

    uow.categories.add.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_by_id(uow):
    category_id = uuid4()
    category = Mock(id=category_id)

    uow.categories.get_by_id.return_value = category

    service = CategoryService(uow)

    result = await service.get_by_id(category_id)

    assert result is category

    uow.categories.get_by_id.assert_awaited_once_with(category_id)


@pytest.mark.asyncio
async def test_get_by_slug(uow):
    category = Mock()

    uow.categories.get_by_slug.return_value = category

    service = CategoryService(uow)

    result = await service.get_by_slug("wedding-dress")

    assert result is category

    uow.categories.get_by_slug.assert_awaited_once_with("wedding-dress")


@pytest.mark.asyncio
async def test_list(uow):
    categories = [Mock(), Mock()]

    uow.categories.list.return_value = categories

    service = CategoryService(uow)

    result = await service.list()

    assert result == categories

    uow.categories.list.assert_awaited_once_with(status=None)


@pytest.mark.asyncio
async def test_list_with_status(uow):
    categories = [Mock()]

    uow.categories.list.return_value = categories

    service = CategoryService(uow)

    result = await service.list(status=RecordStatus.PUBLISHED)

    assert result == categories

    uow.categories.list.assert_awaited_once_with(status=RecordStatus.PUBLISHED)


@pytest.mark.asyncio
async def test_delete(uow):
    category_id = uuid4()
    category = Mock(id=category_id)

    uow.categories.get_by_id.return_value = category

    service = CategoryService(uow)

    await service.delete(category_id)

    uow.categories.get_by_id.assert_awaited_once_with(category_id)
    uow.categories.delete.assert_awaited_once_with(category)
    uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_fails_when_category_does_not_exist(uow):
    category_id = uuid4()

    uow.categories.get_by_id.return_value = None

    service = CategoryService(uow)

    with pytest.raises(
        ValueError,
        match=f"Category '{category_id}' not found",
    ):
        await service.delete(category_id)

    uow.categories.delete.assert_not_awaited()
    uow.commit.assert_not_awaited()
