"""add owner_id to pets and orders

Revision ID: b4f2e8d9c1a3
Revises: 2505f7e521cf
Create Date: 2026-03-25 19:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b4f2e8d9c1a3"
down_revision: Union[str, None] = "2505f7e521cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("pets") as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))
        batch_op.create_index("ix_pets_owner_id", ["owner_id"], unique=False)
        batch_op.create_foreign_key(
            "fk_pets_owner_id_users",
            "users",
            ["owner_id"],
            ["id"],
        )

    with op.batch_alter_table("orders") as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))
        batch_op.create_index("ix_orders_owner_id", ["owner_id"], unique=False)
        batch_op.create_foreign_key(
            "fk_orders_owner_id_users",
            "users",
            ["owner_id"],
            ["id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("orders") as batch_op:
        batch_op.drop_constraint("fk_orders_owner_id_users", type_="foreignkey")
        batch_op.drop_index("ix_orders_owner_id")
        batch_op.drop_column("owner_id")

    with op.batch_alter_table("pets") as batch_op:
        batch_op.drop_constraint("fk_pets_owner_id_users", type_="foreignkey")
        batch_op.drop_index("ix_pets_owner_id")
        batch_op.drop_column("owner_id")
