"""add like column for post, add email column for user

Revision ID: 8f0a70f65295
Revises: 6a399954bae5
Create Date: 2026-03-18 17:19:18.345789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f0a70f65295'
down_revision: Union[str, Sequence[str], None] = '6a399954bae5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
   
    op.add_column('posts', sa.Column('likes', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('users', sa.Column('email', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'users', ['email'])
    


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'email')
    op.drop_column('posts', 'likes')
    
