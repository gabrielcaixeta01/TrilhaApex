"""add tag_id to pets

Revision ID: d1f3a9b6c2e4
Revises: c8a7f4d2e9b1
Create Date: 2026-03-25 20:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d1f3a9b6c2e4"
down_revision: Union[str, None] = "c8a7f4d2e9b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("pets") as batch_op:
        batch_op.add_column(sa.Column("tag_id", sa.Integer(), nullable=True))
        batch_op.create_index("ix_pets_tag_id", ["tag_id"], unique=False)
        batch_op.create_foreign_key(
            "fk_pets_tag_id_tags",
            "tags",
            ["tag_id"],
            ["id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("pets") as batch_op:
        batch_op.drop_constraint("fk_pets_tag_id_tags", type_="foreignkey")
        batch_op.drop_index("ix_pets_tag_id")
        batch_op.drop_column("tag_id")
