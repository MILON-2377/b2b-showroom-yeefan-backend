from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.shared.dependencies import get_uow


@pytest.mark.asyncio
async def test_get_uow_yields_unit_of_work():
    session = Mock()

    session_context = AsyncMock()
    session_context.__aenter__.return_value = session

    uow = Mock()

    uow_context = AsyncMock()
    uow_context.__aenter__.return_value = uow

    with (
        patch(
            "app.shared.dependencies.AsyncSessionLocal",
            return_value=session_context,
        ),
        patch(
            "app.shared.dependencies.UnitOfWork",
            return_value=uow_context,
        ),
    ):
        async for result in get_uow():
            assert result is uow

    session_context.__aenter__.assert_awaited_once()
    session_context.__aexit__.assert_awaited_once()

    uow_context.__aenter__.assert_awaited_once()
    uow_context.__aexit__.assert_awaited_once()
