from uuid import UUID

from app.core.contracts.services.auth_session import AbstractSessionService
from app.core.contracts.services.user import AbstractUserService
from app.core.contracts.services.user_profile import AbstractUserProfileService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.security.password_manager import PasswordManager
from app.modules.auth.dtos.user import UserDTO, UserListDTO
from app.modules.auth.exceptions import (
    CannotDeactivateOwnAccountError,
    InvalidCredentialsError,
    UserEmailAlreadyExistsError,
    UserInactiveError,
    UserNotFoundError,
)
from app.modules.auth.models.user import User, UserRole


class UserService(AbstractUserService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        password_manager: PasswordManager,
        session_service: AbstractSessionService,
        user_profile_service: AbstractUserProfileService,
    ) -> None:
        self.uow = uow
        self.password_manager = password_manager
        self.session_service = session_service
        self.user_profile_service = user_profile_service

    @staticmethod
    def _to_dto(user: User) -> UserDTO:
        return UserDTO(
            id=user.id,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def create_admin(
        self,
        *,
        email: str,
        password: str,
    ) -> UserDTO:
        email = email.strip().lower()

        existing_user = await self.uow.users.get_by_email(email)

        if existing_user is not None:
            raise UserEmailAlreadyExistsError(email)

        password_hash = self.password_manager.hash_password(password)

        user = User(
            email=email,
            password_hash=password_hash,
            role=UserRole.ADMIN,
            is_active=True,
        )

        user = await self.uow.users.create(user)

        await self.user_profile_service.create_profile(user_id=user.id)

        await self.uow.commit()

        return self._to_dto(user)

    async def get_user(
        self,
        *,
        user_id: UUID,
    ) -> UserDTO:
        user = await self.uow.users.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        return self._to_dto(user)

    async def list_users(
        self,
        *,
        role: UserRole | None = None,
        is_active: bool | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> UserListDTO:

        offset = (page - 1) * page_size

        users = await self.uow.users.list(
            role=role, is_active=is_active, offset=offset, limit=page_size
        )

        total = await self.uow.users.count(role=role, is_active=is_active)

        return UserListDTO(
            items=[self._to_dto(user) for user in users],
            page=page,
            page_size=page_size,
            total=total,
        )

    async def update_user(
        self,
        *,
        user_id: UUID,
        email: str | None = None,
    ) -> UserDTO:
        user = await self.uow.users.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        if email is not None and email != user.email:
            existing_user = await self.uow.users.get_by_email(email)

            if existing_user is not None:
                raise UserEmailAlreadyExistsError(email)

            user.email = email

        user = await self.uow.users.update(user)

        await self.uow.commit()
        await self.uow.refresh(user)

        return self._to_dto(user)

    async def activate_user(
        self,
        *,
        user_id: UUID,
    ) -> UserDTO:
        user = await self.uow.users.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        user.is_active = True

        user = await self.uow.users.update(user)

        await self.uow.commit()
        await self.uow.refresh(user)

        return self._to_dto(user)

    async def deactivate_user(self, *, user_id: UUID, actor_user_id: UUID) -> UserDTO:

        if user_id == actor_user_id:
            raise CannotDeactivateOwnAccountError()

        user = await self.uow.users.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        user.is_active = False

        user = await self.uow.users.update(user)

        await self.uow.auth_sessions.revoke_all(user_id=user_id)

        await self.uow.commit()

        await self.uow.refresh(user)

        return self._to_dto(user)

    async def reset_password(
        self,
        *,
        user_id: UUID,
        password: str,
    ) -> None:
        user = await self.uow.users.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        user.password_hash = self.password_manager.hash_password(password)

        await self.uow.users.update(user)

        await self.uow.commit()

    async def change_password(
        self, *, user_id: UUID, current_password: str, new_password: str
    ) -> None:
        user = await self.uow.users.get_by_id(user_id)

        if not user.is_active:
            raise UserInactiveError()

        is_valid = self.password_manager.verify_password(
            current_password,
            user.password_hash,
        )

        if not is_valid:
            raise InvalidCredentialsError()

        user.password_hash = self.password_manager.hash_password(
            new_password,
        )

        await self.uow.users.update(user)
        await self.uow.commit()

    async def revoke_user_sessions(
        self,
        *,
        user_id: UUID,
    ) -> None:
        user = await self.uow.users.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        await self.session_service.revoke_all_sessions(
            user_id=user_id,
        )

        await self.uow.commit()
