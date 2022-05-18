from flask import Blueprint, g, request, Request

from autonet_ng.core import exceptions as exc
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
