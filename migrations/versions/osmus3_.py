"""
default projects.database to '' instead of 0

Originally this column was a boolean-ish integer, but was converted to a string
later to support multiple sandboxes (the string is the DNS name of the sandbox).

This prevents the default from being incorrectly cast to the string '0' if no
value is provided by the client.

Revision ID: osmus3
Revises: 6276c258149c
Create Date: 2026-07-31

"""
from alembic import op

revision = "osmus3"
down_revision = "6276c258149c"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("ALTER TABLE projects ALTER COLUMN database SET DEFAULT ''")

def downgrade():
    op.execute("ALTER TABLE projects ALTER COLUMN database SET DEFAULT 0")
