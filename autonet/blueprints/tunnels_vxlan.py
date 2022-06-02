from flask import Blueprint, g, request

from autonet.core import exceptions as exc
from autonet.core.objects import vxlan as an_vxlan
from autonet.core.response import autonet_response

blueprint = Blueprint('vxlan', __name__)


@blueprint.route('/vxlan/', methods=['GET'])
def get_tunnels(device_id):
    def verify(driver_response):
        if not isinstance(driver_response, list):
            return False
        for item in driver_response:
            if not isinstance(item, an_vxlan.VXLAN):
                return False
        return True

    result = g.driver.execute('tunnels:vxlan', 'read')
    if not verify(result):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(result)


@blueprint.route('/vxlan/<vni>', methods=['GET'])
def get_tunnel(device_id, vni):
    response = g.driver.execute('tunnels:vxlan', 'read', request_data=vni)
    if not response:
        raise exc.ObjectNotFound()
    if not isinstance(response, an_vxlan.VXLAN):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/vxlan', methods=['POST'])
def create_tunnel(device_id):
    vxlan = an_vxlan.VXLAN(**request.json)
    if g.driver.execute('tunnels:vxlan', 'read', request_data=vxlan.id):
        raise exc.ObjectExists()
    response = g.driver.execute('tunnels:vxlan', 'create', request_data=vxlan)
    if not isinstance(response, an_vxlan.VXLAN):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response, 201)


@blueprint.route('/vxlan/<vni>', methods=['DELETE'])
def delete_tunnel(device_id, vni):
    if not g.driver.execute('tunnels:vxlan', 'read', request_data=vni):
        raise exc.ObjectNotFound()
    response = g.driver.execute('tunnels:vxlan', 'delete', request_data=vni)
    if response is not None:
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(None, 204)
