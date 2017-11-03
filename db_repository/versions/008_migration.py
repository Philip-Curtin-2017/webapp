from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
results = Table('results', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('image', VARCHAR(length=120)),
    Column('x1', SMALLINT),
    Column('x2', SMALLINT),
    Column('y1', SMALLINT),
    Column('y2', SMALLINT),
    Column('GT_status', VARCHAR(length=2)),
    Column('score', FLOAT),
    Column('votes', SMALLINT),
    Column('yes', INTEGER),
    Column('no', INTEGER),
    Column('unsure', SMALLINT),
    Column('result', SMALLINT),
    Column('timestamp', DATETIME),
    Column('testentry', BOOLEAN),
    Column('testanswer', BOOLEAN),
)

CDA_results = Table('CDA_results', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('image', String(length=120)),
    Column('x1', SmallInteger),
    Column('x2', SmallInteger),
    Column('y1', SmallInteger),
    Column('y2', SmallInteger),
    Column('GT_conflict', Boolean, default=ColumnDefault(False)),
    Column('score', Float),
    Column('votes', SmallInteger, default=ColumnDefault(0)),
    Column('yes', SmallInteger, default=ColumnDefault(0)),
    Column('no', SmallInteger, default=ColumnDefault(0)),
    Column('unsure', SmallInteger, default=ColumnDefault(0)),
    Column('result', SmallInteger, default=ColumnDefault(3)),
    Column('timestamp', DateTime),
)

training_entries = Table('training_entries', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('image', String(length=120)),
    Column('x1', SmallInteger),
    Column('x2', SmallInteger),
    Column('y1', SmallInteger),
    Column('y2', SmallInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['results'].drop()
    post_meta.tables['CDA_results'].create()
    post_meta.tables['training_entries'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['results'].create()
    post_meta.tables['CDA_results'].drop()
    post_meta.tables['training_entries'].drop()
