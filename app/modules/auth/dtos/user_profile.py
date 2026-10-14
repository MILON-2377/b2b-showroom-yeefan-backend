from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class UserProfileAvatarDTO:
    id: UUID
    url: str
    mime_type: str
    width: int | None
    height: int | None


@dataclass(frozen=True)
class UserProfileDTO:
    id: UUID
    user_id: UUID
    first_name: str | None
    last_name: str | None
    display_name: str | None
    phone: str | None
    job_title: str | None
    bio: str | None
    avatar_media_id: UUID | None
    avatar: UserProfileAvatarDTO | None
    created_at: datetime
    updated_at: datetime
