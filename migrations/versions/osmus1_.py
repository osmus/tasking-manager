"""add database (OSM vs. SANDBOX) column to projects table

Revision ID: osmus1
Revises: a9cbd2c6c213
Create Date: 2023-01-30

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "osmus1"
down_revision = "a9cbd2c6c213"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "projects", sa.Column("database", sa.Integer(), server_default=sa.literal(0), nullable=False)
    )


def downgrade():
    op.drop_column("projects", "database")
