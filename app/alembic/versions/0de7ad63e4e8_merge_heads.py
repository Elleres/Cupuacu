"""Merge heads

Revision ID: 0de7ad63e4e8
Revises: 4514ea0a4827, aecfd7808371
Create Date: 2025-06-04 17:12:39.357399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0de7ad63e4e8'
down_revision: Union[str, None] = ('4514ea0a4827', 'aecfd7808371')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
