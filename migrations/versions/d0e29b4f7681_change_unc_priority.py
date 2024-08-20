"""Change UNC priority

Revision ID: d0e29b4f7681
Revises: d9f74d282e0b
Create Date: 2024-08-20 15:36:47.699931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0e29b4f7681'
down_revision = 'd9f74d282e0b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('UPDATE jav_quality SET priority = "100" WHERE name = "1080p"')
    op.execute('UPDATE jav_quality SET priority = "50" WHERE name = "1080p-UNC"')


def downgrade():
    op.execute('UPDATE jav_quality SET priority = "90" WHERE name = "1080p"')
    op.execute('UPDATE jav_quality SET priority = "100" WHERE name = "1080p-UNC"')
