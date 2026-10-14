from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

import app.core.database.models
from app.core.models import RecordStatus
from app.modules.brands.model import Brand
from app.modules.brands.query import BrandListQuery
from app.modules.brands.repository import BrandRepository


@pytest.mark.asyncio
async def test_get_by_id_returns_brand():
    brand_id = uuid4()
    brand = Brand(
        id=brand_id,
        name="YEEFANS",
        slug="yeefans",
    )

    result = Mock()
    result.scalar_one_or_none.return_value = brand

    session = Mock()
    session.execute = AsyncMock(return_value=result)

    repository = BrandRepository(session)

    returned_brand = await repository.get_by_id(brand_id)

    assert returned_brand is brand
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_slug_returns_brand():
    brand = Brand(
        id=uuid4(),
        name="YEEFANS",
        slug="yeefans",
    )

    result = Mock()
    result.scalar_one_or_none.return_value = brand

    session = Mock()
    session.execute = AsyncMock(return_value=result)

    repository = BrandRepository(session)

    returned_brand = await repository.get_by_slug("yeefans")

    assert returned_brand is brand
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_returns_all_brands():
    brands = [
        Brand(id=uuid4(), name="YEEFANS", slug="yeefans"),
        Brand(id=uuid4(), name="Soiowar", slug="soiowar"),
    ]

    result = Mock()
    result.scalars.return_value.all.return_value = brands

    session = AsyncMock()
    session.execute = AsyncMock(return_value=result)

    repository = BrandRepository(session)

    returned_brands = await repository.list(BrandListQuery())

    assert returned_brands == [brands]
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_filters_by_status():
    brands = [
        Brand(
            id=uuid4(),
            name="YEEFANS",
            slug="yeefans",
            status=RecordStatus.PUBLISHED,
        )
    ]

    result = Mock()
    result.scalars.return_value.all.return_value = brands

    session = Mock()
    session.execute = AsyncMock(return_value=result)

    repository = BrandRepository(session)

    returned_brands = await repository.list(
        status=RecordStatus.PUBLISHED,
    )

    assert returned_brands == brands
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_exists_by_slug_returns_true_when_brand_exists():
    brand_id = uuid4()

    result = Mock()
    result.scalar_one_or_none.return_value = brand_id

    session = Mock()
    session.execute = AsyncMock(return_value=result)

    repository = BrandRepository(session)

    exists = await repository.exists_by_slug("yeefans")

    assert exists is True
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_exists_by_slug_returns_false_when_brand_does_not_exist():
    result = Mock()
    result.scalar_one_or_none.return_value = None

    session = Mock()
    session.execute = AsyncMock(return_value=result)

    repository = BrandRepository(session)

    exists = await repository.exists_by_slug("unknown")

    assert exists is False
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_add_adds_brand_to_session():
    session = Mock()

    repository = BrandRepository(session)

    brand = Brand(
        id=uuid4(),
        name="YEEFANS",
        slug="yeefans",
    )

    returned_brand = await repository.add(brand)

    assert returned_brand is brand
    session.add.assert_called_once_with(brand)


@pytest.mark.asyncio
async def test_delete_deletes_brand_from_session():
    session = Mock()
    session.delete = AsyncMock()

    repository = BrandRepository(session)

    brand = Brand(
        id=uuid4(),
        name="YEEFANS",
        slug="yeefans",
    )

    await repository.delete(brand)

    session.delete.assert_awaited_once_with(brand)


@pytest.mark.asyncio
async def test_list_returns_items_and_total(
    db_session,
):
    repository = BrandRepository(db_session)

    brand_1 = Brand(
        name="YEEFANS",
        slug="yeefans",
        status=RecordStatus.PUBLISHED,
    )
    brand_2 = Brand(
        name="Soiowar",
        slug="soiowar",
        status=RecordStatus.PUBLISHED,
    )

    db_session.add_all([brand_1, brand_2])
    await db_session.flush()

    result = await repository.list(BrandListQuery())

    assert result.total == 2
    assert len(result.items) == 2
    assert [brand.name for brand in result.items] == [
        "Soiowar",
        "YEEFANS",
    ]


@pytest.mark.asyncio
async def test_list_filters_by_status(
    db_session,
):
    repository = BrandRepository(db_session)

    db_session.add_all(
        [
            Brand(
                name="YEEFANS",
                slug="yeefans",
                status=RecordStatus.PUBLISHED,
            ),
            Brand(
                name="Soiowar",
                slug="soiowar",
                status=RecordStatus.DRAFT,
            ),
        ]
    )

    await db_session.flush()

    result = await repository.list(
        BrandListQuery(
            status=RecordStatus.PUBLISHED,
        )
    )

    assert result.total == 1
    assert len(result.items) == 1
    assert result.items[0].name == "YEEFANS"


@pytest.mark.asyncio
async def test_list_searches_by_name(
    db_session,
):
    repository = BrandRepository(db_session)

    db_session.add_all(
        [
            Brand(
                name="YEEFANS",
                slug="yeefans",
                status=RecordStatus.PUBLISHED,
            ),
            Brand(
                name="Soiowar",
                slug="soiowar",
                status=RecordStatus.PUBLISHED,
            ),
        ]
    )

    await db_session.flush()

    result = await repository.list(
        BrandListQuery(
            search="yee",
        )
    )

    assert result.total == 1
    assert len(result.items) == 1
    assert result.items[0].name == "YEEFANS"


@pytest.mark.asyncio
async def test_list_paginates_results(
    db_session,
):
    repository = BrandRepository(db_session)

    db_session.add_all(
        [
            Brand(
                name="Alpha",
                slug="alpha",
                status=RecordStatus.PUBLISHED,
            ),
            Brand(
                name="Beta",
                slug="beta",
                status=RecordStatus.PUBLISHED,
            ),
            Brand(
                name="Gamma",
                slug="gamma",
                status=RecordStatus.PUBLISHED,
            ),
        ]
    )

    await db_session.flush()

    result = await repository.list(
        BrandListQuery(
            page=2,
            page_size=2,
        )
    )

    assert result.total == 3
    assert len(result.items) == 1
    assert result.items[0].name == "Gamma"


@pytest.mark.asyncio
async def test_list_combines_search_and_status(
    db_session,
):
    repository = BrandRepository(db_session)

    db_session.add_all(
        [
            Brand(
                name="YEEFANS",
                slug="yeefans",
                status=RecordStatus.PUBLISHED,
            ),
            Brand(
                name="YEEFANS Draft",
                slug="yeefans-draft",
                status=RecordStatus.DRAFT,
            ),
            Brand(
                name="Soiowar",
                slug="soiowar",
                status=RecordStatus.PUBLISHED,
            ),
        ]
    )

    await db_session.flush()

    result = await repository.list(
        BrandListQuery(
            search="yee",
            status=RecordStatus.PUBLISHED,
        )
    )

    assert result.total == 1
    assert len(result.items) == 1
    assert result.items[0].name == "YEEFANS"
