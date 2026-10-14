from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.contracts.repositories.user_profile import (
    AbstractUserProfileRepository,
)
from app.modules.auth.models.user_profile import UserProfile


class UserProfileRepository(AbstractUserProfileRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        profile: UserProfile,
    ) -> UserProfile:
        self.session.add(profile)
        await self.session.flush()
        await self.session.refresh(profile)

        return profile

    async def get_by_id(
        self,
        profile_id: UUID,
    ) -> UserProfile | None:
        statement = select(UserProfile).options(selectinload(UserProfile.avatar_media)).where(UserProfile.id == profile_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> UserProfile | None:
        statement = (
            select(UserProfile)
            .options(
                selectinload(UserProfile.avatar_media),
            )
            .where(UserProfile.user_id == user_id)
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def update(
        self,
        profile: UserProfile,
    ) -> UserProfile:
        self.session.add(profile)
        await self.session.flush()
        await self.session.refresh(profile)

        return profile

    async def delete(
        self,
        profile: UserProfile,
    ) -> None:
        await self.session.delete(profile)
        await self.session.flush()
