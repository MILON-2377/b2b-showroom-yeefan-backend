from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.contracts.repositories.about_video import (
    AbstractAboutVideoRepository,
)
from app.core.models import RecordStatus
from app.modules.about_videos.model import AboutVideo


class AboutVideoRepository(AbstractAboutVideoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        video: AboutVideo,
    ) -> AboutVideo:
        self.session.add(video)
        await self.session.flush()

        return video

    async def get_by_id(
        self,
        video_id: UUID,
    ) -> AboutVideo | None:
        result = await self.session.execute(
            select(AboutVideo)
            .options(selectinload(AboutVideo.media_asset))
            .where(AboutVideo.id == video_id)
        )
        return result.scalar_one_or_none()

    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> tuple[list[AboutVideo], int]:
        filters = []

        if search:
            term = f"%{search.strip()}%"
            filters.append(
                or_(
                    AboutVideo.title.ilike(term),
                    AboutVideo.description.ilike(term),
                )
            )

        if status is not None:
            filters.append(AboutVideo.status == status)

        count_result = await self.session.execute(
            select(func.count(AboutVideo.id)).where(*filters)
        )
        total = count_result.scalar_one()

        result = await self.session.execute(
            select(AboutVideo)
            .options(selectinload(AboutVideo.media_asset))
            .where(*filters)
            .order_by(
                AboutVideo.sort_order.asc(),
                AboutVideo.created_at.desc(),
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        return list(result.scalars().all()), total

    async def list_published(self) -> list[AboutVideo]:
        stmt = (
            select(AboutVideo)
            .options(
                selectinload(AboutVideo.media_asset),
            )
            .where(
                AboutVideo.status == RecordStatus.PUBLISHED,
            )
            .order_by(
                AboutVideo.sort_order.asc(),
                AboutVideo.created_at.desc(),
            )
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def update(self, video: AboutVideo) -> AboutVideo:
        self.session.add(video)
        await self.session.flush()
        await self.session.refresh(video)

        return video

    async def delete(
        self,
        video: AboutVideo,
    ) -> None:
        await self.session.delete(video)
        await self.session.flush()
