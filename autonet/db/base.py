from conf_engine.options import BooleanOption, NumberOption, StringOption
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker

from autonet.config import config

db_opts = [
    StringOption('connection', default='sqlite:///'),
    NumberOption('pool_recycle', default=3600),
    BooleanOption('pool_pre_ping', default=True)
]

config.register_options(db_opts, 'database')
mapper_registry = registry()
engine = create_engine(config.database.connection, echo=config.debug,
                       future=True, pool_pre_ping=config.database.pool_pre_ping,
                       pool_recycle=config.database.pool_recycle)
Session = sessionmaker(bind=engine, expire_on_commit=False)


def init_db():
    mapper_registry.metadata.create_all(engine)
