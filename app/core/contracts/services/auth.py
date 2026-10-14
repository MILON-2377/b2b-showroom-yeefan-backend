from abc import ABC, abstractmethod

from app.modules.auth.dtos.auth import AuthTokensDTO
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.auth.models.user import User


class AbstractAuthService(ABC):
    @abstractmethod
    async def register(
        self,
        *,
        email: str,
        password: str,
    ) -> User: ...

    @abstractmethod
    async def login(
        self,
        *,
        email: str,
        password: str,
        device_name: str | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> AuthTokensDTO: ...

    @abstractmethod
    async def refresh(
        self,
        *,
        refresh_token: str,
    ) -> AuthTokensDTO: ...

    @abstractmethod
    async def logout(
        self,
        *,
        refresh_token: str,
    ) -> None: ...

    @abstractmethod
    async def get_current_user(
        self,
        *,
        access_token: str,
    ) -> AuthContext: ...
