from abc import ABC, abstractmethod
from typing import Any


class AbstractDashboardRepository(ABC):

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def list_recent_inquiries(
        self,
        *,
        limit: int,
    ) -> list[Any]:
        raise NotImplementedError

    @abstractmethod
    async def list_recent_products(
        self,
        *,
        limit: int,
    ) -> list[Any]:
        raise NotImplementedError

    @abstractmethod
    async def list_pending_reviews(
        self,
        *,
        limit: int,
    ) -> list[Any]:
        raise NotImplementedError