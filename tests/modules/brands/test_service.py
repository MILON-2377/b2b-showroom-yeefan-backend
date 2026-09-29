from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

import app.core.database.models
from app.core.models import RecordStatus
from app.modules.brands.model import Brand
from app.modules.brands.service import BrandService


@pytest.fixture
def uow():
    uow = Mock()
    uow.brands = Mock()

    uow.brands.exists_by_slug = AsyncMock()
    uow.brands.get_by_id = AsyncMock()
    uow.brands.get_by_slug = AsyncMock()
    uow.brands.list = AsyncMock()
    uow.brands.add = AsyncMock()
    uow.brands.delete = AsyncMock()

    uow.commit = AsyncMock()

    return uow


@pytest.fixture
def service(uow):
    return BrandService(uow)


@pytest.mark.asyncio
async def test_create_brand_generates_slug(service, uow):
    uow.brands.exists_by_slug.return_value = False

    brand = await service.create(
        name="YEEFANS",
        description="Bridal fashion brand",
    )

    assert isinstance(brand, Brand)
    assert brand.name == "YEEFANS"
    assert brand.slug == "yeefans"
    assert brand.description == "Bridal fashion brand"
    assert brand.status == RecordStatus.DRAFT

    uow.brands.exists_by_slug.assert_awaited_once_with("yeefans")
    uow.brands.add.assert_awaited_once_with(brand)
    uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_brand_with_existing_slug_raises_error(service, uow):
    uow.brands.exists_by_slug.return_value = True

    with pytest.raises(
        ValueError,
        match="Brand slug 'yeefans' already exists",
    ):
        await service.create(name="YEEFANS")

    uow.brands.add.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_brand_by_id(service, uow):
    brand = Mock(spec=Brand)
    brand_id = uuid4()

    uow.brands.get_by_id.return_value = brand

    result = await service.get_by_id(brand_id)

    assert result is brand
    uow.brands.get_by_id.assert_awaited_once_with(brand_id)


@pytest.mark.asyncio
async def test_get_brand_by_slug(service, uow):
    brand = Mock(spec=Brand)

    uow.brands.get_by_slug.return_value = brand

    result = await service.get_by_slug("yeefans")

    assert result is brand
    uow.brands.get_by_slug.assert_awaited_once_with("yeefans")


@pytest.mark.asyncio
async def test_list_brands(service, uow):
    brands = [
        Mock(spec=Brand),
        Mock(spec=Brand),
    ]

    uow.brands.list.return_value = brands

    result = await service.list()

    assert result == brands
    uow.brands.list.assert_awaited_once_with(status=None)


@pytest.mark.asyncio
async def test_list_brands_with_status(service, uow):
    brands = [Mock(spec=Brand)]

    uow.brands.list.return_value = brands

    result = await service.list(status=RecordStatus.PUBLISHED)

    assert result == brands
    uow.brands.list.assert_awaited_once_with(status=RecordStatus.PUBLISHED)


@pytest.mark.asyncio
async def test_delete_brand(service, uow):
    brand = Mock(spec=Brand)
    brand_id = uuid4()

    uow.brands.get_by_id.return_value = brand

    await service.delete(brand_id)

    uow.brands.get_by_id.assert_awaited_once_with(brand_id)
    uow.brands.delete.assert_awaited_once_with(brand)
    uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_brand_not_found(service, uow):
    brand_id = uuid4()

    uow.brands.get_by_id.return_value = None

    with pytest.raises(
        ValueError,
        match=f"Brand '{brand_id}' not found",
    ):
        await service.delete(brand_id)

    uow.brands.delete.assert_not_awaited()
    uow.commit.assert_not_awaited()
