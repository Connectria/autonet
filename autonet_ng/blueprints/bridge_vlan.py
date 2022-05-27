from flask import Blueprint, g, request
from typing import Union

from autonet_ng.core import exceptions as exc
from autonet_ng.core.objects import vlan as an_vlan
from autonet_ng.core.response import autonet_response

blueprint = Blueprint('bridge:vlan', __name__)


def _prepare_defaults(request_data: dict) -> dict:
    """
    Setup default parameters for a given request if they are not supplied.
    :param request_data: The request body.
    :return:
    """
    if request_data['admin_enabled'] is None:
        request_data['admin_enabled'] = True
    return request_data


@blueprint.route('/', methods=['GET'])
def get_vlans(device_id):
    def verify(driver_response):
        if not isinstance(driver_response, list):
            return False
        for item in driver_response:
            if not isinstance(item, an_vlan.VLAN):
                return False
        return True

    response = g.driver.execute('bridge:vlan', 'read')
    if not verify(response):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/<vlan_id>', methods=['GET'])
def get_vlan(device_id, vlan_id):
    response = g.driver.execute('bridge:vlan', 'read', request_data=vlan_id)
    if not response:
        raise exc.ObjectNotFound()
    if not isinstance(response, an_vlan.VLAN):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/', methods=['POST'])
def create_vlan(device_id):
    request_data = _prepare_defaults(request.json)
    vlan = an_vlan.VLAN(**request_data)
    if g.driver.execute('bridge:vlan', 'read', request_data=vlan.id):
        raise exc.ObjectExists()
    response = g.driver.execute('bridge:vlan', 'create', request_data=vlan)
    if not isinstance(response, an_vlan.VLAN):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/', methods=['PUT', 'PATCH'])
def _update_vlan(device_id):
    return update_vlan(device_id, None)


@blueprint.route('/<vlan_id>', methods=['PUT', 'PATCH'])
def update_vlan(device_id, vlan_id=None):
    request_data = _prepare_defaults(request.json)
    # We give precedence to the VLAN identified in the URI.
    if vlan_id is not None:
        request_data['id'] = int(vlan_id)

    update = request.method == 'PATCH'
    if update and not g.driver.execute('bridge:vlan', 'read', request_data=request_data['id']):
        raise exc.ObjectNotFound()
    vlan = an_vlan.VLAN(**request_data)
    response = g.driver.execute('bridge:vlan', 'update', request_data=vlan, update=update)
    if not isinstance(response, an_vlan.VLAN):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/<vlan_id>', methods=['DELETE'])
def delete_vlan(device_id, vlan_id):
    if not g.driver.execute('bridge:vlan', 'read', request_data=vlan_id):
        raise exc.ObjectNotFound()
    response = g.driver.execute('bridge:vlan', 'delete', request_data=vlan_id)
    if response is not None:
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(None, 204)
