from dataclasses import dataclass

from app.core.models import RecordStatus

from .model import Brand


@dataclass(frozen=True)
class BrandListQuery:
    page: int = 1
    page_size: int = 20
    search: str | None = None
    status: RecordStatus | None = None


@dataclass(frozen=True)
class BrandListResult:
    items: list[Brand]
    total: int
