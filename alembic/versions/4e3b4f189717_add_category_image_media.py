"""add category image media

Revision ID: 4e3b4f189717
Revises: ddd1a54f84cd
Create Date: 2026-09-30 21:49:49.046877

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4e3b4f189717"
down_revision: Union[str, Sequence[str], None] = "ddd1a54f84cd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "categories",
        sa.Column("image_media_id", sa.UUID(), nullable=True),
    )

    op.create_index(
        op.f("ix_categories_image_media_id"),
        "categories",
        ["image_media_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_categories_image_media_id_media_assets",
        "categories",
        "media_assets",
        ["image_media_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_categories_image_media_id_media_assets",
        "categories",
        type_="foreignkey",
    )

    op.drop_index(
        op.f("ix_categories_image_media_id"),
        table_name="categories",
    )

    op.drop_column(
        "categories",
        "image_media_id",
    )
