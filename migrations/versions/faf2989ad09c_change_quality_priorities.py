"""change quality priorities

Revision ID: faf2989ad09c
Revises: 58a1aa3651e9
Create Date: 2023-09-25 16:27:42.627298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faf2989ad09c'
down_revision = '58a1aa3651e9'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('UPDATE jav_quality SET priority = "90" WHERE name = "1080p"')
    op.execute('UPDATE jav_quality SET priority = "100" WHERE name = "1080p-UNC"')


def downgrade():
    op.execute('UPDATE jav_quality SET priority = "100" WHERE name = "1080p"')
    op.execute('UPDATE jav_quality SET priority = "110" WHERE name = "1080p-UNC"')
