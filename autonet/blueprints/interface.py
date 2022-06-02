from flask import Blueprint, g, request
from typing import Union

from autonet.core import exceptions as exc
from autonet.core.objects import interfaces as an_if
from autonet.core.response import autonet_response

blueprint = Blueprint('interfaces', __name__)


def _verify_name_match(request_if_name: str, uri_if_name: str) -> bool:
    """
    Verify that the name, if provided, in the request payload matches
    the name as presented in the URI.  Returns False if the
    request is not well-formed
    :param request_if_name: The name from the request payload.
    :param uri_if_name: The interface name from the URI.
    :return:
    """
    if request_if_name and request_if_name != uri_if_name:
        return False
    return True


def _required_config_data_missing(request_data: dict, update: bool = False) -> Union[str, bool]:
    """
    Verify that the minimum data required for a POST or PUT operation
    is present.  Returns the missing field name, or False if all fields
    are present.
    :param request_data: The raw reqeust data sent to the endpoint.
    :param update: Set True for PATCH operation, which has less stringent checking.
    :return:
    """
    # Verify minimum data is sent with request
    fields = ['name'] if update else ['name', 'attributes', 'mode']
    for field in fields:
        if request_data.get(field, None) is None:
            return field

    return False


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
    """
    .. :quickref: Interface; Get a list of interfaces.

    A list interfaces on the device and their current configuration state
    and attributes will be returned.  Specialized system interfaces, such
    as management interfaces or tunnel termination interfaces, will not
    be returned.

    **Response data**

    .. code-block:: json

        [
            {
                "bool: admin_enabled": "Indicates the admin state of the interface.",
                "object: attributes": {},
                "bool: child": "Indicates if this is a child interface.",
                "str: description": "The description of the interface from the device configuration.",
                "str: duplex": "The current duplex state of the interface.",
                "str: mode": "The current interface configuration mode.",
                "int: mtu": "The current interface MTU in bytes.",
                "str: name": "The interface name or identifier.",
                "str: parent": "The name of the parent interface if this interface is a child interface.",
                "str: physical_address": "The interface's MAC address.",
                "int: speed": "The interface speed in Megabits/sec.",
                "bool: virtual": "Indicates if the interface is physical or virtual."
            }   
        ]

    **Response codes**

    * :http:statuscode:`200`
    """
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
    """
    .. :quickref: Interface; Get an interface.
    
    The named interfaces on the device and its current configuration state
    and attributes will be returned.
    
    **Response data**
    
    .. code-block:: json
        
        {
            "bool: admin_enabled": "Indicates the admin state of the interface.",
            "object: attributes": {},
            "bool: child": "Indicates if this is a child interface.",
            "str: description": "The description of the interface from the device configuration.",
            "str: duplex": "The current duplex state of the interface.",
            "str: mode": "The current interface configuration mode.",
            "int: mtu": "The current interface MTU in bytes.",
            "str: name": "The interface name or identifier.",
            "str: parent": "The name of the parent interface if this interface is a child interface.",
            "str: physical_address": "The interface's MAC address.",
            "int: speed": "The interface speed in Megabits/sec.",
            "bool: virtual": "Indicates if the interface is physical or virtual."
        }   

    **Response codes**
    
    * :http:statuscode:`200`
    * :http:statuscode:`404`
    """
    response = g.driver.execute('interface', 'read', request_data=interface_name)
    if not response:
        raise exc.ObjectNotFound()
    if not isinstance(response, an_if.Interface):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/', methods=['POST'])
def create_interface(device_id):
    """
    .. :quickref: Interface; Create an interface.
    
    Create an interface on the device.  This allows for the creation of
    virtual interfaces or sub-interfaces of existing physical interfaces.
    
    **Request data**
    
    .. code-block:: json
    
        {
            "bool: admin_enabled": "Indicates the admin state of the interface.",
            "object: attributes": {},
            "str: description": "The description of the interface from the device configuration.",
            "str: duplex": "The current duplex state of the interface.",
            "str: mode": "The current interface configuration mode.",
            "int: mtu": "The current interface MTU in bytes.",
            "str: name": "The interface name or identifier.",
            "str: parent": "The name of the parent interface if this interface is a child interface.",
            "str: physical_address": "The interface's MAC address.",
            "int: speed": "The interface speed in Megabits/sec.",
            "bool: virtual": "Indicates if the interface is physical or virtual."
        }   
    
    **Response data**
    
    .. code-block:: json
    
        {
            "bool: admin_enabled": "Indicates the admin state of the interface.",
            "object: attributes": {},
            "bool: child": "Indicates if this is a child interface.",
            "str: description": "The description of the interface from the device configuration.",
            "str: duplex": "The current duplex state of the interface.",
            "str: mode": "The current interface configuration mode.",
            "int: mtu": "The current interface MTU in bytes.",
            "str: name": "The interface name or identifier.",
            "str: parent": "The name of the parent interface if this interface is a child interface.",
            "str: physical_address": "The interface's MAC address.",
            "int: speed": "The interface speed in Megabits/sec.",
            "bool: virtual": "Indicates if the interface is physical or virtual."
        }   
    
    **Response codes**
    
    * :http:statuscode:`201`
    * :http:statuscode:`409`
    """
    request_data = request.json
    if g.driver.execute('interface', 'read', request_data=request_data['name']):
        raise exc.ObjectExists()

    # Verify minimum data is sent with request
    missing = _required_config_data_missing(request_data)
    if missing:
        raise exc.RequestValueMissing(missing)

    # Now we set default values as appropriate.
    request_data = _prepare_defaults(request_data)

    an_if_object = _build_interface_from_request_data(request_data)
    response = g.driver.execute('interface', 'create', request_data=an_if_object)
    if not isinstance(response, an_if.Interface):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response, 201)


@blueprint.route('/<interface_name>', methods=['PUT', 'PATCH'])
def update_interface(device_id, interface_name):
    """
    .. :quickref: Interface; Update an interface.
    
    Create an interface on the device.  Any interface may be updated
    in this manner.  Interfaces cannot be renamed in this manner, nor
    can they be assigned a new parent.
    
    **Request data**
    
    .. code-block:: json
    
        {
            "bool: admin_enabled": "Indicates the admin state of the interface.",
            "object: attributes": {},
            "str: description": "The description of the interface from the device configuration.",
            "str: duplex": "The current duplex state of the interface.",
            "str: mode": "The current interface configuration mode.",
            "int: mtu": "The current interface MTU in bytes.",
            "str: physical_address": "The interface's MAC address.",
            "int: speed": "The interface speed in Megabits/sec.",
            "bool: virtual": "Indicates if the interface is physical or virtual."
        }   
    
    **Response data**
    
    .. code-block:: json
    
        {
            "bool: admin_enabled": "Indicates the admin state of the interface.",
            "object: attributes": {},
            "bool: child": "Indicates if this is a child interface.",
            "str: description": "The description of the interface from the device configuration.",
            "str: duplex": "The current duplex state of the interface.",
            "str: mode": "The current interface configuration mode.",
            "int: mtu": "The current interface MTU in bytes.",
            "str: name": "The interface name or identifier.",
            "str: parent": "The name of the parent interface if this interface is a child interface.",
            "str: physical_address": "The interface's MAC address.",
            "int: speed": "The interface speed in Megabits/sec.",
            "bool: virtual": "Indicates if the interface is physical or virtual."
        }   
    
    **Response codes**
    
    * :http:statuscode:`200`
    * :http:statuscode:`404`
    """
    request_if_name = request.json.get('name', None)
    if not _verify_name_match(request_if_name, interface_name):
        raise exc.RequestValueError('name', request_if_name, [interface_name])
    return _update_interface(device_id, interface_name)


@blueprint.route('/', methods=['PUT', 'PATCH'])
def _update_interface(device_id, interface_name: str = None):
    request_data = request.json
    if interface_name and not request_data.get('name', None):
        request_data['name'] = interface_name

    # Verify minimum data is sent with request
    update = request.method == 'PATCH'
    missing = _required_config_data_missing(request_data, update)
    if missing:
        raise exc.RequestValueMissing(missing)

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
    """
    .. :quickref: Interface; Delete an interface.

    Delete an interface on the device.  This can be called against
    a physical interface or a virtual interface.  In the case of a
    virtual interface, it will be destroyed.  In the case of a
    physical interface, it will be set back to the default configuration
    as determined by the device's driver.  It should not be expected
    that references to the deleted interface in other parts of the
    configuration will be deleted as well.

    **Response codes**

    * :http:statuscode:`204`
    * :http:statuscode:`404`
    """
    if not g.driver.execute('interface', 'read', request_data=interface_name):
        raise exc.ObjectNotFound()
    response = g.driver.execute('interface', 'delete', request_data=interface_name)
    if response is not None:
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(None, 204)
