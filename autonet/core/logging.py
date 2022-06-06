import logging

from flask import g, has_request_context
from flask.logging import default_handler


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
