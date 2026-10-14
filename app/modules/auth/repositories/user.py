from uuid import UUID

from sqlalchemy import exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.user import AbstractUserRepository
from app.modules.auth.models.user import User, UserRole


class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):

        self.session = session

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:

        statement = select(User).where(User.id == user_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:

        statement = select(User).where(User.email == email)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def update(
        self,
        user: User,
    ) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def exists_by_email(self, email) -> bool:
        statement = select(exists().where(User.email == email))

        result = await self.session.execute(statement)

        return result.scalar_one()

    async def list(
        self,
        *,
        role: UserRole | None = None,
        is_active: bool | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> list[User]:
        statement = select(User)

        if role is not None:
            statement = statement.where(User.role == role)

        if is_active is not None:
            statement = statement.where(User.is_active == is_active)

        statement = (
            statement.order_by(User.created_at.desc()).offset(offset).limit(limit)
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def count(
        self,
        *,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> int:
        statement = select(func.count(User.id))

        if role is not None:
            statement = statement.where(User.role == role)

        if is_active is not None:
            statement = statement.where(User.is_active == is_active)

        result = await self.session.execute(statement)

        return result.scalar_one()

    async def delete(
        self,
        user: User,
    ) -> None:
        await self.session.delete(user)
        await self.session.flush()
