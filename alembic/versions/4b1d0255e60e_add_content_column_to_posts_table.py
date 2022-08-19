"""add content column to posts table

Revision ID: 4b1d0255e60e
Revises: dcd50549b097
Create Date: 2022-08-12 13:36:57.539708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b1d0255e60e'
down_revision = 'dcd50549b097'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('content', sa.String(), nullable=False)
                  )
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
