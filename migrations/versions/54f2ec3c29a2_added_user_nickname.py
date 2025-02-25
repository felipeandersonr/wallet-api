"""added user nickname

Revision ID: 54f2ec3c29a2
Revises: 7e340a0d967f
Create Date: 2025-02-17 16:17:28.668817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '54f2ec3c29a2'
down_revision: Union[str, None] = '7e340a0d967f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('nickname', sa.String(), nullable=True, unique=True))

    from sqlalchemy.sql import text
    conn = op.get_bind()
    conn.execute(text("UPDATE users SET nickname = CONCAT('user_', id)"))

    op.alter_column('users', 'nickname', nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'nickname')
