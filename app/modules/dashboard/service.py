from app.core.contracts.services.dashboard import (
    AbstractDashboardService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.dashboard.dtos import (
    DashboardDTO,
    DashboardInquiryDTO,
    DashboardProductDTO,
    DashboardReviewDTO,
    DashboardStatsDTO,
)


class DashboardService(AbstractDashboardService):

    def __init__(
        self,
        uow: AbstractUnitOfWork,
    ) -> None:
        self.uow = uow

    async def get_dashboard(self) -> DashboardDTO:
        stats = await self.uow.dashboard.get_stats()

        inquiries = await self.uow.dashboard.list_recent_inquiries(
            limit=5,
        )

        products = await self.uow.dashboard.list_recent_products(
            limit=5,
        )

        reviews = await self.uow.dashboard.list_pending_reviews(
            limit=5,
        )

        return DashboardDTO(
            stats=DashboardStatsDTO(**stats),
            recent_inquiries=tuple(
                DashboardInquiryDTO(
                    id=item.id,
                    name=item.name,
                    company_name=item.company_name,
                    status=self._status_value(item.status),
                    created_at=item.created_at,
                )
                for item in inquiries
            ),
            recent_products=tuple(
                DashboardProductDTO(
                    id=item.id,
                    name=item.name,
                    product_code=item.product_code,
                    status=self._status_value(item.status),
                    created_at=item.created_at,
                )
                for item in products
            ),
            pending_reviews=tuple(
                DashboardReviewDTO(
                    id=item.id,
                    name=item.name,
                    company_name=item.company_name,
                    rating=item.rating,
                    status=self._status_value(item.status),
                    created_at=item.created_at,
                )
                for item in reviews
            ),
        )

    @staticmethod
    def _status_value(status: object) -> str:
        value = getattr(status, "value", status)
        return str(value)