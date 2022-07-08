import logging

from conf_engine.options import StringOption
from flask import g, has_request_context
from flask.logging import default_handler

from autonet.config import config

logging_opts = [
    StringOption('log_level', default='warning')
]
config.register_options(logging_opts)


class AutonetLogFormatter(logging.Formatter):
    """
    The log formatter for Autonet.
    """

    def format(self, record):
        if has_request_context() and hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            record.request_id = None
        return super().format(record)


def get_log_level() -> int:
    """
    Returns the logging level based on configured parameters.  Log
    level explicitly defined by :code:`log_level` option is used
    except when superseded by :code:`debug` option.

    :return:
    """
    if config.debug:
        return logging.DEBUG
    if config.log_level == 'fatal':
        return logging.FATAL
    elif config.log_level == 'critical':
        return logging.CRITICAL
    elif config.log_level == 'error':
        return logging.ERROR
    elif config.log_level == 'warning':
        return logging.WARNING
    elif config.log_level == 'informational':
        return logging.INFO
    elif config.log_level == 'debug':
        return logging.DEBUG
    else:
        return logging.WARNING


def setup_logging():
    """
    Performs the setup of the :py:class:`AutonetLogFormatter` and
    applies it to the default log handler.
    :return:
    """
    formatter = AutonetLogFormatter(
        '[%(asctime)s][%(levelname)s] (%(request_id)s): %(message)s'
    )
    default_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(get_log_level())
