from typing import Any
from uuid import UUID, uuid4

from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.services.user_profile import (
    AbstractUserProfileService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.auth.dtos.user_profile import UserProfileAvatarDTO, UserProfileDTO
from app.modules.auth.exceptions import UserProfileNotFoundError
from app.modules.auth.models.user_profile import UserProfile
from app.modules.media.exceptions import (
    MediaAssetNotFoundError,
    MediaAssetNotReadyError,
)
from app.modules.media.model import MediaAssetStatus


class UserProfileService(AbstractUserProfileService):
    def __init__(
        self, uow: AbstractUnitOfWork, media_service: AbstractMediaUploadService
    ) -> None:
        self.uow = uow
        self.media_service = media_service

    async def create_profile(
        self,
        *,
        user_id: UUID,
        first_name: str | None = None,
        last_name: str | None = None,
        display_name: str | None = None,
        phone: str | None = None,
        job_title: str | None = None,
        bio: str | None = None,
        avatar_media_id: UUID | None = None,
    ) -> UserProfileDTO:

        existing = await self.uow.user_profiles.get_by_user_id(user_id)

        if existing is not None:
            return self._to_dto(existing)

        profile = UserProfile(
            id=uuid4(),
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
            phone=phone,
            job_title=job_title,
            bio=bio,
            avatar_media_id=avatar_media_id,
        )

        profile = await self.uow.user_profiles.create(profile)

        await self.uow.commit()

        return self._to_dto(profile)

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> UserProfileDTO:

        profile = await self.uow.user_profiles.get_by_user_id(user_id)

        if profile is None:
            raise UserProfileNotFoundError(user_id)

        return self._to_dto(profile)

    async def update_profile(
        self,
        *,
        user_id: UUID,
        updates: dict[str, Any],
    ) -> UserProfileDTO:

        profile = await self.uow.user_profiles.get_by_user_id(user_id)

        if profile is None:
            raise UserProfileNotFoundError(user_id)

        if "avatar_media_id" in updates:
            avatar_media_id = updates["avatar_media_id"]

            if avatar_media_id is not None:
                media_asset = await self.uow.media_assets.get_by_id(avatar_media_id)

                if media_asset is None:
                    raise MediaAssetNotFoundError(avatar_media_id)

                if media_asset.status != MediaAssetStatus.READY:
                    raise MediaAssetNotReadyError(avatar_media_id)

        for field, value in updates.items():
            setattr(profile, field, value)

        profile = await self.uow.user_profiles.update(profile)

        await self.uow.commit()

        return self._to_dto(profile)

    def _to_dto(
        self,
        profile: UserProfile,
    ) -> UserProfileDTO:

        avatar = None

        if profile.avatar_media is not None:
            url = self.media_service.get_asset_url(
                media_asset=profile.avatar_media,
            )

            avatar = UserProfileAvatarDTO(
                id=profile.avatar_media.id,
                url=url,
                mime_type=profile.avatar_media.mime_type,
                width=profile.avatar_media.width,
                height=profile.avatar_media.height,
            )

        return UserProfileDTO(
            id=profile.id,
            user_id=profile.user_id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            display_name=profile.display_name,
            phone=profile.phone,
            job_title=profile.job_title,
            bio=profile.bio,
            avatar_media_id=profile.avatar_media_id,
            avatar=avatar,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )
