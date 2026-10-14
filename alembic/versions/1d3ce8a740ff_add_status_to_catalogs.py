"""add status to catalogs

Revision ID: 1d3ce8a740ff
Revises: 640ad4575aaf
Create Date: 2026-10-09 12:12:16.854232

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1d3ce8a740ff"
down_revision: Union[str, Sequence[str], None] = "640ad4575aaf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "catalogs",
        sa.Column(
            "status",
            postgresql.ENUM(
                "DRAFT",
                "PUBLISHED",
                "ARCHIVED",
                name="record_status",
                create_type=False,
            ),
            server_default="DRAFT",
            nullable=False,
        ),
    )

    op.create_index(
        op.f("ix_catalogs_status"),
        "catalogs",
        ["status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_catalogs_status"),
        table_name="catalogs",
    )

    op.drop_column(
        "catalogs",
        "status",
    )
