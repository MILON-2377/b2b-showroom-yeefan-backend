from uuid import uuid4

from app.core.models import RecordStatus
from app.modules.products.query import (
    ProductListQuery,
    ProductSortField,
    SortOrder,
)


def test_product_list_query_defaults():
    query = ProductListQuery()

    assert query.page == 1
    assert query.page_size == 24
    assert query.brand_id is None
    assert query.collection_id is None
    assert query.category_id is None
    assert query.search is None
    assert query.status is None
    assert query.sort_by == ProductSortField.CREATED_AT
    assert query.sort_order == SortOrder.DESC


def test_product_list_query_accepts_filters():
    brand_id = uuid4()
    collection_id = uuid4()
    category_id = uuid4()

    query = ProductListQuery(
        page=2,
        page_size=48,
        brand_id=brand_id,
        collection_id=collection_id,
        category_id=category_id,
        search="mermaid",
        status=RecordStatus.PUBLISHED,
        sort_by=ProductSortField.NAME,
        sort_order=SortOrder.ASC,
    )

    assert query.page == 2
    assert query.page_size == 48
    assert query.brand_id == brand_id
    assert query.collection_id == collection_id
    assert query.category_id == category_id
    assert query.search == "mermaid"
    assert query.status == RecordStatus.PUBLISHED
    assert query.sort_by == ProductSortField.NAME
    assert query.sort_order == SortOrder.ASC
