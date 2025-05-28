"""create initial tables

Revision ID: 001
Revises:
Create Date: 2024-05-25 19:15:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'box_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'boxes',
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('box_type_id', sa.Integer(), nullable=False),
        sa.Column('weight', sa.Numeric(10, 2), nullable=False),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('price_currency', sa.String(length=3), nullable=False),
        sa.Column('delivery_price', sa.Numeric(10, 2), nullable=True),
        sa.Column('delivery_currency', sa.String(length=3), nullable=True),
        sa.ForeignKeyConstraint(['box_type_id'],
                                ['box_types.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_boxes_user_id'), 'boxes', ['user_id'], unique=False)


    # Insert default box types
    box_types_table = sa.table(
        'box_types',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
    )

    op.bulk_insert(
        box_types_table,
        [
            {"id": 1, "name": "Clothing"},
            {"id": 2, "name": "Electronics"},
            {"id": 3, "name": "Other"},
        ],
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_boxes_user_id'), table_name='boxes')
    op.drop_table('boxes')
    op.drop_table('box_types')
