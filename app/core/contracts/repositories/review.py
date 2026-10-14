from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.reviews.model import Review


class AbstractReviewRepository(ABC):
    @abstractmethod
    async def create(
        self,
        review: Review,
    ) -> Review:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        review_id: UUID,
    ) -> Review | None:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        *,
        status: object | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Review], int]:
        raise NotImplementedError

    @abstractmethod
    async def list_public(
        self,
        *,
        page: int,
        page_size: int,
    ) -> tuple[list[Review], int]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        review: Review,
    ) -> Review:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        review: Review,
    ) -> None:
        raise NotImplementedError
