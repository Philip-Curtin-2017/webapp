from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
votes = Table('votes', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('crater_id', INTEGER),
    Column('start_timestamp', DATETIME),
    Column('end_timestamp', DATETIME),
    Column('vote_result', VARCHAR(length=1)),
    Column('x1_new', SMALLINT),
    Column('x2_new', SMALLINT),
    Column('y1_new', SMALLINT),
    Column('y2_new', SMALLINT),
    Column('session_data', VARCHAR(length=120)),
    Column('var1', VARCHAR(length=120)),
    Column('var2', VARCHAR(length=120)),
)

votes = Table('votes', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('crater_id', Integer),
    Column('start_timestamp', DateTime),
    Column('end_timestamp', DateTime),
    Column('vote', String(length=20)),
    Column('x1_new', SmallInteger),
    Column('x2_new', SmallInteger),
    Column('y1_new', SmallInteger),
    Column('y2_new', SmallInteger),
    Column('session_data', String(length=120)),
    Column('var1', String(length=120)),
    Column('var2', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['votes'].columns['vote_result'].drop()
    post_meta.tables['votes'].columns['vote'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['votes'].columns['vote_result'].create()
    post_meta.tables['votes'].columns['vote'].drop()
