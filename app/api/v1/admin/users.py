from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status

from app.core.contracts.services.user import AbstractUserService
from app.core.contracts.services.user_profile import AbstractUserProfileService
from app.core.security.dependencies import RequirePermission
from app.core.security.permissions import Permissions
from app.core.security.rate_limiter import limiter
from app.modules.auth.dependencies import (
    get_user_profile_service,
    get_user_service,
)
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.auth.models.user import User, UserRole
from app.modules.auth.schemas.user import (
    CreateAdminRequest,
    ResetPasswordRequest,
    UpdateUserRequest,
    UserListResponse,
    UserResponse,
)
from app.modules.auth.schemas.user_profile import (
    UpdateUserProfileRequest,
    UserProfileResponse,
)

router = APIRouter(prefix="/users", tags=["User"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
async def create_admin(
    request: Request,
    payload: CreateAdminRequest,
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.USER_CREATE)),
    ],
    user_service: Annotated[
        AbstractUserService,
        Depends(get_user_service),
    ],
) -> UserResponse:
    user = await user_service.create_admin(
        email=payload.email,
        password=payload.password,
    )

    return UserResponse.model_validate(user)


@router.get(
    "",
    response_model=UserListResponse,
)
@limiter.limit("60/minute")
async def list_users(
    request: Request,
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.USER_READ)),
    ],
    user_service: Annotated[
        AbstractUserService,
        Depends(get_user_service),
    ],
    role: UserRole | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> UserListResponse:
    users = await user_service.list_users(
        role=role,
        is_active=is_active,
        page=page,
        page_size=page_size,
    )

    return UserListResponse(
        items=[
            {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            for user in users.items
        ],
        page=users.page,
        page_size=users.page_size,
        total=users.total,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute")
async def get_user(
    request: Request,
    user_id: UUID,
    _: Annotated[AuthContext, Depends(RequirePermission(Permissions.USER_READ))],
    user_service: Annotated[AbstractUserService, Depends(get_user_service)],
) -> UserResponse:
    user = await user_service.get_user(
        user_id=user_id,
    )

    return UserResponse.model_validate(user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
async def update_user(
    request: Request,
    user_id: UUID,
    payload: UpdateUserRequest,
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.USER_UPDATE)),
    ],
    user_service: Annotated[
        AbstractUserService,
        Depends(get_user_service),
    ],
) -> UserResponse:
    user = await user_service.update_user(
        user_id=user_id,
        email=payload.email,
    )

    return UserResponse.model_validate(user)


@router.post(
    "/{user_id}/activate",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
async def activate_user(
    request: Request,
    user_id: UUID,
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.USER_ACTIVATE)),
    ],
    user_service: Annotated[
        AbstractUserService,
        Depends(get_user_service),
    ],
) -> UserResponse:
    user = await user_service.activate_user(
        user_id=user_id,
    )

    return UserResponse.model_validate(user)


@router.post(
    "/{user_id}/deactivate",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
async def deactivate_user(
    request: Request,
    user_id: UUID,
    authe_context: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.USER_DEACTIVATE)),
    ],
    user_service: Annotated[
        AbstractUserService,
        Depends(get_user_service),
    ],
) -> UserResponse:
    user = await user_service.deactivate_user(
        user_id=user_id, actor_user_id=authe_context.user.id
    )

    return UserResponse.model_validate(user)


@router.post(
    "/{user_id}/reset-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("5/minute")
async def reset_password(
    request: Request,
    user_id: UUID,
    payload: ResetPasswordRequest,
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.USER_RESET_PASSWORD)),
    ],
    user_service: Annotated[
        AbstractUserService,
        Depends(get_user_service),
    ],
) -> None:
    await user_service.reset_password(
        user_id=user_id,
        password=payload.password,
    )


@router.post(
    "/{user_id}/revoke-sessions",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("10/minute")
async def revoke_user_sessions(
    request: Request,
    user_id: UUID,
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.USER_REVOKE_SESSIONS)),
    ],
    user_service: Annotated[
        AbstractUserService,
        Depends(get_user_service),
    ],
) -> None:
    await user_service.revoke_user_sessions(
        user_id=user_id,
    )


@router.patch(
    "/{user_id}/profile",
    response_model=UserProfileResponse,
)
@limiter.limit("30/minute")
async def update_user_profile(
    request: Request,
    user_id: UUID,
    payload: UpdateUserProfileRequest,
    _: Annotated[
        AuthContext,
        Depends(RequirePermission(Permissions.USER_UPDATE)),
    ],
    profile_service: Annotated[
        AbstractUserProfileService,
        Depends(get_user_profile_service),
    ],
) -> UserProfileResponse:
    profile = await profile_service.update_profile(
        user_id=user_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        display_name=payload.display_name,
        phone=payload.phone,
        job_title=payload.job_title,
        bio=payload.bio,
        avatar_media_id=payload.avatar_media_id,
    )

    return UserProfileResponse(**profile.__dict__)
