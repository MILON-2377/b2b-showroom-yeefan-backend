from typing import Annotated

from fastapi import Depends

from app.core.contracts.services.dashboard import (
    AbstractDashboardService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.dashboard.service import DashboardService
from app.shared.dependencies import get_uow


def get_dashboard_service(
    uow: Annotated[
        AbstractUnitOfWork,
        Depends(get_uow),
    ],
) -> AbstractDashboardService:
    return DashboardService(uow)
