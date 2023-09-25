"""Improve quality

Revision ID: 58a1aa3651e9
Revises: 6e0154238f70
Create Date: 2023-09-25 09:40:55.807827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58a1aa3651e9'
down_revision = '6e0154238f70'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('jav_quality', schema=None) as batch_op:
        batch_op.add_column(sa.Column('priority', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('resolution', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('vr', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('uncensored', sa.Boolean(), nullable=False))

    meta = sa.schema.MetaData()
    meta.reflect(bind=op.get_bind(), only=['jav_quality'])
    qualities = sa.Table('jav_quality', meta)

    op.bulk_insert(qualities, [
        {
            'name': '1080p',
            'priority': 100,
            'resolution': '1080p',
            'vr': False,
            'uncensored': False
        },
        {
            'name': '1080p-UNC',
            'priority': 110,
            'resolution': '1080p',
            'vr': False,
            'uncensored': True
        },
        {
            'name': '4K',
            'priority': -10,
            'resolution': '2160p',
            'vr': False,
            'uncensored': False
        },
        {
            'name': 'VR-4K',
            'priority': 50,
            'resolution': '2160p',
            'vr': True,
            'uncensored': False
        },
        {
            'name': 'VR-8K',
            'priority': 100,
            'resolution': '4096p',
            'vr': True,
            'uncensored': False
        }
    ])

def downgrade():
    op.execute('DELETE FROM jav_quality WHERE name in ("1080p", "1080p-UNC", "4K", "VR-4K", "VR-8K");')

    with op.batch_alter_table('jav_quality', schema=None) as batch_op:
        batch_op.drop_column('uncensored')
        batch_op.drop_column('vr')
        batch_op.drop_column('resolution')
        batch_op.drop_column('priority')

