from flask import Blueprint, g, request

from autonet.core import exceptions as exc
from autonet.core.objects import vxlan as an_vxlan
from autonet.core.response import autonet_response

blueprint = Blueprint('tunnels_vxlan', __name__)


@blueprint.route('/vxlan/', methods=['GET'])
def get_tunnels(device_id):
    """
    .. :quickref: VXLAN; Get a list of VXLAN Tunnels on the device.

    A list of VXLAN Tunnel objects will be returned.

    **Response data**

    .. code-block:: json

        [
            {
                "mixed: bound_object_id": "The identifier of the bound object.",
                "array: export_targets": [
                    "Route target strings for EVPN export."
                ],
                "int: id": 70002,
                "array: import_targets": [
                    "Route target strings for EVPN import."
                ],
                "int: layer": "The operating layer for the VNI.",
                "str: route_distinguisher": "The EVPN route distinguisher.",
                "str: source_address": "The tunnel's VTEP address."
            }
        ]

    **Response codes**

    * :http:statuscode:`200`
    """
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
    """
    .. :quickref: VXLAN; Get a VXLAN Tunnel on the device.

    A VXLAN Tunnel object will be returned.

    **Response data**

    .. code-block:: json

        {
            "mixed: bound_object_id": "The identifier of the bound object.",
            "array: export_targets": [
                "Route target strings for EVPN export."
            ],
            "int: id": 70002,
            "array: import_targets": [
                "Route target strings for EVPN import."
            ],
            "int: layer": "The operating layer for the VNI.",
            "str: route_distinguisher": "The EVPN route distinguisher.",
            "str: source_address": "The tunnel's VTEP address."
        }

    **Response codes**

    * :http:statuscode:`200`
    * :http:statuscode:`404`
    """
    response = g.driver.execute('tunnels:vxlan', 'read', request_data=vni)
    if not response:
        raise exc.ObjectNotFound()
    if not isinstance(response, an_vxlan.VXLAN):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/vxlan', methods=['POST'])
def create_tunnel(device_id):
    """
    .. :quickref: VXLAN; Create a VXLAN Tunnel on the device.

    A VXLAN Tunnel object representing the finalized configuration
    will be returned.

    **Request data**

    .. code-block:: json

        {
            "mixed: bound_object_id": "The identifier of the bound object.",
            "array: export_targets": [
                "Route target strings for EVPN export."
            ],
            "int: id": 70002,
            "array: import_targets": [
                "Route target strings for EVPN import."
            ],
            "int: layer": "The operating layer for the VNI.",
            "str: route_distinguisher": "The EVPN route distinguisher.",
            "str: source_address": "The tunnel's VTEP address."
        }

    **Response data**

    .. code-block:: json

        {
            "mixed: bound_object_id": "The identifier of the bound object.",
            "array: export_targets": [
                "Route target strings for EVPN export."
            ],
            "int: id": 70002,
            "array: import_targets": [
                "Route target strings for EVPN import."
            ],
            "int: layer": "The operating layer for the VNI.",
            "str: route_distinguisher": "The EVPN route distinguisher.",
            "str: source_address": "The tunnel's VTEP address."
        }

    **Response codes**

    * :http:statuscode:`201`
    * :http:statuscode:`409`
    """
    vxlan = an_vxlan.VXLAN(**request.json)
    if g.driver.execute('tunnels:vxlan', 'read', request_data=vxlan.id):
        raise exc.ObjectExists()
    response = g.driver.execute('tunnels:vxlan', 'create', request_data=vxlan)
    if not isinstance(response, an_vxlan.VXLAN):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response, 201)


@blueprint.route('/vxlan/<vni>', methods=['DELETE'])
def delete_tunnel(device_id, vni):
    """
    .. :quickref: VXLAN; Delete a VXLAN Tunnel on the device.

    Tunnel delete actions will remove the tunnel and any related
    EVPN configuration.  It may not remove other related configuration
    at the discretion of the driver implementation or other restrictions
    of the device.

    * :http:statuscode:`204`
    * :http:statuscode:`404`
    """
    if not g.driver.execute('tunnels:vxlan', 'read', request_data=vni):
        raise exc.ObjectNotFound()
    response = g.driver.execute('tunnels:vxlan', 'delete', request_data=vni)
    if response is not None:
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(None, 204)
