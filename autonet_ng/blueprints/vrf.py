from flask import Blueprint, g, request

from autonet_ng.core.objects import vrf as an_vrf
from autonet_ng.core.response import autonet_response

blueprint = Blueprint('vrf', __name__)


@blueprint.route('/', methods=['GET'])
def get_vrfs(device_id):
    result = g.driver.execute('vrf', 'read')
    return autonet_response(result)


@blueprint.route('/<vrf_name>', methods=['GET'])
def get_vrf(device_id, vrf_name):
    result = g.driver.execute('vrf', 'read', request_data=vrf_name)
    return autonet_response(result)
