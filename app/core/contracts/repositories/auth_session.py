from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.auth.models.session import Session


class AbstractSessionRepository(ABC):
    @abstractmethod
    async def create(
        self,
        session: Session,
    ) -> Session: ...

    @abstractmethod
    async def get_by_id(
        self,
        session_id: UUID,
    ) -> Session | None: ...

    @abstractmethod
    async def get_by_id_and_user(
        self,
        *,
        session_id: UUID,
        user_id: UUID,
    ) -> Session | None: ...

    @abstractmethod
    async def get_active_by_id(
        self,
        session_id: UUID,
    ) -> Session | None: ...

    @abstractmethod
    async def get_user_sessions(
        self,
        user_id: UUID,
    ) -> list[Session]: ...

    @abstractmethod
    async def get_active_sessions(
        self,
        user_id: UUID,
    ) -> list[Session]: ...

    @abstractmethod
    async def revoke(
        self,
        session: Session,
    ) -> None: ...

    @abstractmethod
    async def revoke_all(
        self,
        user_id: UUID,
    ) -> None: ...

    @abstractmethod
    async def update_activity(
        self,
        session: Session,
    ) -> None: ...

    @abstractmethod
    async def update(
        self,
        session: Session,
    ) -> Session: ...

    @abstractmethod
    async def revoke_other_sessions(
        self,
        *,
        user_id: UUID,
        current_session_id: UUID,
    ) -> None: ...
