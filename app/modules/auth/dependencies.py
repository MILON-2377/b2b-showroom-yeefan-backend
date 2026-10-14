from typing import Annotated

from fastapi import Depends, Request

from app.core.config import settings
from app.core.contracts.security.jwt_manager import AbstractJwtManager
from app.core.contracts.services.auth import AbstractAuthService
from app.core.contracts.services.auth_session import AbstractSessionService
from app.core.contracts.services.cookie import AbstractCookieService
from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.services.token import AbstractTokenService
from app.core.contracts.services.user import AbstractUserService
from app.core.contracts.services.user_profile import AbstractUserProfileService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.security.jwt_manager import JwtManager
from app.core.security.password_manager import PasswordManager
from app.core.security.policies.cookie import CookiePolicy
from app.core.security.policies.session_policy import SessionPolicy
from app.core.security.policies.token_policy import TokenPolicy
from app.core.security.token_hasher import (
    AbstractTokenHasher,
    TokenHasher,
)
from app.modules.auth.cookie import CookieService
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.auth.exceptions import (
    InsufficientPermissionsError,
    InvalidAccessTokenError,
)
from app.modules.auth.models.user import UserRole
from app.modules.auth.services.auth import AuthService
from app.modules.auth.services.refresh_token import TokenService
from app.modules.auth.services.session import SessionService
from app.modules.auth.services.user import UserService
from app.modules.auth.services.user_profile import UserProfileService
from app.modules.media.dependencies import get_media_upload_service
from app.shared.dependencies import get_uow


def get_password_manager() -> PasswordManager:
    return PasswordManager()


def get_jwt_manager() -> AbstractJwtManager:
    return JwtManager()


def get_token_hasher() -> AbstractTokenHasher:
    return TokenHasher()


def get_token_policy() -> TokenPolicy:
    return TokenPolicy(security_settings=settings)


def get_session_policy() -> SessionPolicy:
    return SessionPolicy(security_settings=settings)


def get_token_service(
    uow: Annotated[
        AbstractUnitOfWork,
        Depends(get_uow),
    ],
    jwt_manager: Annotated[
        AbstractJwtManager,
        Depends(get_jwt_manager),
    ],
    token_hasher: Annotated[
        AbstractTokenHasher,
        Depends(get_token_hasher),
    ],
    token_policy: Annotated[
        TokenPolicy,
        Depends(get_token_policy),
    ],
) -> AbstractTokenService:
    return TokenService(
        uow=uow,
        jwt_manager=jwt_manager,
        token_hasher=token_hasher,
        token_policy=token_policy,
    )


def get_session_service(
    uow: Annotated[
        AbstractUnitOfWork,
        Depends(get_uow),
    ],
    session_policy: Annotated[
        SessionPolicy,
        Depends(get_session_policy),
    ],
) -> AbstractSessionService:
    return SessionService(
        uow=uow,
        session_policy=session_policy,
    )


def get_auth_service(
    uow: Annotated[
        AbstractUnitOfWork,
        Depends(get_uow),
    ],
    password_manager: Annotated[
        PasswordManager,
        Depends(get_password_manager),
    ],
    token_service: Annotated[
        AbstractTokenService,
        Depends(get_token_service),
    ],
    session_service: Annotated[
        AbstractSessionService,
        Depends(get_session_service),
    ],
) -> AbstractAuthService:
    return AuthService(
        uow=uow,
        password_manager=password_manager,
        token_service=token_service,
        session_service=session_service,
    )


def get_cookie_policy() -> CookiePolicy:
    return CookiePolicy(cookie_settings=settings)


def get_cookie_service(
    cookie_policy: Annotated[
        CookiePolicy,
        Depends(get_cookie_policy),
    ],
) -> AbstractCookieService:
    return CookieService(
        cookie_policy=cookie_policy,
    )


async def get_current_user(
    request: Request,
    auth_service: Annotated[
        AbstractAuthService,
        Depends(get_auth_service),
    ],
    cookie_service: Annotated[
        AbstractCookieService,
        Depends(get_cookie_service),
    ],
) -> AuthContext:
    access_token = cookie_service.get_access_token(request)

    if access_token is None:
        raise InvalidAccessTokenError()

    return await auth_service.get_current_user(
        access_token=access_token,
    )


async def require_authenticated_user(
    auth_context: Annotated[
        AuthContext,
        Depends(get_current_user),
    ],
) -> AuthContext:
    return auth_context


async def require_admin(
    auth_context: Annotated[
        AuthContext,
        Depends(require_authenticated_user),
    ],
) -> AuthContext:
    if auth_context.user.role not in {
        UserRole.ADMIN,
        UserRole.SUPER_ADMIN,
    }:
        raise InsufficientPermissionsError()

    return auth_context


async def require_super_admin(
    auth_context: Annotated[
        AuthContext,
        Depends(require_authenticated_user),
    ],
) -> AuthContext:
    if auth_context.user.role != UserRole.SUPER_ADMIN:
        raise InsufficientPermissionsError()

    return auth_context


# User Profile Service
def get_user_profile_service(
    uow: Annotated[
        AbstractUnitOfWork,
        Depends(get_uow),
    ],
    media_service: Annotated[
        AbstractMediaUploadService,
        Depends(get_media_upload_service),
    ],
) -> AbstractUserProfileService:
    return UserProfileService(uow, media_service=media_service)


# User Service
def get_user_service(
    uow: Annotated[
        AbstractUnitOfWork,
        Depends(get_uow),
    ],
    password_manager: Annotated[
        PasswordManager,
        Depends(get_password_manager),
    ],
    session_service: Annotated[
        AbstractSessionService,
        Depends(get_session_service),
    ],
    user_profile_service: Annotated[
        AbstractUserProfileService,
        Depends(get_user_profile_service),
    ],
) -> AbstractUserService:
    return UserService(
        uow=uow,
        password_manager=password_manager,
        session_service=session_service,
        user_profile_service=user_profile_service,
    )
