from flask import Blueprint, g, request

from autonet.core import exceptions as exc
from autonet.core.objects import vrf as an_vrf
from autonet.core.response import autonet_response

blueprint = Blueprint('vrf', __name__)


@blueprint.route('/', methods=['GET'])
def get_vrfs(device_id):
    """
    .. :quickref: VRF; Get a list of VRFs on the device.

    A list of VRF objects will be returned.

    **Response data**

    .. code-block:: json

        [
            {
                "array: export_targets": [
                    "Route Target strings for IP-VPN export."
                ],
                "array: import_targets": [
                    "Route Target strings for IP-VPN import."
                ],
                "bool: ipv4": "IPv4 routing enabled.",
                "bool: ipv6": "IPv6 routing enabled.",
                "str: name": "The VRF name.",
                "str: route_distinguisher": "The IP-VPN route distinguisher."
            }
        ]

    **Response codes**

    * :http:statuscode:`200`
    """
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
    """
    .. :quickref: VRF; Get a VRF on the device.

    A VRF object will be returned.

    **Response data**

    .. code-block:: json

        {
            "array: export_targets": [
                "Route Target strings for IP-VPN export."
            ],
            "array: import_targets": [
                "Route Target strings for IP-VPN import."
            ],
            "bool: ipv4": "IPv4 routing enabled.",
            "bool: ipv6": "IPv6 routing enabled.",
            "str: name": "The VRF name.",
            "str: route_distinguisher": "The IP-VPN route distinguisher."
        }

    **Response codes**

    * :http:statuscode:`200`
    * :http:statuscode:`404`
    """
    response = g.driver.execute('vrf', 'read', request_data=vrf_name)
    if not response:
        raise exc.ObjectNotFound()
    if not isinstance(response, an_vrf.VRF):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response)


@blueprint.route('/', methods=['POST'])
def create_vrf(device_id):
    """
    .. :quickref: VRF; Create a VRF on the device.

    A VRF object representing the final configuration state will be returned.

    **Request data**

    .. code-block:: json

        {
            "array: export_targets": [
                "Route Target strings for IP-VPN export."
            ],
            "array: import_targets": [
                "Route Target strings for IP-VPN import."
            ],
            "bool: ipv4": "IPv4 routing enabled.",
            "bool: ipv6": "IPv6 routing enabled.",
            "str: name": "The VRF name.",
            "str: route_distinguisher": "The IP-VPN route distinguisher."
        }

    **Response data**

    .. code-block:: json

        {
            "array: export_targets": [
                "Route Target strings for IP-VPN export."
            ],
            "array: import_targets": [
                "Route Target strings for IP-VPN import."
            ],
            "bool: ipv4": "IPv4 routing enabled.",
            "bool: ipv6": "IPv6 routing enabled.",
            "str: name": "The VRF name.",
            "str: route_distinguisher": "The IP-VPN route distinguisher."
        }

    **Response codes**

    * :http:statuscode:`201`
    * :http:statuscode:`409`
    """
    vrf = an_vrf.VRF(**request.json)
    if g.driver.execute('vrf', 'read', request_data=vrf.name):
        raise exc.ObjectExists()
    response = g.driver.execute('vrf', 'create', request_data=vrf)
    if not isinstance(response, an_vrf.VRF):
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(response, 201)


@blueprint.route('/<vrf_name>', methods=['DELETE'])
def delete_vrf(device_id, vrf_name):
    """
    .. :quickref: VRF; Delete a VRF on the device.

    Deleting the VRF on the device will remove the VRF and any related
    IP-VPN configuration.  Configuration for other BGP address families
    as well as other VRF related items may not be updated based on
    driver implementation and device restrictions.

    **Response codes**

    * :http:statuscode:`200`
    * :http:statuscode:`404`
    """
    if not g.driver.execute('vrf', 'read', request_data=vrf_name):
        raise exc.ObjectNotFound()
    response = g.driver.execute('vrf', 'delete', request_data=vrf_name)
    if response is not None:
        raise exc.DriverResponseInvalid(g.driver)
    return autonet_response(None, 204)
