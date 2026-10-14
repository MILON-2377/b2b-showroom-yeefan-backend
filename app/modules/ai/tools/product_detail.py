from typing import Any
from uuid import UUID

from app.core.contracts.services.product import AbstractProductService


class ProductDetailTool:
    name = "get_product"

    description = (
        "Get detailed information about a published bridal product "
        "using its product ID."
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
        product_id = UUID(arguments["product_id"])

        product = await self.product_service.get_by_id(product_id)

        return {
            "id": str(product.id),
            "brand_id": str(product.brand_id),
            "collection_id": str(product.collection_id),
            "category_id": str(product.category_id),
            "product_code": product.product_code,
            "name": product.name,
            "slug": product.slug,
            "description": product.description,
            "status": product.status.value,
            "details": product.details,
            "colors": product.colors,
            "sizes": product.sizes,
            "measurement_guide": product.measurement_guide,
            "customization": product.customization,
            "media": product.media,
        }
