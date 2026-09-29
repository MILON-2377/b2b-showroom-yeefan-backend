import app.core.database.models  # noqa: F401

from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.core.models import RecordStatus
from app.modules.products.service import ProductService


@pytest.fixture
def uow():
    uow = Mock()

    uow.brands = Mock()
    uow.brands.get_by_id = AsyncMock()

    uow.collections = Mock()
    uow.collections.get_by_id = AsyncMock()

    uow.categories = Mock()
    uow.categories.get_by_id = AsyncMock()

    uow.products = Mock()
    uow.products.exists_by_product_code = AsyncMock()
    uow.products.exists_by_slug = AsyncMock()
    uow.products.get_by_id = AsyncMock()
    uow.products.get_by_slug = AsyncMock()
    uow.products.get_by_product_code = AsyncMock()
    uow.products.list = AsyncMock()
    uow.products.add = AsyncMock()
    uow.products.delete = AsyncMock()

    uow.commit = AsyncMock()

    return uow


@pytest.mark.asyncio
async def test_create_product(uow):
    brand_id = uuid4()
    collection_id = uuid4()
    category_id = uuid4()

    brand = Mock(id=brand_id)
    collection = Mock(
        id=collection_id,
        brand_id=brand_id,
    )
    category = Mock(id=category_id)

    uow.brands.get_by_id.return_value = brand
    uow.collections.get_by_id.return_value = collection
    uow.categories.get_by_id.return_value = category
    uow.products.exists_by_product_code.return_value = False
    uow.products.exists_by_slug.return_value = False

    service = ProductService(uow)

    product = await service.create(
        brand_id=brand_id,
        collection_id=collection_id,
        category_id=category_id,
        product_code="K5892",
        name="Holy Girl",
        description="Bridal collection design",
    )

    assert product.brand_id == brand_id
    assert product.collection_id == collection_id
    assert product.category_id == category_id
    assert product.product_code == "K5892"
    assert product.name == "Holy Girl"
    assert product.slug == "holy-girl"
    assert product.description == "Bridal collection design"
    assert product.status == RecordStatus.DRAFT

    uow.products.add.assert_awaited_once_with(product)
    uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_product_fails_when_brand_does_not_exist(uow):
    brand_id = uuid4()

    uow.brands.get_by_id.return_value = None

    service = ProductService(uow)

    with pytest.raises(
        ValueError,
        match=f"Brand '{brand_id}' not found",
    ):
        await service.create(
            brand_id=brand_id,
            collection_id=uuid4(),
            category_id=uuid4(),
            product_code="K5892",
            name="Holy Girl",
        )

    uow.products.add.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_product_fails_when_collection_does_not_exist(
    uow,
):
    brand_id = uuid4()
    collection_id = uuid4()

    uow.brands.get_by_id.return_value = Mock(id=brand_id)
    uow.collections.get_by_id.return_value = None

    service = ProductService(uow)

    with pytest.raises(
        ValueError,
        match=f"Collection '{collection_id}' not found",
    ):
        await service.create(
            brand_id=brand_id,
            collection_id=collection_id,
            category_id=uuid4(),
            product_code="K5892",
            name="Holy Girl",
        )

    uow.products.add.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_product_fails_when_collection_belongs_to_another_brand(
    uow,
):
    brand_id = uuid4()
    other_brand_id = uuid4()
    collection_id = uuid4()

    uow.brands.get_by_id.return_value = Mock(id=brand_id)

    uow.collections.get_by_id.return_value = Mock(
        id=collection_id,
        brand_id=other_brand_id,
    )

    service = ProductService(uow)

    with pytest.raises(
        ValueError,
        match=(f"Collection '{collection_id}' does not belong to brand '{brand_id}'"),
    ):
        await service.create(
            brand_id=brand_id,
            collection_id=collection_id,
            category_id=uuid4(),
            product_code="K5892",
            name="Holy Girl",
        )

    uow.categories.get_by_id.assert_not_awaited()
    uow.products.add.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_product_fails_when_category_does_not_exist(
    uow,
):
    brand_id = uuid4()
    collection_id = uuid4()
    category_id = uuid4()

    uow.brands.get_by_id.return_value = Mock(id=brand_id)

    uow.collections.get_by_id.return_value = Mock(
        id=collection_id,
        brand_id=brand_id,
    )

    uow.categories.get_by_id.return_value = None

    service = ProductService(uow)

    with pytest.raises(
        ValueError,
        match=f"Category '{category_id}' not found",
    ):
        await service.create(
            brand_id=brand_id,
            collection_id=collection_id,
            category_id=category_id,
            product_code="K5892",
            name="Holy Girl",
        )

    uow.products.add.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_product_fails_when_product_code_exists(
    uow,
):
    brand_id = uuid4()
    collection_id = uuid4()
    category_id = uuid4()

    uow.brands.get_by_id.return_value = Mock(id=brand_id)

    uow.collections.get_by_id.return_value = Mock(
        id=collection_id,
        brand_id=brand_id,
    )

    uow.categories.get_by_id.return_value = Mock(id=category_id)

    uow.products.exists_by_product_code.return_value = True

    service = ProductService(uow)

    with pytest.raises(
        ValueError,
        match=(f"Product code 'K5892' already exists for brand '{brand_id}'"),
    ):
        await service.create(
            brand_id=brand_id,
            collection_id=collection_id,
            category_id=category_id,
            product_code="K5892",
            name="Holy Girl",
        )

    uow.products.exists_by_slug.assert_not_awaited()
    uow.products.add.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_product_fails_when_slug_exists(
    uow,
):
    brand_id = uuid4()
    collection_id = uuid4()
    category_id = uuid4()

    uow.brands.get_by_id.return_value = Mock(id=brand_id)

    uow.collections.get_by_id.return_value = Mock(
        id=collection_id,
        brand_id=brand_id,
    )

    uow.categories.get_by_id.return_value = Mock(id=category_id)

    uow.products.exists_by_product_code.return_value = False
    uow.products.exists_by_slug.return_value = True

    service = ProductService(uow)

    with pytest.raises(
        ValueError,
        match=(f"Product slug 'holy-girl' already exists for brand '{brand_id}'"),
    ):
        await service.create(
            brand_id=brand_id,
            collection_id=collection_id,
            category_id=category_id,
            product_code="K5892",
            name="Holy Girl",
        )

    uow.products.add.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_by_id(uow):
    product_id = uuid4()
    product = Mock(id=product_id)

    uow.products.get_by_id.return_value = product

    service = ProductService(uow)

    result = await service.get_by_id(product_id)

    assert result is product
    uow.products.get_by_id.assert_awaited_once_with(product_id)


@pytest.mark.asyncio
async def test_get_by_product_code(uow):
    brand_id = uuid4()
    product = Mock()

    uow.products.get_by_product_code.return_value = product

    service = ProductService(uow)

    result = await service.get_by_product_code(
        brand_id,
        "K5892",
    )

    assert result is product
    uow.products.get_by_product_code.assert_awaited_once_with(
        brand_id,
        "K5892",
    )


@pytest.mark.asyncio
async def test_list_with_filters(uow):
    brand_id = uuid4()
    collection_id = uuid4()
    category_id = uuid4()

    products = [Mock()]

    uow.products.list.return_value = products

    service = ProductService(uow)

    result = await service.list(
        brand_id=brand_id,
        collection_id=collection_id,
        category_id=category_id,
        status=RecordStatus.PUBLISHED,
    )

    assert result == products

    uow.products.list.assert_awaited_once_with(
        brand_id=brand_id,
        collection_id=collection_id,
        category_id=category_id,
        status=RecordStatus.PUBLISHED,
    )


@pytest.mark.asyncio
async def test_delete(uow):
    product_id = uuid4()
    product = Mock(id=product_id)

    uow.products.get_by_id.return_value = product

    service = ProductService(uow)

    await service.delete(product_id)

    uow.products.get_by_id.assert_awaited_once_with(product_id)
    uow.products.delete.assert_awaited_once_with(product)
    uow.commit.assert_awaited_once()
