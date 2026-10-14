from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from app.core.models import RecordStatus

if TYPE_CHECKING:
    from app.core.database.models import Product


class ProductSortField(str, Enum):
    CREATED_AT = "created_at"
    PUBLISHED_AT = "published_at"
    NAME = "name"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True)
class ProductListQuery:
    page: int = 1
    page_size: int = 24
    brand_id: UUID | None = None
    collection_id: UUID | None = None
    category_id: UUID | None = None
    search: str | None = None
    status: RecordStatus | None = None
    sort_by: ProductSortField = ProductSortField.CREATED_AT
    sort_order: SortOrder = SortOrder.DESC


@dataclass(frozen=True)
class ProductListResult:
    items: list["Product"]
    total: int



