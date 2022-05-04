from flask import Blueprint, g

from core.response import autonet_response

blueprint = Blueprint('interfaces', __name__)


@blueprint.route('/', methods=['GET'])
def get_interfaces(device_id):
    response = g.driver.execute('interface', 'read')
    return autonet_response(response, 200)