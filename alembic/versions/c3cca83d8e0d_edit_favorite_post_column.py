"""edit favorite post column

Revision ID: c3cca83d8e0d
Revises: 8cd4813f7ef2
Create Date: 2026-01-29 21:58:47.204780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c3cca83d8e0d'
down_revision: Union[str, Sequence[str], None] = '8cd4813f7ef2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.alter_column('users', 'favorite_posts_ids',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               type_=postgresql.JSONB(astext_type=sa.Text()),
               existing_nullable=True)
    


def downgrade() -> None:
    """Downgrade schema."""
    
    op.alter_column('users', 'favorite_posts_ids',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               type_=postgresql.JSON(astext_type=sa.Text()),
               existing_nullable=True)
    
