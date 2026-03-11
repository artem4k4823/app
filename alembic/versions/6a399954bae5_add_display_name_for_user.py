"""add display name for user

Revision ID: 6a399954bae5
Revises: d154d6d45958
Create Date: 2026-03-11 21:07:52.529972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a399954bae5'
down_revision: Union[str, Sequence[str], None] = 'd154d6d45958'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
  
    op.add_column('users', sa.Column('displayName', sa.String(), nullable=False, server_default=''))
   


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_column('users', 'displayName')
    
