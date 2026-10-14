from __future__ import annotations

from uuid import UUID

from app.core.contracts.services.inquiry import (
    AbstractInquiryService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.models import RecordStatus
from app.modules.inquiries.dtos.inquiry import (
    CreateInquiryDTO,
    InquiryDTO,
    InquiryProductDTO,
    UpdateInquiryStatusDTO,
)
from app.modules.inquiries.dtos.inquiry_product import CreateInquiryProductDTO
from app.modules.inquiries.exceptions import InquiryNotFoundError
from app.modules.inquiries.models.inquiry import Inquiry
from app.modules.inquiries.models.inquiry_product import InquiryProduct
from app.modules.inquiries.schemas import CreateInquiryRequest


class InquiryService(AbstractInquiryService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
    ) -> None:
        self.uow = uow

    async def update_status(
        self,
        inquiry_id: UUID,
        data: UpdateInquiryStatusDTO,
    ) -> InquiryDTO:
        inquiry = await self.uow.inquiries.get_by_id(inquiry_id=inquiry_id)

        if inquiry is None:
            raise InquiryNotFoundError(inquiry_id)

        if data.status is not None:
            inquiry.status = data.status

        if data.internal_notes is not None:
            inquiry.internal_notes = data.internal_notes

        await self.uow.inquiries.update_status(inquiry=inquiry)
        await self.uow.commit()

        products = await self.uow.inquiry_products.get_by_inquiry_id(
            inquiry_id,
        )

        return self._to_dto(
            inquiry=inquiry,
            products=products,
        )

    async def create(
        self,
        *,
        payload: CreateInquiryDTO,
    ) -> InquiryDTO:
        inquiry = Inquiry(
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            country=payload.country,
            company_name=payload.company_name,
            job_title=payload.job_title,
            inquiry_type=payload.inquiry_type,
            quantity_range=payload.quantity_range,
            message=payload.message,
            source_page=payload.source_page,
        )

        await self.uow.inquiries.create(inquiry)

        inquiry_products = [
            InquiryProduct(
                inquiry_id=inquiry.id,
                product_id=item.product_id,
                quantity_requested=item.quantity_requested,
                notes=item.notes,
            )
            for item in payload.products
        ]

        if inquiry_products:
            await self.uow.inquiry_products.create_many(
                inquiry_products,
            )

        await self.uow.commit()

        return InquiryDTO(
            id=inquiry.id,
            name=inquiry.name,
            email=inquiry.email,
            phone=inquiry.phone,
            country=inquiry.country,
            company_name=inquiry.company_name,
            job_title=inquiry.job_title,
            inquiry_type=inquiry.inquiry_type,
            quantity_range=inquiry.quantity_range,
            message=inquiry.message,
            source_page=inquiry.source_page,
            status=inquiry.status,
            internal_notes=inquiry.internal_notes,
            created_at=inquiry.created_at,
            updated_at=inquiry.updated_at,
            products=tuple(self._product_to_dto(item) for item in inquiry_products),
        )

    async def get_by_id(
        self,
        inquiry_id: UUID,
    ) -> InquiryDTO:
        inquiry = await self.uow.inquiries.get_by_id(inquiry_id)

        if inquiry is None:
            raise InquiryNotFoundError(inquiry_id)

        products = await self.uow.inquiry_products.get_by_inquiry_id(
            inquiry_id,
        )

        return self._to_dto(
            inquiry=inquiry,
            products=products,
        )

    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> tuple[list[InquiryDTO], int]:
        offset = (page - 1) * page_size

        inquiries = await self.uow.inquiries.list_admin(
            offset=offset,
            limit=page_size,
            search=search,
            status=status,
        )

        total = await self.uow.inquiries.count_admin(
            search=search,
            status=status,
        )

        return [
            InquiryDTO(
                id=inquiry.id,
                name=inquiry.name,
                email=inquiry.email,
                phone=inquiry.phone,
                country=inquiry.country,
                company_name=inquiry.company_name,
                job_title=inquiry.job_title,
                inquiry_type=inquiry.inquiry_type,
                quantity_range=inquiry.quantity_range,
                message=inquiry.message,
                source_page=inquiry.source_page,
                status=inquiry.status,
                internal_notes=inquiry.internal_notes,
                created_at=inquiry.created_at,
                updated_at=inquiry.updated_at,
                products=(),
            )
            for inquiry in inquiries
        ], total

    async def list(
        self,
        *,
        page: int,
        page_size: int,
    ) -> tuple[list[InquiryDTO], int]:
        offset = (page - 1) * page_size

        inquiries = await self.uow.inquiries.list(
            offset=offset,
            limit=page_size,
        )

        total = await self.uow.inquiries.count()

        dtos: list[InquiryDTO] = []

        for inquiry in inquiries:
            products = await self.uow.inquiry_products.get_by_inquiry_id(
                inquiry.id,
            )

            dtos.append(
                self._to_dto(
                    inquiry=inquiry,
                    products=products,
                )
            )

        return dtos, total

    @staticmethod
    def _product_to_dto(
        product: InquiryProduct,
    ) -> InquiryProductDTO:
        return InquiryProductDTO(
            id=product.id,
            inquiry_id=product.inquiry_id,
            product_id=product.product_id,
            quantity_requested=product.quantity_requested,
            notes=product.notes,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

    def _to_dto(
        self,
        *,
        inquiry: Inquiry,
        products: list[InquiryProduct],
    ) -> InquiryDTO:
        return InquiryDTO(
            id=inquiry.id,
            name=inquiry.name,
            email=inquiry.email,
            phone=inquiry.phone,
            country=inquiry.country,
            company_name=inquiry.company_name,
            job_title=inquiry.job_title,
            inquiry_type=inquiry.inquiry_type,
            quantity_range=inquiry.quantity_range,
            message=inquiry.message,
            source_page=inquiry.source_page,
            status=inquiry.status,
            internal_notes=inquiry.internal_notes,
            created_at=inquiry.created_at,
            updated_at=inquiry.updated_at,
            products=tuple(self._product_to_dto(product) for product in products),
        )

    @staticmethod
    def _to_create_dto(
        payload: CreateInquiryRequest,
    ) -> CreateInquiryDTO:
        return CreateInquiryDTO(
            name=payload.name,
            email=str(payload.email),
            phone=payload.phone,
            country=payload.country,
            company_name=payload.company_name,
            job_title=payload.job_title,
            inquiry_type=payload.inquiry_type,
            quantity_range=payload.quantity_range,
            message=payload.message,
            source_page=payload.source_page,
            products=tuple(
                CreateInquiryProductDTO(
                    product_id=item.product_id,
                    quantity_requested=item.quantity_requested,
                    notes=item.notes,
                )
                for item in payload.products
            ),
        )
