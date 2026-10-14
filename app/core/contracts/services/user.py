from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.auth.dtos.user import UserDTO, UserListDTO
from app.modules.auth.models.user import UserRole


class AbstractUserService(ABC):
    @abstractmethod
    async def create_admin(
        self,
        *,
        email: str,
        password: str,
    ) -> UserDTO: ...

    @abstractmethod
    async def get_user(
        self,
        *,
        user_id: UUID,
    ) -> UserDTO: ...

    @abstractmethod
    async def list_users(
        self,
        *,
        role: UserRole | None = None,
        is_active: bool | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> UserListDTO: ...

    @abstractmethod
    async def update_user(
        self,
        *,
        user_id: UUID,
        email: str | None = None,
    ) -> UserDTO: ...

    @abstractmethod
    async def activate_user(
        self,
        *,
        user_id: UUID,
    ) -> UserDTO: ...

    @abstractmethod
    async def deactivate_user(
        self,
        *,
        user_id: UUID,
        actor_user_id: UUID
    ) -> UserDTO: ...

    @abstractmethod
    async def reset_password(
        self,
        *,
        user_id: UUID,
        password: str,
    ) -> None: ...

    @abstractmethod
    async def change_password(
        self,
        *,
        user_id: UUID,
        current_password: str,
        new_password: str,
    ) -> None: ...

    @abstractmethod
    async def revoke_user_sessions(
        self,
        *,
        user_id: UUID,
    ) -> None: ...
