from dataclasses import dataclass
from uuid import UUID

from app.core.database.models import Collection
from app.core.models import RecordStatus


@dataclass(frozen=True)
class CollectionListQuery:
    page: int = 1
    page_size: int = 20
    brand_id: UUID | None = None
    search: str | None = None
    status: RecordStatus | None = None


@dataclass(frozen=True)
class CollectionListResult:
    items: list[Collection]
    total: int
