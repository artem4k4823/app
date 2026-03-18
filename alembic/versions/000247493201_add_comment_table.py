"""add comment table

Revision ID: 000247493201
Revises: 8f0a70f65295
Create Date: 2026-03-19 00:37:24.616718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '000247493201'
down_revision: Union[str, Sequence[str], None] = '8f0a70f65295'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
   
    op.create_table('coments',
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('user', sa.String(), nullable=False),
    sa.Column('post', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post'], ['posts.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['users.username'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_coments_id'), 'coments', ['id'], unique=False)
    op.add_column('posts', sa.Column('coments', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

   


def downgrade() -> None:
    """Downgrade schema."""
   
    op.drop_column('users', 'is_verified')
    op.drop_column('posts', 'coments')
    op.drop_index(op.f('ix_coments_id'), table_name='coments')
    op.drop_table('coments')
    
