from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserProfileAvatarResponse(BaseModel):
    id: UUID
    url: str
    mime_type: str
    width: int | None
    height: int | None


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    first_name: str | None
    last_name: str | None
    display_name: str | None
    phone: str | None
    job_title: str | None
    bio: str | None
    avatar_media_id: UUID | None
    avatar: UserProfileAvatarResponse | None


class UpdateUserProfileRequest(BaseModel):
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    display_name: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    job_title: str | None = Field(default=None, max_length=150)
    bio: str | None = None
    avatar_media_id: UUID | None = None
