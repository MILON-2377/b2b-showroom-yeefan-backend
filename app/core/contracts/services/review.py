from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.reviews.dtos import (
    CreateReviewDTO,
    PublicReviewListDTO,
    ReviewDTO,
    ReviewListDTO,
    UpdateReviewDTO,
    UpdateReviewNotesDTO,
    UpdateReviewStatusDTO,
)


class AbstractReviewService(ABC):
    @abstractmethod
    async def create(self, payload: CreateReviewDTO) -> ReviewDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, review_id: UUID) -> ReviewDTO:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        *,
        status: object | None,
        page: int,
        page_size: int,
    ) -> ReviewListDTO:
        raise NotImplementedError

    @abstractmethod
    async def list_public(
        self,
        *,
        page: int,
        page_size: int,
    ) -> PublicReviewListDTO:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        review_id: UUID,
        payload: UpdateReviewDTO,
    ) -> ReviewDTO:
        raise NotImplementedError

    @abstractmethod
    async def update_status(
        self,
        review_id: UUID,
        payload: UpdateReviewStatusDTO,
    ) -> ReviewDTO:
        raise NotImplementedError

    @abstractmethod
    async def update_notes(
        self,
        review_id: UUID,
        payload: UpdateReviewNotesDTO,
    ) -> ReviewDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, review_id: UUID) -> None:
        raise NotImplementedError
