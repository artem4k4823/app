"""Initial migration

Revision ID: a148a87cf912
Revises: 
Create Date: 2026-01-04 22:48:18.890998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a148a87cf912'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # We do nothing here to preserve the existing users table
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
