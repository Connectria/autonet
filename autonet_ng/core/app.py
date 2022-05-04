import traceback

from flask import g, Flask, request
from uuid import uuid4


from .response import autonet_response
from blueprints.interfaces import blueprint as interfaces_blueprint
from blueprints.users import blueprint as admin_users_blueprint
from config import config
from core.exceptions import AutonetException
from core.logging import setup_logging
from core.marshal import marshal_device, marshal_device_driver
from db import Session
from db.models import Tokens, Users
from util.auth import verify_password


flask_app = Flask(__name__)
flask_app.register_blueprint(interfaces_blueprint, url_prefix='/<device_id>/interfaces')
flask_app.register_blueprint(admin_users_blueprint, url_prefix='/admin/users')
print(flask_app.url_map)
setup_logging()


@flask_app.before_request
def setup_request():
    g.errors = []
    g.request_id = str(uuid4())


@flask_app.before_request
def setup_device_object():
    """
    Middleware will retrieve the AutonetDevice object for any request
    that has a `device_id` arg defined and place it in `g.device`
    :return:
    """
    if request.view_args and 'device_id' in request.view_args:
        g.device = marshal_device(request.view_args['device_id'])
        driver = marshal_device_driver(g.device)
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
