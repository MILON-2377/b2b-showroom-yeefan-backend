from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import TimestampMixin

if TYPE_CHECKING:
    from app.modules.products.model import Product


class InquiryStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    RESPONDED = "RESPONDED"
    CLOSED = "CLOSED"


class InquiryType(str, Enum):
    GENERAL = "GENERAL"
    PRODUCT = "PRODUCT"
    CUSTOMIZATION = "CUSTOMIZATION"
    OEM = "OEM"
    ODM = "ODM"
    PRIVATE_LABEL = "PRIVATE_LABEL"
    WHOLESALE = "WHOLESALE"


class QuantityRange(str, Enum):
    SAMPLE = "SAMPLE"
    SMALL_BATCH = "SMALL_BATCH"
    WHOLESALE = "WHOLESALE"
    LARGE_VOLUME = "LARGE_VOLUME"
    NOT_SURE = "NOT_SURE"


class Inquiry(Base, TimestampMixin):
    __tablename__ = "inquiries"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    # Contact
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Company
    company_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    job_title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Inquiry classification
    inquiry_type: Mapped[InquiryType] = mapped_column(
        SAEnum(InquiryType, name="inquiry_type"),
        nullable=False,
        default=InquiryType.GENERAL,
        index=True,
    )

    quantity_range: Mapped[QuantityRange | None] = mapped_column(
        SAEnum(QuantityRange, name="quantity_range"),
        nullable=True,
    )

    # Requirement
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Lead context
    source_page: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Internal management
    status: Mapped[InquiryStatus] = mapped_column(
        SAEnum(InquiryStatus, name="inquiry_status"),
        nullable=False,
        default=InquiryStatus.NEW,
        index=True,
    )

    internal_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ORM relationship
    inquiry_products: Mapped[list["InquiryProduct"]] = relationship(
        "InquiryProduct",
        back_populates="inquiry",
        cascade="all, delete-orphan",
    )


class InquiryProduct(Base, TimestampMixin):
    __tablename__ = "inquiry_products"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    inquiry_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("inquiries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    quantity_requested: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "inquiry_id",
            "product_id",
            name="uq_inquiry_product",
        ),
        CheckConstraint(
            "quantity_requested > 0",
            name="ck_inquiry_product_quantity_positive",
        ),
    )

    # ORM relationships
    inquiry: Mapped["Inquiry"] = relationship(
        "Inquiry",
        back_populates="inquiry_products",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="inquiry_products",
    )
