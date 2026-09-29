from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    and_,
    func,
)
from sqlalchemy import (
    Enum as SqlEnum,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.models import RecordStatus, TimestampMixin

if TYPE_CHECKING:
    from app.modules.brands.model import Brand
    from app.modules.categories.model import Category
    from app.modules.collections.model import Collection
    from app.modules.inquiries.model import InquiryProduct
    from app.modules.product_colors.model import ProductColor
    from app.modules.product_customizations.model import ProductCustomization
    from app.modules.product_details.model import ProductDetail
    from app.modules.product_media.model import ProductMedia
    from app.modules.product_sizes.model import ProductMeasurementGuide, ProductSize


class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    brand_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("brands.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    collection_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    category_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    product_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[RecordStatus] = mapped_column(
        SqlEnum(RecordStatus, name="record_status"),
        nullable=False,
        default=RecordStatus.DRAFT,
        index=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "brand_id",
            "product_code",
            name="uq_products_brand_product_code",
        ),
        UniqueConstraint(
            "brand_id",
            "slug",
            name="uq_products_brand_slug",
        ),
        ForeignKeyConstraint(
            ["collection_id", "brand_id"],
            ["collections.id", "collections.brand_id"],
            ondelete="RESTRICT",
            name="fk_products_collection_brand",
        ),
    )

    collection: Mapped["Collection"] = relationship(
        "Collection",
        back_populates="products",
        primaryjoin=(
            "and_("
            "Product.collection_id == Collection.id, "
            "Product.brand_id == Collection.brand_id"
            ")"
        ),
        foreign_keys="Product.collection_id",
    )

    brand: Mapped["Brand"] = relationship(
        "Brand",
        back_populates="products",
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
    )

    media: Mapped[list["ProductMedia"]] = relationship(
        "ProductMedia",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    details: Mapped["ProductDetail | None"] = relationship(
        "ProductDetail",
        back_populates="product",
        cascade="all, delete-orphan",
        uselist=False,
    )

    colors: Mapped[list["ProductColor"]] = relationship(
        "ProductColor",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    sizes: Mapped[list["ProductSize"]] = relationship(
        "ProductSize",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    measurement_guide: Mapped["ProductMeasurementGuide | None"] = relationship(
        "ProductMeasurementGuide",
        back_populates="product",
        cascade="all, delete-orphan",
        uselist=False,
    )

    customization: Mapped["ProductCustomization | None"] = relationship(
        "ProductCustomization",
        back_populates="product",
        cascade="all, delete-orphan",
        uselist=False,
    )

    inquiry_products: Mapped[list["InquiryProduct"]] = relationship(
        "InquiryProduct",
        back_populates="product",
    )
