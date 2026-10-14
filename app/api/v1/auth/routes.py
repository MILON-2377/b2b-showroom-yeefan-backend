from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status

from app.api.v1.auth.helpers import (
    to_profile_response,
    to_session_response,
)
from app.core.contracts.services.auth import AbstractAuthService
from app.core.contracts.services.auth_session import AbstractSessionService
from app.core.contracts.services.cookie import AbstractCookieService
from app.core.contracts.services.user import AbstractUserService
from app.core.contracts.services.user_profile import AbstractUserProfileService
from app.core.security.dependencies import RequirePermission
from app.core.security.permissions import Permissions
from app.core.security.rate_limiter import limiter
from app.modules.auth.dependencies import (
    get_auth_service,
    get_cookie_service,
    get_session_service,
    get_user_profile_service,
    get_user_service,
)
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.auth.exceptions import InvalidRefreshTokenError
from app.modules.auth.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    UserResponse,
)
from app.modules.auth.schemas.session import SessionResponse
from app.modules.auth.schemas.user_profile import (
    UpdateUserProfileRequest,
    UserProfileResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("5/minute")
async def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    auth_service: Annotated[
        AbstractAuthService,
        Depends(get_auth_service),
    ],
    cookie_service: Annotated[
        AbstractCookieService,
        Depends(get_cookie_service),
    ],
) -> None:
    tokens = await auth_service.login(
        email=payload.email,
        password=payload.password,
        device_name=payload.device_name,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )

    cookie_service.set_auth_cookies(
        response,
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        access_token_expires_at=tokens.expires_at,
    )


@router.post(
    "/refresh",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("20/minute")
async def refresh(
    request: Request,
    response: Response,
    auth_service: Annotated[
        AbstractAuthService,
        Depends(get_auth_service),
    ],
    cookie_service: Annotated[
        AbstractCookieService,
        Depends(get_cookie_service),
    ],
) -> None:

    refresh_token = cookie_service.get_refresh_token(request)

    if refresh_token is None:
        raise InvalidRefreshTokenError()

    tokens = await auth_service.refresh(
        refresh_token=refresh_token,
    )

    cookie_service.set_auth_cookies(
        response,
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        access_token_expires_at=tokens.expires_at,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("20/minute")
async def logout(
    request: Request,
    response: Response,
    payload: RefreshTokenRequest,
    auth_service: Annotated[
        AbstractAuthService,
        Depends(get_auth_service),
    ],
    cookie_service: Annotated[
        AbstractCookieService,
        Depends(get_cookie_service),
    ],
) -> None:
    await auth_service.logout(
        refresh_token=payload.refresh_token,
    )

    cookie_service.clear_auth_cookies(response)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("120/minute")
async def get_current_user(
    request: Request,
    auth_context: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.ACCOUNT_READ_SELF)),
    ],
) -> UserResponse:
    return UserResponse.model_validate(auth_context.user)


@router.post("/me/password", status_code=204)
@limiter.limit("5/minute")
async def change_my_password(
    request: Request,
    payload: ChangePasswordRequest,
    auth_context: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.ACCOUNT_CHANGE_PASSWORD)),
    ],
    user_service: Annotated[
        AbstractUserService,
        Depends(get_user_service),
    ],
) -> None:
    await user_service.change_password(
        user_id=auth_context.user.id,
        current_password=payload.current_password,
        new_password=payload.new_password,
    )


@router.get(
    "/sessions",
    response_model=list[SessionResponse],
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute")
async def get_my_sessions(
    request: Request,
    auth_context: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.SESSION_READ_SELF)),
    ],
    session_service: Annotated[
        AbstractSessionService,
        Depends(get_session_service),
    ],
) -> list[SessionResponse]:
    sessions = await session_service.get_user_sessions(
        user_id=auth_context.user.id,
    )

    return [to_session_response(session=session) for session in sessions]


@router.delete(
    "/sessions/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("10/minute")
async def revoke_my_session(
    request: Request,
    session_id: UUID,
    auth_context: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.SESSION_REVOKE_SELF)),
    ],
    session_service: Annotated[
        AbstractSessionService,
        Depends(get_session_service),
    ],
) -> None:
    session = await session_service.revoke_session(
        session_id=session_id,
        user_id=auth_context.user.id,
    )

    return to_session_response(session)


@router.post("/sessions/revoke-others", status_code=204)
@limiter.limit("60/minute")
async def revoke_other_sessions(
    request: Request,
    auth_context: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.SESSION_REVOKE_OTHERS)),
    ],
    session_service: Annotated[
        AbstractSessionService,
        Depends(get_session_service),
    ],
) -> None:
    await session_service.revoke_other_sessions(
        user_id=auth_context.user.id,
        current_session_id=auth_context.session_id,
    )


@router.get(
    "/sessions/{session_id}",
    response_model=SessionResponse,
)
@limiter.limit("60/minute")
async def get_my_session(
    request: Request,
    session_id: UUID,
    auth_context: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.SESSION_READ_SELF)),
    ],
    session_service: Annotated[
        AbstractSessionService,
        Depends(get_session_service),
    ],
) -> SessionResponse:
    session = await session_service.get_session(
        session_id=session_id,
        user_id=auth_context.user.id,
    )

    return to_session_response(session)


# User Profile
@router.get(
    "/me/profile",
    response_model=UserProfileResponse,
)
@limiter.limit("120/minute")
async def get_my_profile(
    request: Request,
    auth_context: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.ACCOUNT_READ_SELF)),
    ],
    profile_service: Annotated[
        AbstractUserProfileService,
        Depends(get_user_profile_service),
    ],
) -> UserProfileResponse:
    profile = await profile_service.get_by_user_id(auth_context.user.id)

    return to_profile_response(profile)


@router.patch(
    "/me/profile",
    response_model=UserProfileResponse,
)
@limiter.limit("30/minute")
async def update_my_profile(
    request: Request,
    payload: UpdateUserProfileRequest,
    auth_context: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.ACCOUNT_UPDATE_SELF)),
    ],
    profile_service: Annotated[
        AbstractUserProfileService,
        Depends(get_user_profile_service),
    ],
) -> UserProfileResponse:

    updates = payload.model_dump(
        exclude_unset=True,
    )

    profile = await profile_service.update_profile(
        user_id=auth_context.user.id,
        updates=updates,
    )

    return to_profile_response(profile)
