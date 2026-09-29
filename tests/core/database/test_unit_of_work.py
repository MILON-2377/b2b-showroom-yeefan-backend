from unittest.mock import AsyncMock, Mock

import pytest

from app.core.database.unit_of_work import UnitOfWork
from app.modules.brands.repository import BrandRepository


@pytest.mark.asyncio
async def test_uow_starts_transaction():
    session = Mock()
    session.in_transaction.return_value = False
    session.begin = AsyncMock()
    session.close = AsyncMock()

    uow = UnitOfWork(session)

    async with uow:
        pass

    session.begin.assert_awaited_once()
    session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_uow_does_not_start_existing_transaction():
    session = Mock()
    session.in_transaction.return_value = True
    session.begin = AsyncMock()
    session.close = AsyncMock()

    uow = UnitOfWork(session)

    async with uow:
        pass

    session.begin.assert_not_awaited()
    session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_uow_commits():
    session = Mock()
    session.in_transaction.return_value = False
    session.begin = AsyncMock()
    session.commit = AsyncMock()
    session.close = AsyncMock()

    uow = UnitOfWork(session)

    async with uow:
        await uow.commit()

    session.commit.assert_awaited_once()
    session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_uow_rolls_back_on_exception():
    session = Mock()
    session.in_transaction.return_value = False
    session.begin = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()

    uow = UnitOfWork(session)

    with pytest.raises(ValueError):
        async with uow:
            raise ValueError("something failed")

    session.rollback.assert_awaited_once()
    session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_uow_closes_session():
    session = Mock()
    session.in_transaction.return_value = False
    session.begin = AsyncMock()
    session.close = AsyncMock()

    uow = UnitOfWork(session)

    async with uow:
        pass

    session.close.assert_awaited_once()


def test_uow_lazily_creates_brand_repository():
    session = Mock()

    uow = UnitOfWork(session)

    first_repository = uow.brands
    second_repository = uow.brands

    assert isinstance(first_repository, BrandRepository)
    assert first_repository is second_repository
    assert first_repository.session is session
