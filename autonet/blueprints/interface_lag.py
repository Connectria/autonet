from flask import Blueprint, g, request, Request

from autonet.core import exceptions as exc
from autonet.core.objects import lag as an_lag
from autonet.core.response import autonet_response

blueprint = Blueprint('lag', __name__)


@blueprint.route('/', methods=['GET'])
def get_lags(device_id):
    def verify(driver_response):
        if not isinstance(driver_response, list):
            return False
        for item in driver_response:
            if not isinstance(item, an_lag.LAG):
                return False
        return True

    response = g.driver.execute('interface:lag', 'read')
    if not verify(response):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/<lag_id>', methods=['GET'])
def get_lag(device_id, lag_id):
    response = g.driver.execute('interface:lag', 'read', request_data=lag_id)
    if not response:
        raise exc.ObjectNotFound()
    if not isinstance(response, an_lag.LAG):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/', methods=['POST'])
def create_lag(device_id):
    lag = an_lag.LAG(**request.json)
    # Verify the LAG does not already exist.
    if g.driver.execute('interface:lag', 'read', request_data=lag.name):
        raise exc.ObjectExists()
    response = g.driver.execute('interface:lag', 'create', request_data=lag)
    if not isinstance(response, an_lag.LAG):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response, 201)

@blueprint.route('/<lag_id>', methods=['PUT', 'PATCH'])
def update_lag(device_id, lag_id):
    update = request.method == 'PATCH'
    if update and not g.driver.execute('interface:lag', 'read', request_data=lag_id):
        raise exc.ObjectNotFound()
    lag = an_lag.LAG(**request.json)
    response = g.driver.execute('interface:lag', 'update', request_data=lag, update=update)
    if not isinstance(response, an_lag.LAG):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)

@blueprint.route('/<lag_id>', methods=['DELETE'])
def delete_lag(device_id, lag_id):
    if not g.driver.execute('interface:lag', 'read', request_data=lag_id):
        raise exc.ObjectNotFound()
    response = g.driver.execute('interface:lag', 'delete', request_data=lag_id)

    if response is not None:
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(None, 204)
