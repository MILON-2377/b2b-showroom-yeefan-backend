from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

import app.core.database.models  # noqa: F401
from app.core.models import RecordStatus
from app.modules.products.model import Product
from app.modules.products.repository import ProductRepository


@pytest.fixture
def session():
    return Mock()


@pytest.fixture
def repository(session):
    session.execute = AsyncMock()
    session.add = Mock()
    session.delete = AsyncMock()

    return ProductRepository(session)


@pytest.mark.asyncio
async def test_get_by_id(repository, session):
    product_id = uuid4()
    product = Mock(id=product_id)

    result = Mock()
    result.scalar_one_or_none.return_value = product

    session.execute.return_value = result

    found = await repository.get_by_id(product_id)

    assert found is product
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_product_code(repository, session):
    brand_id = uuid4()
    product = Mock()

    result = Mock()
    result.scalar_one_or_none.return_value = product

    session.execute.return_value = result

    found = await repository.get_by_product_code(
        brand_id,
        "K5892",
    )

    assert found is product
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_list(repository, session):
    products = [Mock(), Mock()]

    result = Mock()
    result.scalars.return_value.all.return_value = products

    session.execute.return_value = result

    found = await repository.list()

    assert found == products
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_with_filters(repository, session):
    brand_id = uuid4()
    collection_id = uuid4()
    category_id = uuid4()

    products = [Mock()]

    result = Mock()
    result.scalars.return_value.all.return_value = products

    session.execute.return_value = result

    found = await repository.list(
        brand_id=brand_id,
        collection_id=collection_id,
        category_id=category_id,
        status=RecordStatus.PUBLISHED,
    )

    assert found == products
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_exists_by_slug(repository, session):
    brand_id = uuid4()

    result = Mock()
    result.scalar_one_or_none.return_value = uuid4()

    session.execute.return_value = result

    exists = await repository.exists_by_slug(
        brand_id,
        "holy-girl",
    )

    assert exists is True
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_exists_by_slug_returns_false_when_missing(
    repository,
    session,
):
    brand_id = uuid4()

    result = Mock()
    result.scalar_one_or_none.return_value = None

    session.execute.return_value = result

    exists = await repository.exists_by_slug(
        brand_id,
        "holy-girl",
    )

    assert exists is False


@pytest.mark.asyncio
async def test_exists_by_product_code(repository, session):
    brand_id = uuid4()

    result = Mock()
    result.scalar_one_or_none.return_value = uuid4()

    session.execute.return_value = result

    exists = await repository.exists_by_product_code(
        brand_id,
        "K5892",
    )

    assert exists is True


@pytest.mark.asyncio
async def test_delete(repository, session):
    product = Mock()

    await repository.delete(product)

    session.delete.assert_awaited_once_with(product)
