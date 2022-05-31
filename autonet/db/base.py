from conf_engine.options import StringOption
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker

from autonet.config import config

db_opts = [
    StringOption('connection', default='sqlite://'),
]

config.register_options(db_opts, 'database')
mapper_registry = registry()
engine = create_engine(config.database.connection, echo=config.debug, future=True)
Session = sessionmaker(bind=engine, expire_on_commit=False)

_db_init = False


def init_db():
    if not _db_init:
        mapper_registry.metadata.create_all(engine)
