import logging

from flask import g, jsonify
from werkzeug.exceptions import MethodNotAllowed, NotFound

import autonet.core.exceptions as exc

from autonet.config import config

def autonet_response(response=None, status=None, headers=None):
    if g.errors and not status:
        status = 500
    for error in g.errors:
        if isinstance(error, exc.RequestValueMissing):
            status = 400
        if isinstance(error, (NotFound, exc.ObjectNotFound)):
            status = 404
        if isinstance(error, MethodNotAllowed):
            status = 405
        if isinstance(error, exc.ObjectExists):
            status = 409
        if isinstance(error, exc.DriverOperationUnsupported) \
                or isinstance(error, exc.DeviceOperationUnsupported):
            status = 501
    errors = [str(error) for error in g.errors]
    if errors and config.debug:
        logging.debug(errors)
    response = jsonify({
        "request-id": g.request_id,
        "data": response,
        "errors": errors,
        "status": status or 200
    })
    return response, status, headers
