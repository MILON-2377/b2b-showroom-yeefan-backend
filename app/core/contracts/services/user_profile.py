from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from app.modules.auth.dtos.user_profile import UserProfileDTO


class AbstractUserProfileService(ABC):
    @abstractmethod
    async def create_profile(
        self,
        *,
        user_id: UUID,
        first_name: str | None = None,
        last_name: str | None = None,
        display_name: str | None = None,
        phone: str | None = None,
        job_title: str | None = None,
        bio: str | None = None,
        avatar_media_id: UUID | None = None,
    ) -> UserProfileDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> UserProfileDTO:
        raise NotImplementedError

    @abstractmethod
    async def update_profile(
        self,
        *,
        user_id: UUID,
        updates: dict[str, Any],
    ) -> UserProfileDTO:
        raise NotImplementedError
