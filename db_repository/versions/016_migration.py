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
    Column('var1', String(length=120)),
    Column('var2', String(length=120)),
)

CDA_results = Table('CDA_results', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('image', String(length=120)),
    Column('x1', SmallInteger),
    Column('x2', SmallInteger),
    Column('y1', SmallInteger),
    Column('y2', SmallInteger),
    Column('score', Float),
    Column('GT_conflict', Boolean, default=ColumnDefault(True)),
    Column('votes', SmallInteger, default=ColumnDefault(0)),
    Column('timestamp', DateTime),
    Column('var1', String(length=120)),
    Column('var2', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['votes'].columns['var1'].create()
    post_meta.tables['votes'].columns['var2'].create()
    post_meta.tables['CDA_results'].columns['var1'].create()
    post_meta.tables['CDA_results'].columns['var2'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['votes'].columns['var1'].drop()
    post_meta.tables['votes'].columns['var2'].drop()
    post_meta.tables['CDA_results'].columns['var1'].drop()
    post_meta.tables['CDA_results'].columns['var2'].drop()
