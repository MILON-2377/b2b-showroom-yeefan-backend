from uuid import UUID

from app.core.contracts.services.product_detail import (
    AbstractProductDetailService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.product_details.dtos import (
    CreateProductDetailDTO,
    ProductDetailDTO,
    UpdateProductDetailDTO,
)
from app.modules.product_details.exceptions import ProductDetailNotFoundError
from app.modules.product_details.model import ProductDetail


class ProductDetailService(AbstractProductDetailService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
    ) -> None:
        self.uow = uow

    async def create(
        self,
        *,
        product_id: UUID,
        payload: CreateProductDetailDTO,
    ) -> ProductDetailDTO:

        detail = ProductDetail(
            product_id=product_id,
            garment_type=payload.garment_type,
            silhouette=payload.silhouette,
            length=payload.length,
            fabric=payload.fabric,
            secondary_fabric=payload.secondary_fabric,
            lining=payload.lining,
            neckline=payload.neckline,
            back_style=payload.back_style,
            waistline=payload.waistline,
            sleeve_type=payload.sleeve_type,
            sleeve_length=payload.sleeve_length,
            train=payload.train,
            embellishment=payload.embellishment,
            closure=payload.closure,
            internal_support=payload.internal_support,
        )

        detail = await self.uow.product_details.create(detail)

        return self._to_dto(detail)

    async def get_by_product_id(
        self,
        *,
        product_id: UUID,
    ) -> ProductDetailDTO:

        detail = await self.uow.product_details.get_by_product_id(product_id)

        if detail is None:
            raise ProductDetailNotFoundError(product_id)

        return self._to_dto(detail)

    async def update(
        self,
        *,
        product_id: UUID,
        payload: UpdateProductDetailDTO,
    ) -> ProductDetailDTO:
        detail = await self.uow.product_details.get_by_product_id(
            product_id=product_id,
        )

        if detail is None:
            detail = ProductDetail(
                product_id=product_id,
                garment_type=payload.garment_type,
                silhouette=payload.silhouette,
                length=payload.length,
                fabric=payload.fabric,
                secondary_fabric=payload.secondary_fabric,
                lining=payload.lining,
                neckline=payload.neckline,
                back_style=payload.back_style,
                waistline=payload.waistline,
                sleeve_type=payload.sleeve_type,
                sleeve_length=payload.sleeve_length,
                train=payload.train,
                embellishment=payload.embellishment,
                closure=payload.closure,
                internal_support=payload.internal_support,
            )

            await self.uow.product_details.create(detail)

            return self._to_dto(detail)

        detail.garment_type = payload.garment_type
        detail.silhouette = payload.silhouette
        detail.length = payload.length
        detail.fabric = payload.fabric
        detail.secondary_fabric = payload.secondary_fabric
        detail.lining = payload.lining
        detail.neckline = payload.neckline
        detail.back_style = payload.back_style
        detail.waistline = payload.waistline
        detail.sleeve_type = payload.sleeve_type
        detail.sleeve_length = payload.sleeve_length
        detail.train = payload.train
        detail.embellishment = payload.embellishment
        detail.closure = payload.closure
        detail.internal_support = payload.internal_support

        await self.uow.product_details.update(detail)

        return self._to_dto(detail)

    async def delete(
        self,
        *,
        product_id: UUID,
    ) -> None:

        detail = await self.uow.product_details.get_by_product_id(product_id)

        if detail is None:
            return

        await self.uow.product_details.delete(detail)

    @staticmethod
    def _to_dto(
        detail: ProductDetail,
    ) -> ProductDetailDTO:
        return ProductDetailDTO(
            id=detail.id,
            product_id=detail.product_id,
            garment_type=detail.garment_type,
            silhouette=detail.silhouette,
            length=detail.length,
            fabric=detail.fabric,
            secondary_fabric=detail.secondary_fabric,
            lining=detail.lining,
            neckline=detail.neckline,
            back_style=detail.back_style,
            waistline=detail.waistline,
            sleeve_type=detail.sleeve_type,
            sleeve_length=detail.sleeve_length,
            train=detail.train,
            embellishment=detail.embellishment,
            closure=detail.closure,
            internal_support=detail.internal_support,
            created_at=detail.created_at,
            updated_at=detail.updated_at,
        )
