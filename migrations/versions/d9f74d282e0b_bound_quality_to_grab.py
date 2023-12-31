"""bound quality to grab

Revision ID: d9f74d282e0b
Revises: faf2989ad09c
Create Date: 2023-09-29 10:34:33.576895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9f74d282e0b'
down_revision = 'faf2989ad09c'
branch_labels = None
depends_on = None


def upgrade():
    naming_convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }

    op.execute('DELETE FROM jav_quality;')
    with op.batch_alter_table('grab_history', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.add_column(sa.Column('quality_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_grab_history_quality_id_jav_quality', 'jav_quality', ['quality_id'], ['id'])

    with op.batch_alter_table('jav_movie', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint('fk_jav_movie_quality_id_jav_quality', type_='foreignkey')
        batch_op.drop_column('quality_id')

    with op.batch_alter_table('jav_quality', schema=None) as batch_op:
        batch_op.add_column(sa.Column('def_1080p', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('def_4k', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('def_8k', sa.Boolean(), nullable=False))
        batch_op.drop_column('resolution')

    meta = sa.schema.MetaData()
    meta.reflect(bind=op.get_bind(), only=['jav_quality'])
    qualities = sa.Table('jav_quality', meta)

    op.bulk_insert(qualities, [
        {
            'name': '1080p',
            'priority': 50,
            'def_1080p': True,
            'def_4k': False,
            'def_8k': False,
            'vr': False,
            'uncensored': False
        },
        {
            'name': '1080p-UNC',
            'priority': 100,
            'def_1080p': True,
            'def_4k': False,
            'def_8k': False,
            'vr': False,
            'uncensored': True
        },
        {
            'name': '4K',
            'priority': -10,
            'def_1080p': False,
            'def_4k': True,
            'def_8k': False,
            'vr': False,
            'uncensored': False
        },
        {
            'name': 'VR-4K',
            'priority': 50,
            'def_1080p': False,
            'def_4k': True,
            'def_8k': False,
            'vr': True,
            'uncensored': False
        },
        {
            'name': 'VR-8K',
            'priority': 100,
            'def_1080p': False,
            'def_4k': False,
            'def_8k': True,
            'vr': True,
            'uncensored': False
        }
    ])


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jav_quality', schema=None) as batch_op:
        batch_op.add_column(sa.Column('resolution', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('def_8k')
        batch_op.drop_column('def_4k')
        batch_op.drop_column('def_1080p')

    with op.batch_alter_table('jav_movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quality_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(None, 'jav_quality', ['quality_id'], ['id'])

    with op.batch_alter_table('grab_history', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('quality_id')

    op.create_table('jav_quality_mapper',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('jav_quality_id', sa.INTEGER(), nullable=False),
    sa.Column('mapper', sa.VARCHAR(), nullable=False),
    sa.Column('regex_vr', sa.VARCHAR(), nullable=False),
    sa.Column('regex_uncensored', sa.VARCHAR(), nullable=False),
    sa.Column('regex_resolution', sa.VARCHAR(), nullable=False),
    sa.ForeignKeyConstraint(['jav_quality_id'], ['jav_quality.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
