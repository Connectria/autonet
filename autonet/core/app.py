import logging
import traceback

from conf_engine.options import NumberOption, StringOption
from flask import g, Flask, request
from uuid import uuid4

from autonet.core.response import autonet_response
from autonet.blueprints.bridge_vlan import blueprint as bridge_vlan_blueprint
from autonet.blueprints.interface import blueprint as interfaces_blueprint
from autonet.blueprints.interface_lag import blueprint as interface_lag_blueprint
from autonet.blueprints.tunnels_vxlan import blueprint as tunnels_vxlan_blueprint
from autonet.blueprints.vrf import blueprint as vrf_blueprint
from autonet.blueprints.users import blueprint as admin_users_blueprint
from autonet.config import config
from autonet.db import init_db
from autonet.core.exceptions import AutonetException
from autonet.core.logging import setup_logging
from autonet.core.marshal import marshal_device, marshal_driver
from autonet.db import Session
from autonet.db.models import Tokens, Users
from autonet.util.auth import verify_password

opts = [
    StringOption('bind_host', default='0.0.0.0'),
    NumberOption('port', minimum=1, maximum=65535, default=80)
]
config.register_options(opts)

flask_app = Flask(__name__)
flask_app.register_blueprint(bridge_vlan_blueprint, url_prefix='/<device_id>/bridge/vlans')
flask_app.register_blueprint(interfaces_blueprint, url_prefix='/<device_id>/interfaces')
flask_app.register_blueprint(interface_lag_blueprint, url_prefix='/<device_id>/interfaces/lags')
flask_app.register_blueprint(admin_users_blueprint, url_prefix='/admin/users')
flask_app.register_blueprint(vrf_blueprint, url_prefix='/<device_id>/vrfs')
flask_app.register_blueprint(tunnels_vxlan_blueprint, url_prefix='/<device_id>/tunnels/')

if config.debug:
    print(flask_app.url_map)
setup_logging()


def run_wsgi_app():
    logging.info("Application started via CLI.")
    init_db()
    flask_app.run(config.bind_host, config.port)


@flask_app.before_request
def setup_request():
    g.errors = []
    g.request_id = str(uuid4())
    logging.debug(f'Initial request setup for request_id {g.request_id}')


@flask_app.before_request
def setup_device_object():
    """
    Middleware will retrieve the AutonetDevice object for any request
    that has a `device_id` arg defined and place it in `g.device`

    :return:
    """
    if request.view_args and 'device_id' in request.view_args:
        g.device = marshal_device(request.view_args['device_id'])
        driver = marshal_driver('autonet.drivers', g.device.driver)
        g.driver = driver(g.device)


@flask_app.before_request
def auth_user():
    key_header = request.headers.get('X-API-Key').split(':')
    if not len(key_header) == 2:
        g.errors.append('X-API-Key format is "username:token".')
    else:
        user = key_header[0]
        token = key_header[1]
        with Session() as s:
            for t in s.query(Tokens).join(Users).where(Users.username == user).all():
                if verify_password(token, t.token):
                    return

    g.errors.append('X-API-Key is unset or invalid')
    return autonet_response(None, 401)


@flask_app.errorhandler(Exception)
def append_exception_to_errors(e):
    if config.debug:
        traceback.print_exc()
        tb = traceback.format_exc()
        for tb_line in tb.split('\n'):
            g.errors.append(tb_line)
    if isinstance(e, AutonetException) or config.debug:
        g.errors.append(e)
    else:
        g.errors.append("An internal application error has occurred.")
    return autonet_response()


if __name__ == "__main__":
    run_wsgi_app()
