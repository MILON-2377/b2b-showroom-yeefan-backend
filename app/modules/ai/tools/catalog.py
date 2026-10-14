from typing import Any

from app.core.contracts.services.catalog import AbstractCatalogService
from app.modules.catalogs.dtos import PublicCatalogQueryDTO


class CatalogTool:
    name = "search_catalogs"

    description = (
        "Search published bridal catalogs. "
        "Catalogs are PDF files and the result includes the public PDF URL."
    )

    def __init__(
        self,
        catalog_service: AbstractCatalogService,
    ) -> None:
        self.catalog_service = catalog_service

    async def execute(
        self,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        query = PublicCatalogQueryDTO(
            page=arguments.get("page", 1),
            page_size=arguments.get("page_size", 10),
            search=arguments.get("search"),
        )

        result = await self.catalog_service.list_public(query)

        return {
            "items": [
                {
                    "id": str(catalog.id),
                    "collection_id": str(catalog.collection_id),
                    "title": catalog.title,
                    "description": catalog.description,
                    "catalog_url": catalog.catalog_url,
                    "cover_image_url": catalog.cover_image_url,
                }
                for catalog in result.items
            ],
            "total": result.total,
            "page": result.page,
            "page_size": result.page_size,
            "total_pages": result.total_pages,
        }