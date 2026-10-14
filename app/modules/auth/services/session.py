import logging
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.core.contracts.services.auth_session import AbstractSessionService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.security.policies.session_policy import SessionPolicy
from app.modules.auth.dtos.session import SessionDTO
from app.modules.auth.exceptions import (
    SessionNotFoundError,
    UnauthorizedSessionAccessError,
)
from app.modules.auth.models.session import Session

logger = logging.getLogger(__name__)


# Session Service
class SessionService(AbstractSessionService):
    def __init__(self, uow: AbstractUnitOfWork, session_policy: SessionPolicy):

        self.uow = uow
        self.session_policy = session_policy

    async def create_session(
        self,
        *,
        user_id: UUID,
        device_name: str | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> SessionDTO:

        created_at = datetime.now(timezone.utc)

        session = Session(
            id=uuid4(),
            user_id=user_id,
            device_name=device_name,
            user_agent=user_agent,
            ip_address=ip_address,
            created_at=created_at,
            last_active_at=created_at,
            expires_at=self.session_policy.calculate_expiration(created_at=created_at),
        )

        session = await self.uow.auth_sessions.create(session)
        await self.uow.flush()

        return self._to_dto(session)

    async def get_session(self, *, session_id: UUID, user_id: UUID) -> SessionDTO:

        session = await self.uow.auth_sessions.get_by_id(session_id)

        if session is None:
            raise SessionNotFoundError(session_id)

        if session.user_id != user_id:
            raise UnauthorizedSessionAccessError(session_id)

        return self._to_dto(session)

    async def get_user_sessions(
        self,
        *,
        user_id: UUID,
    ) -> list[SessionDTO]:
        sessions = await self.uow.auth_sessions.get_user_sessions(user_id=user_id)

        return [self._to_dto(session) for session in sessions]

    async def revoke_session(
        self,
        *,
        session_id: UUID,
        user_id: UUID,
    ) -> None:
        session = await self.uow.auth_sessions.get_by_id_and_user(
            session_id=session_id, user_id=user_id
        )

        if session is None:
            raise SessionNotFoundError(session_id)

        if session.user_id != user_id:
            raise UnauthorizedSessionAccessError(session_id)

        if session.revoked_at is not None:
            return

        session.revoked_at = datetime.now(timezone.utc)

        self.uow.auth_sessions.revoke(session)

        await self.uow.flush()
        await self.uow.commit()

        logger.info(
            "Session revoked session_id=%s",
            session.id,
        )

        return self._to_dto(session)

    async def revoke_all_sessions(self, *, user_id: UUID) -> None:
        await self.uow.auth_sessions.revoke_all(user_id)
        logger.info(
            "User sessions revoked user_id=%s",
            user_id,
        )

    async def revoke_other_sessions(
        self,
        *,
        user_id: UUID,
        current_session_id: UUID,
    ) -> None:
        await self.uow.auth_sessions.revoke_other_sessions(
            user_id=user_id,
            current_session_id=current_session_id,
        )

    @staticmethod
    def _to_dto(session: Session) -> SessionDTO:
        return SessionDTO(
            id=session.id,
            device_name=session.device_name,
            user_agent=session.user_agent,
            ip_address=session.ip_address,
            created_at=session.created_at,
            last_active_at=session.last_active_at,
            expires_at=session.expires_at,
            revoked_at=session.revoked_at,
        )
