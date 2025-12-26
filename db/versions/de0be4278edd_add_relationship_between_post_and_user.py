"""Add relationship between post and user

Revision ID: de0be4278edd
Revises: be2a5833ff3d
Create Date: 2025-12-27 00:51:20.194542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de0be4278edd'
down_revision: Union[str, Sequence[str], None] = 'be2a5833ff3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.create_foreign_key(
        'fk_posts_user_id_users',
        source_table= "posts",
        referent_table= "users",
        local_cols= ['user_id'],
        remote_cols= ['id'],
        ondelete='CASCADE',
        onupdate='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint('fk_posts_user_id_users', table_name= 'posts', type_='foreignkey')
    
