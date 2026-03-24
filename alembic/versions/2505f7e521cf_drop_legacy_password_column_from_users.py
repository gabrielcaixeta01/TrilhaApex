"""drop legacy password column from users

Revision ID: 2505f7e521cf
Revises: 77a394bf638c
Create Date: 2026-03-24 15:35:09.315880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2505f7e521cf'
down_revision: Union[str, None] = '77a394bf638c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("password")


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("password", sa.String(), nullable=True))
