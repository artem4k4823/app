"""post table

Revision ID: b37907cfb332
Revises: 7726f383f08b
Create Date: 2026-01-26 22:17:38.316082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = 'b37907cfb332'
down_revision: Union[str, Sequence[str], None] = '7726f383f08b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.create_table('posts',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('user', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user'], ['users.username'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_table('posts')
    
