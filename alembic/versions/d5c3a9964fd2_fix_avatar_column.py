"""fix avatar column

Revision ID: d5c3a9964fd2
Revises: c9c34fe3efd3
Create Date: 2026-03-10 20:54:08.163153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5c3a9964fd2'
down_revision: Union[str, Sequence[str], None] = 'c9c34fe3efd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column('users', sa.Column('avatar', sa.String(), nullable=True))
    op.drop_column('users', 'image')
   


def downgrade() -> None:
    """Downgrade schema."""
   
    op.add_column('users', sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'avatar')
    
