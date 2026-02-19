"""add chats column for users

Revision ID: e9178b431546
Revises: 3659e415b6ba
Create Date: 2026-02-19 20:26:56.374799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e9178b431546'
down_revision: Union[str, Sequence[str], None] = '3659e415b6ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column('users', sa.Column('chats', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    


def downgrade() -> None:
    """Downgrade schema."""
   
    op.drop_column('users', 'chats')
    
