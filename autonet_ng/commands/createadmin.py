import logging

from db import select, Session
from db.models import Users, Tokens
from util.auth import generate_token, hash_password

LOG = logging.getLogger()
DEFAULT_ADMIN_NAME = 'admin'


def _create_admin() -> str:
    try:
        with Session() as s:
            user = s.scalars(select(Users).where(Users.username == DEFAULT_ADMIN_NAME)).first()
            if not user:
                user = Users(username=DEFAULT_ADMIN_NAME, email='admin@localhost', description='Default Admin')
            generated_token = generate_token()
            token = Tokens(token=hash_password(generated_token), description='Default Token')
            user.tokens.append(token)

            s.add(user)
            s.add(token)
            s.commit()
        return generated_token
    except Exception as e:
        LOG.exception(e)


def create_admin():
    token = _create_admin()
    if token:
        print(f"Created token: {token}")
    else:
        print(f"Failed to create default admin user.")
