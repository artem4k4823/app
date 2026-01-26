"""fix token models

Revision ID: 7726f383f08b
Revises: 0efe2bdba414
Create Date: 2026-01-26 21:04:57.541792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7726f383f08b'
down_revision: Union[str, Sequence[str], None] = '0efe2bdba414'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.alter_column('tokens', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint(op.f('tokens_user_id_fkey'), 'tokens', type_='foreignkey')
    op.create_foreign_key(None, 'tokens', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_constraint(None, 'tokens', type_='foreignkey')
    op.create_foreign_key(op.f('tokens_user_id_fkey'), 'tokens', 'users', ['user_id'], ['id'])
    op.alter_column('tokens', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    
