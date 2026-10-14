"""add deletion pending media asset status

Revision ID: 6197dd1fed3c
Revises: 7d67178d97ca
Create Date: 2026-10-06 05:51:03.139868

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6197dd1fed3c"
down_revision: Union[str, Sequence[str], None] = "7d67178d97ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "ALTER TYPE media_asset_status "
        "ADD VALUE IF NOT EXISTS 'DELETION_PENDING'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass