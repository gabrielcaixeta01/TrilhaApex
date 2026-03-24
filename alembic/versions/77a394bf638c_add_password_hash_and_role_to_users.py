"""add password_hash and role to users

Revision ID: 77a394bf638c
Revises: 9c704e7c9c45
Create Date: 2026-03-24 15:28:09.950585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77a394bf638c'
down_revision: Union[str, None] = '9c704e7c9c45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("password_hash", sa.String(), nullable=True))
    op.add_column(
        "users",
        sa.Column("role", sa.String(), nullable=False, server_default=sa.text("'user'")),
    )

    # Backfill existing rows to keep compatibility with previous schema.
    op.execute("UPDATE users SET password_hash = password WHERE password_hash IS NULL")
    op.execute("UPDATE users SET role = 'user' WHERE role IS NULL")


def downgrade() -> None:
    op.drop_column("users", "role")
    op.drop_column("users", "password_hash")
