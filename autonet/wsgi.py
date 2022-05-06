import logging

from config_engine import config
from config_engine.options import NumberOption, StringOption

from autonet.core.app import flask_app
from autonet.db import init_db

opts = [
    StringOption('bind_host'),
    NumberOption('port', minimum=1, maximum=65535)
]
config.register_options(opts)

LOG = logging.getLogger()


def run_wsgi_app():
    LOG.info("Application started via CLI.")
    init_db()
    flask_app.run(config.bind_host, config.port)

