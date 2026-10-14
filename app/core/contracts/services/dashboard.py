from abc import ABC, abstractmethod

from app.modules.dashboard.dtos import DashboardDTO


class AbstractDashboardService(ABC):

    @abstractmethod
    async def get_dashboard(self) -> DashboardDTO:
        raise NotImplementedError