from typing import Any

from app.core.contracts.services.collection import AbstractCollectionService
from app.modules.collections.dtos import PublicCollectionQueryDTO


class CollectionTool:
    name = "search_collections"

    description = "Search published bridal collections by keyword."

    def __init__(
        self,
        collection_service: AbstractCollectionService,
    ) -> None:
        self.collection_service = collection_service

    async def execute(
        self,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        query = PublicCollectionQueryDTO(
            search=arguments.get("search"),
            page=arguments.get("page", 1),
            page_size=arguments.get("page_size", 10),
        )

        result = await self.collection_service.list_public(query)

        return {
            "items": [
                {
                    "id": str(collection.id),
                    "brand_id": str(collection.brand_id),
                    "name": collection.name,
                    "slug": collection.slug,
                    "description": collection.description,
                }
                for collection in result.items
            ],
            "total": result.total,
            "page": result.page,
            "page_size": result.page_size,
            "total_pages": result.total_pages,
        }
