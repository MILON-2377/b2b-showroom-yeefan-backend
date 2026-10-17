from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.auth_refresh_token import (
    AbstractRefreshTokenRepository,
)
from app.modules.auth.models.refresh_token import RefreshToken


class RefreshTokenRepository(AbstractRefreshTokenRepository):
    def __init__(self, session: AsyncSession):

        self.session = session

    async def create(self, refresh_token: RefreshToken) -> RefreshToken:

        self.session.add(refresh_token)
        await self.session.flush()

        return refresh_token

    async def get_active_by_session_id(
        self,
        session_id: UUID,
    ) -> list[RefreshToken]:
        now = datetime.now(timezone.utc)

        statement = select(RefreshToken).where(
            RefreshToken.session_id == session_id,
            RefreshToken.revoked_at.is_(None),
            RefreshToken.expires_at > now,
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def get_by_id(self, jti: str) -> RefreshToken | None:

        statement = select(RefreshToken).where(RefreshToken.jti == jti)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:

        statement = select(RefreshToken).where(RefreshToken.token_hash == token_hash)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_active_by_token_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        now = datetime.now(timezone.utc)

        statement = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked_at.is_(None),
            RefreshToken.expires_at > now,
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_family(
        self,
        family_id: UUID,
    ) -> list[RefreshToken]:
        statement = (
            select(RefreshToken)
            .where(RefreshToken.family_id == family_id)
            .order_by(RefreshToken.created_at.asc())
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def revoke(
        self,
        refresh_token: RefreshToken,
    ) -> None:
        if refresh_token.revoked_at is not None:
            return

        refresh_token.revoked_at = datetime.now(timezone.utc)

        await self.session.flush()

    async def revoke_family(
        self,
        family_id: UUID,
    ) -> None:
        now = datetime.now(timezone.utc)

        statement = (
            update(RefreshToken)
            .where(
                RefreshToken.family_id == family_id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )

        await self.session.execute(statement)

    async def rotate(
        self,
        current_token: RefreshToken,
        replacement_token: RefreshToken,
    ) -> None:
        now = datetime.now(timezone.utc)

        current_token.revoked_at = now
        current_token.replaced_by_token_id = replacement_token.id

        self.session.add(replacement_token)

        await self.session.flush()

    async def update(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        await self.session.flush()

        return refresh_token

    async def get_by_session_id(
        self,
        session_id: UUID,
    ) -> list[RefreshToken]:
        statement = (
            select(RefreshToken)
            .where(RefreshToken.session_id == session_id)
            .order_by(RefreshToken.created_at.asc())
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def get_by_jti(self, jti: str) -> RefreshToken | None:

        statement = select(RefreshToken).where(RefreshToken.jti == jti)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_token_hash(self, token_hash: str) -> RefreshToken | None:

        statement = select(RefreshToken).where(RefreshToken.token_hash == token_hash)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()
