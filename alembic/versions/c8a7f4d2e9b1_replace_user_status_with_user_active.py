"""replace userStatus with user_active

Revision ID: c8a7f4d2e9b1
Revises: b4f2e8d9c1a3
Create Date: 2026-03-25 20:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c8a7f4d2e9b1"
down_revision: Union[str, None] = "b4f2e8d9c1a3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "user_active",
                sa.Boolean(),
                nullable=False,
                server_default=sa.text("1"),
            )
        )

    op.execute("UPDATE users SET user_active = CASE WHEN userStatus = 1 THEN 1 ELSE 0 END")

    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("userStatus")


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("userStatus", sa.Integer(), nullable=True))

    op.execute("UPDATE users SET userStatus = CASE WHEN user_active = 1 THEN 1 ELSE 0 END")

    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("user_active")
