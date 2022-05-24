from flask import Blueprint, g, request

from autonet_ng.core import exceptions as exc
from autonet_ng.core.objects import vrf as an_vrf
from autonet_ng.core.response import autonet_response

blueprint = Blueprint('vrf', __name__)


@blueprint.route('/', methods=['GET'])
def get_vrfs(device_id):
    def verify(driver_response):
        if not isinstance(driver_response, list):
            return False
        for item in driver_response:
            if not isinstance(item, an_vrf.VRF):
                return False
        return True

    response = g.driver.execute('vrf', 'read')
    if not verify(response):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/<vrf_name>', methods=['GET'])
def get_vrf(device_id, vrf_name):
    response = g.driver.execute('vrf', 'read', request_data=vrf_name)
    if not isinstance(response, an_vrf.VRF):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/', methods=['POST'])
def create_vrf(device_id):
    vrf = an_vrf.VRF(**request.json)
    response = g.driver.execute('vrf', 'create', request_data=vrf)
    if not isinstance(response, an_vrf.VRF):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/<vrf_name>', methods=['DELETE'])
def delete_vrf(device_id, vrf_name):
    response = g.driver.execute('vrf', 'delete', request_data=vrf_name)
    if response is not None:
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(None, 204)
