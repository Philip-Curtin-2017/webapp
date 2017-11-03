from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
votes = Table('votes', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('crater_id', Integer),
    Column('start_timestamp', DateTime),
    Column('end_timestamp', DateTime),
    Column('vote_result', String(length=1)),
    Column('x1_new', SmallInteger),
    Column('x2_new', SmallInteger),
    Column('y1_new', SmallInteger),
    Column('y2_new', SmallInteger),
    Column('session_data', String(length=120)),
)

CDA_results = Table('CDA_results', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('image', VARCHAR(length=120)),
    Column('x1', SMALLINT),
    Column('x2', SMALLINT),
    Column('y1', SMALLINT),
    Column('y2', SMALLINT),
    Column('GT_conflict', BOOLEAN),
    Column('votes', SMALLINT),
    Column('timestamp', DATETIME),
    Column('score', FLOAT),
    Column('no', SMALLINT),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['votes'].create()
    pre_meta.tables['CDA_results'].columns['no'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['votes'].drop()
    pre_meta.tables['CDA_results'].columns['no'].create()
