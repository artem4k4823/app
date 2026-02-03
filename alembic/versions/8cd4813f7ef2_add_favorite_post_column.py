"""add favorite post column

Revision ID: 8cd4813f7ef2
Revises: b37907cfb332
Create Date: 2026-01-29 21:40:24.086572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cd4813f7ef2'
down_revision: Union[str, Sequence[str], None] = 'b37907cfb332'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column('users', sa.Column('favorite_posts_ids', sa.JSON(), nullable=True))
   


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_column('users', 'favorite_posts_ids')
    
