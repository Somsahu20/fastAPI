"""Add User Table

Revision ID: be2a5833ff3d
Revises: 254678f2aecd
Create Date: 2025-12-27 00:38:07.249706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = 'be2a5833ff3d'
down_revision: Union[str, Sequence[str], None] = '254678f2aecd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",
        sa.Column("id", sa.Integer,  primary_key=True, nullable=False, autoincrement=True),
        sa.Column("emial", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default = sa.text('now()'))
        )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
