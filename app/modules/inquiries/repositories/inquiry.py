from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.inquiry import AbstractInquiryRepository
from app.core.models import RecordStatus
from app.modules.inquiries.models.inquiry import Inquiry, InquiryStatus


class InquiryRepository(
    AbstractInquiryRepository,
):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_status(self, inquiry: Inquiry) -> Inquiry:

        self.session.add(inquiry)
        await self.session.flush()
        return inquiry

    async def create(self, inquiry: Inquiry) -> Inquiry:
        self.session.add(inquiry)

        await self.session.flush()

        return inquiry

    async def get_by_id(
        self,
        inquiry_id: UUID,
    ) -> Inquiry | None:
        result = await self.session.execute(
            select(Inquiry).where(Inquiry.id == inquiry_id)
        )

        return result.scalar_one_or_none()

    async def list_admin(
        self,
        *,
        offset: int,
        limit: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> list[Inquiry]:
        filters = []

        if search:
            pattern = f"%{search.strip()}%"

            filters.append(
                or_(
                    Inquiry.name.ilike(pattern),
                    Inquiry.email.ilike(pattern),
                    Inquiry.company_name.ilike(pattern),
                )
            )

        if status is not None:
            filters.append(Inquiry.status == status)

        result = await self.session.execute(
            select(Inquiry)
            .where(*filters)
            .order_by(
                Inquiry.created_at.desc(),
                Inquiry.id.asc(),
            )
            .offset(offset)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def count_admin(
        self,
        *,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> int:
        filters = []

        if search:
            pattern = f"%{search.strip()}%"

            filters.append(
                or_(
                    Inquiry.name.ilike(pattern),
                    Inquiry.email.ilike(pattern),
                    Inquiry.company_name.ilike(pattern),
                )
            )

        if status is not None:
            filters.append(Inquiry.status == status)

        result = await self.session.execute(
            select(func.count(Inquiry.id)).where(*filters)
        )

        return result.scalar_one()
