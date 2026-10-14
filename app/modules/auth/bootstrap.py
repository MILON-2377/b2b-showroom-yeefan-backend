from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.security.password_manager import PasswordManager
from app.modules.auth.models.user import User, UserRole
from app.modules.auth.services.user_profile import UserProfileService


async def bootstrap_super_admin(
    *,
    uow: AbstractUnitOfWork,
    password_manager: PasswordManager,
    email: str,
    password: str,
) -> None:
    email = email.strip().lower()

    existing_user = await uow.users.get_by_email(email)

    if existing_user is not None:
        raise RuntimeError(f"User with email '{email}' already exists.")

    password_hash = password_manager.hash_password(password)

    user = User(
        email=email,
        password_hash=password_hash,
        role=UserRole.SUPER_ADMIN,
        is_active=True,
    )

    user = await uow.users.create(user)


    await uow.user_profiles.create(
        user_id=user.id,
    )

    await uow.commit()
