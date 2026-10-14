from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.auth.models.user import User, UserRole


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(
        self,
        user: User,
    ) -> User: ...

    @abstractmethod
    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None: ...

    @abstractmethod
    async def get_by_email(
        self,
        email: str,
    ) -> User | None: ...

    @abstractmethod
    async def update(
        self,
        user: User,
    ) -> User: ...

    @abstractmethod
    async def exists_by_email(
        self,
        email: str,
    ) -> bool: ...

    @abstractmethod
    async def list(
        self,
        *,
        role: UserRole | None = None,
        is_active: bool | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> list[User]: ...

    @abstractmethod
    async def count(
        self,
        *,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> int: ...

    @abstractmethod
    async def delete(
        self,
        user: User,
    ) -> None: ...
