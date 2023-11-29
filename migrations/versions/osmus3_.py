"""add layer_tag_value column to projects table

Revision ID: osmus3
Revises: osmus2
Create Date: 2023-11-29

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "osmus3"
down_revision = "osmus2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("projects", sa.Column("layer_tag_value", sa.String(), nullable=True))


def downgrade():
    op.drop_column("projects", "layer_tag_value")
