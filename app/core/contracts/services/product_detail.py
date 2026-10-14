from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product_details.dtos import ProductDetailDTO, UpdateProductDetailDTO


class AbstractProductDetailService(ABC):
    @abstractmethod
    async def create(
        self,
        *,
        product_id: UUID,
        garment_type: str | None = None,
        silhouette: str | None = None,
        length: str | None = None,
        fabric: str | None = None,
        secondary_fabric: str | None = None,
        lining: str | None = None,
        neckline: str | None = None,
        back_style: str | None = None,
        waistline: str | None = None,
        sleeve_type: str | None = None,
        sleeve_length: str | None = None,
        train: str | None = None,
        embellishment: str | None = None,
        closure: str | None = None,
        internal_support: str | None = None,
    ) -> ProductDetailDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_product_id(
        self,
        *,
        product_id: UUID,
    ) -> ProductDetailDTO:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, product_id: UUID, payload: UpdateProductDetailDTO
    ) -> ProductDetailDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        *,
        product_id: UUID,
    ) -> None:
        raise NotImplementedError
