from uuid import UUID

from sqlalchemy import Enum, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base import Base
from app.core.models import RecordStatus, TimestampMixin


class CompanyKnowledge(TimestampMixin, Base):
    __tablename__ = "company_knowledge"

    id: Mapped[UUID] = mapped_column(
        Uuid, primary_key=True, server_default=func.gen_random_uuid()
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[RecordStatus] = mapped_column(
        Enum(
            RecordStatus,
            name="company_knowledge_status",
        ),
        nullable=False,
        default=RecordStatus.DRAFT,
        index=True,
    )
