""" add to post onupdate

Revision ID: d154d6d45958
Revises: d5c3a9964fd2
Create Date: 2026-03-11 20:48:25.530378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd154d6d45958'
down_revision: Union[str, Sequence[str], None] = 'd5c3a9964fd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.drop_constraint(op.f('posts_user_fkey'), 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['user'], ['username'], onupdate='CASCADE', ondelete='CASCADE')
    


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key(op.f('posts_user_fkey'), 'posts', 'users', ['user'], ['username'], ondelete='CASCADE')
   
