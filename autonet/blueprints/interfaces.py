from flask import Blueprint, g

from autonet.core import exceptions as exc
from autonet.core import objects as obj
from autonet.core.response import autonet_response


blueprint = Blueprint('interfaces', __name__)


@blueprint.route('', methods=['GET'])
def get_interfaces(device_id):
    def verify(driver_response):
        if not isinstance(driver_response, list):
            return False
        for item in driver_response:
            if not isinstance(item, obj.interfaces.Interface):
                return False
        return True

    response = g.driver.execute('interface', 'read')
    if verify(response):
        return autonet_response(response)
    else:
        raise exc.DriverResponseInvalid(g.driver)


@blueprint.route('/<interface_name>', methods=['GET'])
def get_interface(device_id, interface_name):
    def verify(driver_response):
        return isinstance(driver_response, obj.interfaces.Interface)

    response = g.driver.execute('interface', 'read', request_data=interface_name)
    if verify(response):
        return autonet_response(response)
    else:
        raise exc.DriverResponseInvalid(g.driver)
