from flask import Blueprint, g

from autonet.core.response import autonet_response

blueprint = Blueprint('interfaces', __name__)


@blueprint.route('', methods=['GET'])
def get_interfaces(device_id):
    response = g.driver.execute('interface', 'read')
    return autonet_response(response, 200)


@blueprint.route('/<interface_name>', methods=['GET'])
def get_interface(interface_name):
    response = g.driver.execute('interface', 'read', request_data=interface_name)
    return autonet_response(response, 200)
