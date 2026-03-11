"""add avatar column

Revision ID: c9c34fe3efd3
Revises: e9178b431546
Create Date: 2026-03-10 20:30:56.998502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9c34fe3efd3'
down_revision: Union[str, Sequence[str], None] = 'e9178b431546'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column('users', sa.Column('image', sa.String(), nullable=True))
    


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_column('users', 'image')
    
