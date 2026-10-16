from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.auth.models.refresh_token import RefreshToken


class AbstractRefreshTokenRepository(ABC):
    @abstractmethod
    async def get_active_by_session_id(
        self,
        session_id: UUID,
    ) -> list[RefreshToken]:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken: ...

    @abstractmethod
    async def get_by_id(
        self,
        token_id: UUID,
    ) -> RefreshToken | None: ...

    @abstractmethod
    async def get_by_jti(
        self,
        jti: str,
    ) -> RefreshToken | None: ...

    @abstractmethod
    async def get_by_token_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None: ...

    @abstractmethod
    async def get_active_by_token_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None: ...

    @abstractmethod
    async def get_family(
        self,
        family_id: UUID,
    ) -> list[RefreshToken]: ...

    @abstractmethod
    async def revoke(
        self,
        refresh_token: RefreshToken,
    ) -> None: ...

    @abstractmethod
    async def revoke_family(
        self,
        family_id: UUID,
    ) -> None: ...

    @abstractmethod
    async def rotate(
        self,
        current_token: RefreshToken,
        replacement_token: RefreshToken,
    ) -> None: ...

    @abstractmethod
    async def update(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken: ...

    @abstractmethod
    async def get_by_session_id(
        self,
        session_id: UUID,
    ) -> list[RefreshToken]: ...
