from flask import Blueprint, g, request

from autonet_ng.core import exceptions as exc
from autonet_ng.core.objects import vlan as an_vlan
from autonet_ng.core.response import autonet_response

blueprint = Blueprint('bridge:vlan', __name__)


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
def get_vrf(device_id, vlan_id):
    response = g.driver.execute('bridge:vlan', 'read', request_data=vlan_id)
    if not isinstance(response, an_vlan.VLAN):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/', methods=['POST'])
def create_vrf(device_id):
    vlan = an_vlan.VLAN(**request.json)
    response = g.driver.execute('bridge:vlan', 'create', request_data=vlan)
    if not isinstance(response, an_vlan.VLAN):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/<vlan_id>', methods=['DELETE'])
def delete_vrf(device_id, vlan_id):
    response = g.driver.execute('bridge:vlan', 'delete', request_data=vlan_id)
    if response is not None:
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(None, 204)
