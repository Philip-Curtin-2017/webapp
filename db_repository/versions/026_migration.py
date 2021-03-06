from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
CDA_results = Table('CDA_results', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('image', String(length=120)),
    Column('x1', SmallInteger),
    Column('x2', SmallInteger),
    Column('y1', SmallInteger),
    Column('y2', SmallInteger),
    Column('score', Float),
    Column('GT_conflict', Boolean),
    Column('votes', SmallInteger, default=ColumnDefault(0)),
    Column('timestamp', DateTime),
    Column('IOU', Float),
    Column('var1', String(length=120)),
    Column('var2', String(length=120)),
    Column('recenter_id', Integer),
    Column('vote_result', String(length=120)),
    Column('results_yes', SmallInteger),
    Column('results_no', SmallInteger),
    Column('results_unsure', SmallInteger),
    Column('results_recenter', SmallInteger),
    Column('results_SU_vote', SmallInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['CDA_results'].columns['results_SU_vote'].create()
    post_meta.tables['CDA_results'].columns['results_no'].create()
    post_meta.tables['CDA_results'].columns['results_recenter'].create()
    post_meta.tables['CDA_results'].columns['results_unsure'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['CDA_results'].columns['results_SU_vote'].drop()
    post_meta.tables['CDA_results'].columns['results_no'].drop()
    post_meta.tables['CDA_results'].columns['results_recenter'].drop()
    post_meta.tables['CDA_results'].columns['results_unsure'].drop()
