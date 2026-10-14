from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.auth_session import AbstractSessionRepository
from app.modules.auth.models.session import Session


class SessionRepository(AbstractSessionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, session: Session):

        self.session.add(session)
        await self.session.flush()
        return session

    async def get_by_id(self, session_id: UUID) -> Session | None:

        statement = select(Session).where(Session.id == session_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_active_by_id(
        self,
        session_id: UUID,
    ) -> Session | None:
        now = datetime.now(timezone.utc)

        statement = select(Session).where(
            Session.id == session_id,
            Session.revoked_at.is_(None),
            Session.expires_at > now,
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_id_and_user(
        self,
        *,
        session_id: UUID,
        user_id: UUID,
    ) -> Session | None:
        result = await self.session.execute(
            select(Session).where(
                Session.id == session_id,
                Session.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_user_sessions(
        self,
        *,
        user_id: UUID,
    ) -> list[Session]:
        result = await self.session.execute(
            select(Session)
            .where(Session.user_id == user_id)
            .order_by(Session.created_at.desc())
        )

        return list(result.scalars().all())

    async def get_active_sessions(self, user_id: UUID) -> list[Session]:

        now = datetime.now(timezone.utc)

        statement = (
            select(Session)
            .where(
                Session.user_id == user_id,
                Session.revoked_at.is_(None),
                Session.expires_at > now,
            )
            .order_by(Session.created_at.desc())
        )

        result = await self.session.execute(statement)

        return result.scalars().all()

    def revoke(self, session: Session) -> None:

        if session.revoked_at is not None:
            return

        session.revoked_at = datetime.now(timezone.utc)

    async def revoke_all(self, user_id: UUID) -> None:

        now = datetime.now(timezone.utc)

        statement = (
            update(Session)
            .where(
                Session.user_id == user_id,
                Session.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )

        await self.session.execute(statement)

    async def update_activity(
        self,
        session: Session,
    ) -> None:
        session.last_active_at = datetime.now(timezone.utc)

        await self.session.flush()

    async def update(
        self,
        session: Session,
    ) -> Session:
        await self.session.flush()

        return session

    async def revoke_other_sessions(
        self,
        *,
        user_id: UUID,
        current_session_id: UUID,
    ) -> None:
        stmt = (
            update(Session)
            .where(
                Session.user_id == user_id,
                Session.id != current_session_id,
                Session.revoked_at.is_(None),
            )
            .values(
                revoked_at=datetime.now(timezone.utc),
            )
        )

        await self.session.execute(stmt)
