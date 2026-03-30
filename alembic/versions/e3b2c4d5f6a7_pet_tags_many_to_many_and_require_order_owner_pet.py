"""pet tags many-to-many and require order owner/pet

Revision ID: e3b2c4d5f6a7
Revises: d1f3a9b6c2e4
Create Date: 2026-03-30 21:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e3b2c4d5f6a7"
down_revision: Union[str, None] = "d1f3a9b6c2e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    # Ensure we can safely enforce NOT NULL on orders.
    orders_without_pet = bind.execute(sa.text('SELECT COUNT(*) FROM "orders" WHERE "petId" IS NULL')).scalar_one()
    orders_without_owner = bind.execute(sa.text('SELECT COUNT(*) FROM "orders" WHERE owner_id IS NULL')).scalar_one()
    if orders_without_pet or orders_without_owner:
        raise RuntimeError(
            "Nao foi possivel aplicar migration: existem pedidos sem petId ou owner_id. "
            "Corrija os dados antes de migrar."
        )

    op.create_table(
        "pet_tags",
        sa.Column("pet_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["pet_id"], ["pets.id"]),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"]),
        sa.PrimaryKeyConstraint("pet_id", "tag_id"),
    )

    # Migrate existing single-tag relation to association table.
    bind.execute(
        sa.text(
            'INSERT INTO pet_tags (pet_id, tag_id) '
            'SELECT id, tag_id FROM pets WHERE tag_id IS NOT NULL'
        )
    )

    with op.batch_alter_table("pets") as batch_op:
        batch_op.drop_constraint("fk_pets_tag_id_tags", type_="foreignkey")
        batch_op.drop_index("ix_pets_tag_id")
        batch_op.drop_column("tag_id")

    with op.batch_alter_table("orders") as batch_op:
        batch_op.alter_column("petId", existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column("owner_id", existing_type=sa.Integer(), nullable=False)


def downgrade() -> None:
    with op.batch_alter_table("orders") as batch_op:
        batch_op.alter_column("owner_id", existing_type=sa.Integer(), nullable=True)
        batch_op.alter_column("petId", existing_type=sa.Integer(), nullable=True)

    with op.batch_alter_table("pets") as batch_op:
        batch_op.add_column(sa.Column("tag_id", sa.Integer(), nullable=True))
        batch_op.create_index("ix_pets_tag_id", ["tag_id"], unique=False)
        batch_op.create_foreign_key(
            "fk_pets_tag_id_tags",
            "tags",
            ["tag_id"],
            ["id"],
        )

    bind = op.get_bind()
    bind.execute(
        sa.text(
            'UPDATE pets SET tag_id = ('
            'SELECT MIN(pt.tag_id) FROM pet_tags pt WHERE pt.pet_id = pets.id'
            ')'
        )
    )

    op.drop_table("pet_tags")
