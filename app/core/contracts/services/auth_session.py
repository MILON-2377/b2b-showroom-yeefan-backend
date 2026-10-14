from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.auth.dtos.session import SessionDTO


class AbstractSessionService(ABC):
    @abstractmethod
    async def create_session(
        self,
        *,
        user_id: UUID,
        device_name: str | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> SessionDTO: ...

    @abstractmethod
    async def get_session(
        self,
        *,
        session_id: UUID,
        user_id: UUID,
    ) -> SessionDTO: ...

    @abstractmethod
    async def get_user_sessions(
        self,
        *,
        user_id: UUID,
    ) -> list[SessionDTO]: ...

    @abstractmethod
    async def revoke_session(
        self,
        *,
        session_id: UUID,
        user_id: UUID,
    ) -> None: ...

    @abstractmethod
    async def revoke_all_sessions(
        self,
        *,
        user_id: UUID,
    ) -> None: ...

    @abstractmethod
    async def revoke_other_sessions(
        self,
        *,
        user_id: UUID,
        current_session_id: UUID,
    ) -> None: ...
