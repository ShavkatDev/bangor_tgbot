"""add group_id to users

Revision ID: 3513b3682e90
Revises: c9074278262c
Create Date: 2025-04-04 17:44:57.538974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3513b3682e90'
down_revision: Union[str, None] = 'c9074278262c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schedule_cache',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('data', sa.Text(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schedule_cache_date'), 'schedule_cache', ['date'], unique=False)
    op.create_index(op.f('ix_schedule_cache_group_id'), 'schedule_cache', ['group_id'], unique=False)
    op.add_column('users', sa.Column('group_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_users_group_id'), 'users', ['group_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_group_id'), table_name='users')
    op.drop_column('users', 'group_id')
    op.drop_index(op.f('ix_schedule_cache_group_id'), table_name='schedule_cache')
    op.drop_index(op.f('ix_schedule_cache_date'), table_name='schedule_cache')
    op.drop_table('schedule_cache')
    # ### end Alembic commands ###
