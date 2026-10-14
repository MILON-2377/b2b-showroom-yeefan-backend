from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.auth.models.user_profile import UserProfile


class AbstractUserProfileRepository(ABC):
    @abstractmethod
    async def create(
        self,
        profile: UserProfile,
    ) -> UserProfile:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        profile_id: UUID,
    ) -> UserProfile | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> UserProfile | None:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        profile: UserProfile,
    ) -> UserProfile:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        profile: UserProfile,
    ) -> None:
        raise NotImplementedError
