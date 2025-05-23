"""Add subscription month price for server

Revision ID: 166d0634dfce
Revises: b1d3d196dc52
Create Date: 2025-03-27 20:27:39.649895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '166d0634dfce'
down_revision: Union[str, None] = 'b1d3d196dc52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('servers', sa.Column('month_price', sa.DECIMAL(precision=10, scale=2), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('servers', 'month_price')
    # ### end Alembic commands ###
