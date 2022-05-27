from flask import Blueprint, g, request, Request

from autonet_ng.core import exceptions as exc
from autonet_ng.core.objects import interfaces as an_if
from autonet_ng.core.response import autonet_response

blueprint = Blueprint('interfaces', __name__)


def _verify_name_match(request_if_name: str, uri_if_name: str):
    """
    Verify that the name, if provided, in the request payload matches
    the name as presented in the URI.  Raises an exception if the
    request is not well-formed
    :param request_if_name: The name from the request payload.
    :param uri_if_name: The interface name from the URI.
    :return:
    """
    if request_if_name and request_if_name != uri_if_name:
        raise exc.RequestValueError('name', request_if_name, [uri_if_name])


def _verify_required_config_data(request_data: dict, put: bool = False):
    """
    Verify that the minimum data required for a POST or PUT operation
    is present.  Raises an exception if data set is insufficient.
    :param request_data: The raw reqeust data sent to the endpoint.
    :param put: Set True for PUT operation, which has less stringent checking.
    :return:
    """
    # Verify minimum data is sent with request
    fields = ['name', 'attributes', 'mode'] if put else ['name']
    for field in fields:
        if request_data.get(field, None) is None:
            raise exc.RequestValueMissing(field)


def _prepare_defaults(request_data: dict) -> dict:
    """
    Prepares the defaults for any undefined attributes.
    :param request_data: The raw reqeust data sent to the endpoint.
    :return:
    """
    request_data['admin_enabled'] = request_data.get('admin_enabled', True)
    request_data['mtu'] = request_data.get('mtu', 1500)
    return request_data


def _build_interface_from_request_data(request_data: dict) -> an_if.Interface:
    """
    Creates an `Interface` object to provide to the driver based on
    well-formed request data.
    :param request_data:
    :return:
    """
    # NOTE: speed, duplex, virtual, parent and child fields are
    # up to the driver to figure out based on the name.  They may be
    # provided in the request and silently ignored.

    # Depending on the interface mode, the attributes value
    # may be one of 2 classes, or None.
    if request_data['mode'] == 'routed':
        request_data['attributes']['addresses'] = [an_if.InterfaceAddress(**address)
                                                   for address
                                                   in request_data['attributes']['addresses']]
        request_data['attributes'] = an_if.InterfaceRouteAttributes(**request_data['attributes'])
    elif request_data['mode'] == 'bridged':
        request_data['attributes'] = an_if.InterfaceBridgeAttributes(**request_data['attributes'])
    else:
        # Maybe some got sent, but we'll silently ignore them.
        request_data['attributes'] = None

    return an_if.Interface(**request_data)


@blueprint.route('/', methods=['GET'])
def get_interfaces(device_id):
    def verify(driver_response):
        if not isinstance(driver_response, list):
            return False
        for item in driver_response:
            if not isinstance(item, an_if.Interface):
                return False
        return True

    response = g.driver.execute('interface', 'read')
    if not verify(response):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/<interface_name>', methods=['GET'])
def get_interface(device_id, interface_name):
    response = g.driver.execute('interface', 'read', request_data=interface_name)
    if not response:
        raise exc.ObjectNotFound()
    if not isinstance(response, an_if.Interface):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/', methods=['POST'])
def create_interface(device_id):
    request_data = request.json
    if g.driver.execute('interface', 'read', request_data=request_data['name']):
        raise exc.ObjectExists()

    # Verify minimum data is sent with request
    _verify_required_config_data(request_data)

    # Now we set default values as appropriate.
    request_data = _prepare_defaults(request_data)

    an_if_object = _build_interface_from_request_data(request_data)
    response = g.driver.execute('interface', 'create', request_data=an_if_object)
    if not isinstance(response, an_if.Interface):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response, 201)


@blueprint.route('/<interface_name>', methods=['PUT', 'PATCH'])
def update_interface(device_id, interface_name):
    _verify_name_match(flask_request.json.get('name', None), interface_name)
    return _update_interface(device_id, interface_name)


@blueprint.route('/', methods=['PUT', 'PATCH'])
def _update_interface(device_id, interface_name: str = None):
    request_data = request.json
    if interface_name and not request_data.get('name', None):
        request_data['name'] = interface_name

    # Verify minimum data is sent with request
    update = request.method == 'PATCH'
    _verify_required_config_data(request_data, not update)

    if update and not g.driver.execute('interface', 'read', request_data=request_data['name']):
        raise exc.ObjectNotFound()
    # Now we set default values as appropriate, if PUT request.
    if not update:
        request_data = _prepare_defaults(request_data)

    an_if_object = _build_interface_from_request_data(request_data)
    response = g.driver.execute('interface', 'update', request_data=an_if_object, update=update)
    if not isinstance(response, an_if.Interface):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/<interface_name>', methods=['DELETE'])
def delete_interface(device_id, interface_name):
    if not g.driver.execute('interface', 'read', request_data=interface_name):
        raise exc.ObjectNotFound()
    response = g.driver.execute('interface', 'delete', request_data=interface_name)
    if response is not None:
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(None, 204)