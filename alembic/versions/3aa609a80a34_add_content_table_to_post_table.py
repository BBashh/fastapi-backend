"""add content table to post table

Revision ID: 3aa609a80a34
Revises: ebb74fd27de0
Create Date: 2025-10-06 19:34:35.128184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3aa609a80a34'
down_revision: Union[str, Sequence[str], None] = 'ebb74fd27de0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
