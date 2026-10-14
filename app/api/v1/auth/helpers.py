from app.modules.auth.dtos.session import SessionDTO
from app.modules.auth.dtos.user_profile import UserProfileDTO
from app.modules.auth.schemas.session import SessionResponse
from app.modules.auth.schemas.user_profile import (
    UserProfileAvatarResponse,
    UserProfileResponse,
)


def to_session_response(session: SessionDTO) -> SessionResponse:
    return SessionResponse(
        id=session.id,
        device_name=session.device_name,
        user_agent=session.user_agent,
        ip_address=session.ip_address,
        created_at=session.created_at,
        last_active_at=session.last_active_at,
        expires_at=session.expires_at,
        revoked_at=session.revoked_at,
    )


def to_profile_response(
    profile: UserProfileDTO,
) -> UserProfileResponse:
    return UserProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        display_name=profile.display_name,
        phone=profile.phone,
        job_title=profile.job_title,
        bio=profile.bio,
        avatar_media_id=profile.avatar_media_id,
        avatar=(
            UserProfileAvatarResponse(
                id=profile.avatar.id,
                url=profile.avatar.url,
                mime_type=profile.avatar.mime_type,
                width=profile.avatar.width,
                height=profile.avatar.height,
            )
            if profile.avatar is not None
            else None
        ),
    )
