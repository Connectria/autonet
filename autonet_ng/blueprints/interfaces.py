from flask import Blueprint, g, request

from autonet_ng.core import exceptions as exc
from autonet_ng.core.objects import interfaces as an_if
from autonet_ng.core.response import autonet_response


blueprint = Blueprint('interfaces', __name__)


@blueprint.route('', methods=['GET'])
def get_interfaces(device_id):
    def verify(driver_response):
        if not isinstance(driver_response, list):
            return False
        for item in driver_response:
            if not isinstance(item, an_if.Interface):
                return False
        return True

    response = g.driver.execute('interface', 'read')
    if verify(response):
        return autonet_response(response)
    else:
        raise exc.DriverResponseInvalid(g.driver)


@blueprint.route('/<interface_name>', methods=['GET'])
def get_interface(device_id, interface_name):
    response = g.driver.execute('interface', 'read', request_data=interface_name)
    if isinstance(response, an_if.Interface):
        return autonet_response(response)
    else:
        raise exc.DriverResponseInvalid(g.driver)


@blueprint.route('/', methods=['POST'])
def create_interface(device_id):
    # Depending on the interface mode, the attributes value
    # may be one of 2 classes, or None.
    request_data = request.json
    if request_data['mode'] == 'routed':
        request_data['attributes'] = an_if.InterfaceRouteAttributes(**request.json['attributes'])
    elif request_data['mode'] == 'bridged':
        request_data['attributes'] = an_if.InterfaceBridgeAttributes(**request.json['attributes'])
    else:
        # Maybe some got sent, but we'll silently ignore them.
        request_data['attributes'] = None

    request_data = an_if.Interface(**request_data)

    response = g.driver.execute('interface', 'create', request_data=request_data)
    if isinstance(response, an_if.Interface):
        return autonet_response(response)
    else:
        raise exc.DriverResponseInvalid(g.driver)
