from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, NoResultFound

from autonet.core.response import autonet_response
from autonet.db import Session
from autonet.db.models import Tokens, Users
from autonet.util.auth import generate_token, hash_password

blueprint = Blueprint('users', __name__)


@blueprint.route('', methods=['GET'])
def get_users():
    with Session() as s:
        users = s.query(Users).all()
        return autonet_response(users)


@blueprint.route('/<user_id>', methods=['GET'])
def get_user(user_id: str):
    with Session() as s:
        try:
            user = s.query(Users).where(Users.id == user_id).one()
            return autonet_response(user)
        except NoResultFound:
            return autonet_response(None, 404)


@blueprint.route('', methods=['POST'])
def create_user():
    with Session() as s:
        try:
            user = Users(**request.json)
            s.add(user)
            s.commit()
            return autonet_response(user, 201)
        except IntegrityError:
            status = 409

        return autonet_response(None, status)


@blueprint.route('/<user_id>', methods=['PATCH'])
def update_user(user_id: str):
    with Session() as s:
        try:
            user = s.query(Users).where(Users.id == user_id).one()
            user.update(request.json)
            s.commit()
            return autonet_response(user)
        except NoResultFound:
            return autonet_response(None, 404)


@blueprint.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id: str):
    with Session() as s:
        try:
            user = s.query(Users).where(Users.id == user_id).one()
            s.delete(user)
            s.commit()
            return autonet_response(None, 204)
        except NoResultFound:
            return autonet_response(None, 404)


@blueprint.route('/<user_id>/tokens', methods=['GET'])
def get_user_tokens(user_id: str):
    with Session() as s:
        tokens = s.query(Tokens).where(Tokens.user_id == user_id).all()
        return autonet_response(tokens, 200)


@blueprint.route('/<user_id>/tokens', methods=['POST'])
def create_user_token(user_id: str):
    generated_token = generate_token()
    with Session() as s:
        try:
            user = s.query(Users).where(Users.id == user_id).one()
        except NoResultFound:
            return autonet_response(None, 404)
        token = Tokens(token=hash_password(generated_token), description='Default Token', user_id=user.id)
        s.add(token)
        s.commit()
        return autonet_response(None, 201, {'X-API-Key': generated_token})


@blueprint.route('/<user_id>/tokens/<token_id>', methods=['DELETE'])
def delete_user_token(user_id: str, token_id: str):
    with Session() as s:
        try:
            token = s.query(Tokens).where(Tokens.id == token_id, Tokens.user_id == user_id).one()
            s.delete(token)
            s.commit()
            return autonet_response(None, 204)
        except NoResultFound:
            return autonet_response(None, 404)
