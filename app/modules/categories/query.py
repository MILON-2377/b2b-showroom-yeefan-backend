from dataclasses import dataclass

from app.core.models import RecordStatus
from app.modules.categories.dtos import CategoryListItem


@dataclass(frozen=True)
class CategoryListQuery:
    search: str | None = None
    status: RecordStatus | None = None
    page: int = 1
    page_size: int = 20


@dataclass(frozen=True)
class CategoryListResult:
    items: list[CategoryListItem]
    total: int
