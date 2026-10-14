import asyncio
import getpass

from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.database.session import AsyncSessionLocal
from app.core.database.unit_of_work import UnitOfWork
from app.core.security.password_manager import PasswordManager
from app.modules.auth.bootstrap import bootstrap_super_admin
from app.modules.auth.models.user import User, UserRole
from app.modules.auth.services.user_profile import UserProfileService
from app.modules.media.dependencies import get_media_upload_service


async def bootstrap_super_admin(
    *,
    uow: AbstractUnitOfWork,
    password_manager: PasswordManager,
    email: str,
    password: str,
    media_service: AbstractMediaUploadService,
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

    user_profile_service = UserProfileService(uow=uow, media_service=media_service)

    await user_profile_service.create_profile(
        user_id=user.id,
    )

    await uow.commit()

    print(f"Super admin created: {email}")


async def main() -> None:
    email = input("Super admin email: ").strip()

    password = getpass.getpass("Super admin password: ")
    password_confirmation = getpass.getpass("Confirm super admin password: ")

    if password != password_confirmation:
        raise ValueError("Passwords do not match.")

    if not password:
        raise ValueError("Password cannot be empty.")

    password_manager = PasswordManager()

    async with AsyncSessionLocal() as session:
        uow = UnitOfWork(session)

        async with uow:
            await bootstrap_super_admin(
                uow=uow,
                password_manager=password_manager,
                email=email,
                password=password,
                media_service=get_media_upload_service,
            )

    print(f"Super admin created: {email}")


if __name__ == "__main__":
    asyncio.run(main())
