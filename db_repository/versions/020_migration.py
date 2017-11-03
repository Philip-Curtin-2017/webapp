from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
training_entries = Table('training_entries', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('image', VARCHAR(length=120)),
    Column('x1', SMALLINT),
    Column('x2', SMALLINT),
    Column('y1', SMALLINT),
    Column('y2', SMALLINT),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['training_entries'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['training_entries'].create()
