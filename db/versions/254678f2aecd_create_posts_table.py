"""create posts table

Revision ID: 254678f2aecd
Revises: 
Create Date: 2025-12-26 13:08:23.340463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '254678f2aecd'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.String(length=255), nullable=False),
        sa.Column('is_published', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('user_id', sa.Integer, nullable=False)
        # sa.ForeignKeyConstraint(['user_id'])
    )
    #todo: Runs the command for the changes you wanna do


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    #todo: Runs the command for reverting back to previous state
