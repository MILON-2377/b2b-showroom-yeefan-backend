from typing import Any

from app.core.contracts.services.product import AbstractProductService
from app.modules.products.dtos import PublicProductQueryDTO


class ProductSearchTool:
    name = "search_products"

    description = (
        "Search published bridal products by keyword, category, collection, "
        "brand, or product code."
    )

    def __init__(
        self,
        product_service: AbstractProductService,
    ) -> None:
        self.product_service = product_service

    async def execute(
        self,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        query = PublicProductQueryDTO(
            search=arguments.get("search"),
            page_size=arguments.get("page_size", 3),
            brand_id=arguments.get("brand_id"),
            collection_id=arguments.get("collection_id"),
            category_id=arguments.get("category_id"),
        )

        result = await self.product_service.list_public(
            query=query,
        )

        return {
            "items": [
                {
                    "id": str(product.id),
                    "product_code": product.product_code,
                    "name": product.name,
                    "slug": product.slug,
                    "description": product.description,
                }
                for product in result.items
            ],
            "next_cursor": result.next_cursor,
            "has_more": result.has_more,
        }
