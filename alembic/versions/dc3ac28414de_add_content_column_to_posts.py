"""add content column to posts

Revision ID: dc3ac28414de
Revises: f36f8f38ece9
Create Date: 2025-07-10 12:57:38.110676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc3ac28414de'
down_revision: Union[str, Sequence[str], None] = 'f36f8f38ece9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('posts', sa.Column("content", sa.String(), nullable = False))

    pass


def downgrade() :
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
