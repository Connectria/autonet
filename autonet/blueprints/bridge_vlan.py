from flask import Blueprint, g, request

from autonet.core import exceptions as exc
from autonet.core.objects import vlan as an_vlan
from autonet.core.response import autonet_response

blueprint = Blueprint('bridge_vlan', __name__)


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
    """
    .. :quickref: VLAN; Get a list of VLANs on the device.

    A list of VLAN objects will be returned.  Only mutable VLANs are
    returned.  Any system reserved or dynamically generated VLANs
    should be omitted.

    **Response data**

    .. code-block:: json

        [
            {
                "bool: admin_enabled": "The admin state of the VLAN",
                "str: bridge_domain": "Bridge domain of the VLAN",
                "int: id": "The VLAN ID",
                "str: name": "The VLAN name."
            }
        ]

    **Response codes**

    * :http:statuscode:`200`
    """
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
    """
    .. :quickref: VLAN; Get a VLAN by its VLAN ID.

    A VLAN object will be returned.  Only mutable VLANs are
    returned.  Any system reserved or dynamically generated VLANs
    should be omitted.

    **Response data**

    .. code-block:: json

        {
            "bool: admin_enabled": "The admin state of the VLAN",
            "str: bridge_domain": "Bridge domain of the VLAN",
            "int: id": "The VLAN ID",
            "str: name": "The VLAN name."
        }


    **Response codes**

    * :http:statuscode:`200`
    * :http:statuscode:`404`
    """
    response = g.driver.execute('bridge:vlan', 'read', request_data=vlan_id)
    if not response:
        raise exc.ObjectNotFound()
    if not isinstance(response, an_vlan.VLAN):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/', methods=['POST'])
def create_vlan(device_id):
    """
    .. :quickref: VLAN; Create a VLAN.

    A VLAN object representing the committed version of the VLAN
    will be returned.  If the VLAN conflicts with a system generated
    VLAN an :http:statuscode:`409` will be returned despite the same
    VLAN not being searchable via
    :http:get:`/(device_id)/bridge/vlans/(vlan_id)`.

    **Request data**

    .. code-block:: json

        {
            "bool: admin_enabled": "The admin state of the VLAN",
            "str: bridge_domain": "Bridge domain of the VLAN",
            "int: id": "The VLAN ID",
            "str: name": "The VLAN name."
        }

    **Response data**

    .. code-block:: json

        {
            "bool: admin_enabled": "The admin state of the VLAN",
            "str: bridge_domain": "Bridge domain of the VLAN",
            "int: id": "The VLAN ID",
            "str: name": "The VLAN name."
        }


    **Response codes**

    * :http:statuscode:`201`
    * :http:statuscode:`409`
    """
    request_data = _prepare_defaults(request.json)
    vlan = an_vlan.VLAN(**request_data)
    if g.driver.execute('bridge:vlan', 'read', request_data=vlan.id):
        raise exc.ObjectExists()
    response = g.driver.execute('bridge:vlan', 'create', request_data=vlan)
    if not isinstance(response, an_vlan.VLAN):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response, 201)


@blueprint.route('/', methods=['PUT', 'PATCH'])
def _update_vlan(device_id):
    return update_vlan(device_id, None)


@blueprint.route('/<vlan_id>', methods=['PUT', 'PATCH'])
def update_vlan(device_id, vlan_id=None):
    """
    .. :quickref: VLAN; Update a VLAN.

    A VLAN objects representing the committed version of the VLAN
    will be returned.  The VLAN ID cannot be changed in this manner.

    **Request data**

    .. code-block:: json

        {
            "bool: admin_enabled": "The admin state of the VLAN",
            "str: bridge_domain": "Bridge domain of the VLAN",
            "str: name": "The VLAN name."
        }

    **Response data**

    .. code-block:: json

        {
            "bool: admin_enabled": "The admin state of the VLAN",
            "str: bridge_domain": "Bridge domain of the VLAN",
            "int: id": "The VLAN ID",
            "str: name": "The VLAN name."
        }


    **Response codes**

    * :http:statuscode:`202`
    * :http:statuscode:`404`
    """
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
    """
    .. :quickref: VLAN; Delete a VLAN.

    Deletes the VLAN identified by the VLAN ID.  Note that this
    may not remove VLAN related configuration from related objects
    such as interfaces.

    * :http:statuscode:`204`
    * :http:statuscode:`404`
    """
    if not g.driver.execute('bridge:vlan', 'read', request_data=vlan_id):
        raise exc.ObjectNotFound()
    response = g.driver.execute('bridge:vlan', 'delete', request_data=vlan_id)
    if response is not None:
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(None, 204)
