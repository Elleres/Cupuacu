"""add_dados_user

Revision ID: d0a95da65a06
Revises: 158fd426371f
Create Date: 2025-06-23 21:56:04.505929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'd0a95da65a06'
down_revision: Union[str, None] = '158fd426371f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    user_status_enum = postgresql.ENUM('active', 'deleted', 'on_hold', name='userstatustype')
    user_type_enum = postgresql.ENUM("gerente_laboratorio", "admin", "empresa", name='usertype')

    user_type_enum.create(op.get_bind(), checkfirst=True)
    user_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('user', sa.Column('status', sa.Enum('active', 'deleted', 'on_hold', name='userstatustype'), nullable=False))
    op.add_column('user', sa.Column('type', sa.Enum('admin', 'gerente_laboratorio', 'empresa', name='usertype'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'type')
    op.drop_column('user', 'status')
    # ### end Alembic commands ###
