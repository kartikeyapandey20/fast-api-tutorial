"""add foregin key to post table

Revision ID: 61f8b1f3686f
Revises: 31c96196ee26
Create Date: 2024-03-26 03:03:43.277718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61f8b1f3686f'
down_revision: Union[str, None] = '31c96196ee26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("posts_users_fk",source_table="posts",referent_table="users",
                          local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("posts_users_fk",table_name="posts",)
    op.drop_column("posts","owner_id")
