from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.auth.dtos.auth import AuthTokensDTO
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.auth.dtos.login_challenge import LoginChallengeDTO
from app.modules.auth.models.user import User


class AbstractAuthService(ABC):
    @abstractmethod
    async def verify_login_code(
        self,
        *,
        challenge_id: UUID,
        code: str,
    ) -> AuthTokensDTO:
        raise NotImplementedError

    @abstractmethod
    async def register(
        self,
        *,
        email: str,
        password: str,
    ) -> User:
        raise NotImplementedError

    @abstractmethod
    async def login(
        self,
        email: str,
        password: str,
    ) -> LoginChallengeDTO:
        raise NotImplementedError

    @abstractmethod
    async def refresh(
        self,
        *,
        refresh_token: str,
    ) -> AuthTokensDTO:
        raise NotImplementedError

    @abstractmethod
    async def logout(
        self,
        *,
        refresh_token: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_current_user(
        self,
        *,
        access_token: str,
    ) -> AuthContext:
        raise NotImplementedError
