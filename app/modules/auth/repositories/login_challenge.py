from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.login_challenge import (
    AbstractLoginChallengeRepository,
)
from app.modules.auth.models.login_challenge import LoginChallenge


class LoginChallengeRepository(AbstractLoginChallengeRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id_for_update(
        self,
        *,
        challenge_id: UUID,
    ) -> LoginChallenge | None:
        statement = (
            select(LoginChallenge)
            .where(LoginChallenge.id == challenge_id)
            .with_for_update()
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        *,
        challenge_id: UUID,
    ) -> LoginChallenge | None:
        statement = select(LoginChallenge).where(
            LoginChallenge.id == challenge_id,
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def create(
        self,
        challenge: LoginChallenge,
    ) -> LoginChallenge:
        self.session.add(challenge)
        await self.session.flush()
        return challenge

    async def get_latest_active_by_user_id(
        self,
        *,
        user_id: UUID,
        now: datetime,
    ) -> LoginChallenge | None:
        statement = (
            select(LoginChallenge)
            .where(
                LoginChallenge.user_id == user_id,
                LoginChallenge.consumed_at.is_(None),
                LoginChallenge.expires_at > now,
            )
            .order_by(
                LoginChallenge.created_at.desc(),
                LoginChallenge.id.desc(),
            )
            .limit(1)
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def invalidate_active_by_user_id(
        self,
        *,
        user_id: UUID,
        now: datetime,
    ) -> None:
        statement = (
            update(LoginChallenge)
            .where(
                LoginChallenge.user_id == user_id,
                LoginChallenge.consumed_at.is_(None),
            )
            .values(consumed_at=now)
        )

        await self.session.execute(statement)
        await self.session.flush()

    async def update(
        self,
        challenge: LoginChallenge,
    ) -> LoginChallenge:
        self.session.add(challenge)
        await self.session.flush()
        return challenge
