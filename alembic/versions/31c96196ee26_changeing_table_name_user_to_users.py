"""changeing table name user to users

Revision ID: 31c96196ee26
Revises: 76d4733b17b5
Create Date: 2024-03-26 03:02:52.258463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31c96196ee26'
down_revision: Union[str, None] = '76d4733b17b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('user', 'users')


def downgrade() -> None:
    op.rename_table('users', 'user')
