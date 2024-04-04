"""create user table

Revision ID: 76d4733b17b5
Revises: 7d614b04127b
Create Date: 2024-03-26 02:45:29.650275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76d4733b17b5'
down_revision: Union[str, None] = '7d614b04127b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    )
    


def downgrade() -> None:
    op.drop_table("users")
