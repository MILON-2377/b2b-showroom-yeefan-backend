"""add deletion pending media asset enum value

Revision ID: 0767591b2259
Revises: 6197dd1fed3c
Create Date: 2026-10-06 05:55:57.243268

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0767591b2259"
down_revision: Union[str, Sequence[str], None] = "6197dd1fed3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE media_asset_status ADD VALUE IF NOT EXISTS 'DELETION_PENDING'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
