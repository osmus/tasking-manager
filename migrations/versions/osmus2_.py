"""add databases (OSM vs. SANDBOX) column to orgs table

Revision ID: osmus2
Revises: osmus1
Create Date: 2023-01-30

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "osmus2"
down_revision = "osmus1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("organisations",
        sa.Column("databases",
            postgresql.ARRAY(sa.Integer()),
            server_default="{0}",
            nullable=False
        )
    )
            


def downgrade():
    op.drop_column("organisations", "databases")
