from flask import Blueprint, g, request

from autonet_ng.core.objects import vxlan as an_vxlan
from autonet_ng.core.response import autonet_response

blueprint = Blueprint('vxlan', __name__)


@blueprint.route('/vxlan', methods=['GET'])
def get_tunnels(device_id):
    result = g.driver.execute('tunnels:vxlan', 'read')
    return autonet_response(result)


@blueprint.route('/vxlan/<object_id>', methods=['GET'])
def get_tunnel(device_id, object_id):
    result = g.driver.execute('tunnels:vxlan', 'read', request_data=object_id)
    return autonet_response(result)


@blueprint.route('/vxlan', methods=['POST'])
def create_tunnel(device_id):
    vxlan = an_vxlan.VXLAN(**request.json)

    result = g.driver.execute('tunnels:vxlan', 'create', request_data=vxlan)
    return autonet_response(result)


@blueprint.route('/vxlan/<object_id>', methods=['DELETE'])
def delete_tunnel(device_id, object_id):
    g.driver.execute('tunnels:vxlan', 'delete', request_data=object_id)
    return autonet_response(None, 204)
