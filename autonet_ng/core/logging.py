import logging

from flask import g, has_request_context
from flask.logging import default_handler


class AutonetLogFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context() and hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            record.request_id = None
        return super().format(record)


def setup_logging():
    formatter = AutonetLogFormatter(
        '[%(asctime)s][%(levelname)s] (%(request_id)s): %(message)s'
    )
    default_handler.setFormatter(formatter)
