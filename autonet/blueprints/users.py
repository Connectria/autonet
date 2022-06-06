from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, NoResultFound

from autonet.core.response import autonet_response
from autonet.db import Session
from autonet.db.models import Tokens, Users
from autonet.util.auth import generate_token, hash_password

blueprint = Blueprint('users', __name__)


@blueprint.route('', methods=['GET'])
def get_users():
    """
    .. :quickref: User; Get a list of users.

    A list of user objects with attached tokens will be returned.

    **Response data**

    .. code-block:: json

        [
            {
                "str: created_on": "Timestamp of the user object creation.",
                "str: description": "Description of the user.",
                "str: email": "The user's contact email address.",
                "str: id": "The user object UUID.",
                "array: tokens": [
                    {
                        "str: created_on": "Timestamp of the token object creation.",
                        "str: description": "Description of the token.",
                        "str: id": "The token object UUID",
                        "str: token": "The token's stored hash.",
                        "str: updated_on": "Timestamp for the last time the token object was updated.",
                        "str: user_id": "The UUID of the token's user."
                    }
                ],
                "str: updated_on": "Timestamp for the last time the user object was updated.",
                "str: username": "The user's name."
            }
        ]

    **Response codes**

    * :http:statuscode:`200`
    """
    with Session() as s:
        users = s.query(Users).all()
        return autonet_response(users)


@blueprint.route('/<user_id>', methods=['GET'])
def get_user(user_id: str):
    """
    .. :quickref: User; Get a user by UUID.

    A single user object with attached tokens will be returned.

    **Response data**

    .. code-block:: json

        {
            "str: created_on": "Timestamp of the user object creation.",
            "str: description": "Description of the user.",
            "str: email": "The user's contact email address.",
            "str: id": "The user object UUID.",
            "array: tokens": [
                {
                    "str: created_on": "Timestamp of the token object creation.",
                    "str: description": "Description of the token.",
                    "str: id": "The token object UUID",
                    "str: token": "The token's stored hash.",
                    "str: updated_on": "Timestamp for the last time the token object was updated.",
                    "str: user_id": "The UUID of the token's user."
                }
            ],
            "str: updated_on": "Timestamp for the last time the user object was updated.",
            "str: username": "The user's name."
        }

    **Response codes**

    * :http:statuscode:`200`
    * :http:statuscode:`404`
    """
    with Session() as s:
        try:
            user = s.query(Users).where(Users.id == user_id).one()
            return autonet_response(user)
        except NoResultFound:
            return autonet_response(None, 404)


@blueprint.route('', methods=['POST'])
def create_user():
    """
    .. :quickref: User; Create a user.

    The object representing the created user will be returned.  A user will be created
    with no tokens.  In order to assign a token to the user an additional call to
    :http:post:`/admin/users/(user_id)/tokens` will need to be made.

    **Request data**

    .. code-block:: json

        {
            "str: description": "str: Description of the user.",
            "str: email": "str: The user's contact email address.",
            "str: username": "str: The user's name."
        }

    **Response data**

    .. code-block:: json

        {
            "str: created_on": "Timestamp of the user object creation.",
            "str: description": "Description of the user.",
            "str: email": "The user's contact email address.",
            "str: id": "The user object UUID.",
            "array: tokens": [],
            "str: updated_on": "Timestamp for the last time the user object was updated.",
            "str: username": "The user's name."
        }

    **Response codes**

    * :http:statuscode:`201`
    * :http:statuscode:`409`

    """
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
    """
    .. :quickref: User; Update a user.

    The object representing the updated user will be returned.

    **Request data**

    .. code-block:: json

        {
            "str: description": "str: Description of the user.",
            "str: email": "str: The user's contact email address.",
            "str: username": "str: The user's name."
        }

    **Response data**

    .. code-block:: json

        {
            "str: created_on": "Timestamp of the user object creation.",
            "str: description": "Description of the user.",
            "str: email": "The user's contact email address.",
            "str: id": "The user object UUID.",
            "array: tokens": [],
            "str: updated_on": "Timestamp for the last time the user object was updated.",
            "str: username": "The user's name."
        }

    **Response codes**

    * :http:statuscode:`200`
    * :http:statuscode:`404`

    """
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
    """
    .. :quickref: User; Delete a user.

    Delete a user identified by their UUID.

    **Response codes**

    * :http:statuscode:`204`
    * :http:statuscode:`404`
    """
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
    """
    .. :quickref: Token; Get a list of a user's tokens.

    A list of token objects for a user identified by UUID will be returned.

    **Response data**

    .. code-block:: json

        [
            {
                "str: created_on": "Timestamp of the token object creation.",
                "str: description": "Description of the token.",
                "str: id": "The token object UUID",
                "str: token": "The token's stored hash.",
                "str: updated_on": "Timestamp for the last time the token object was updated.",
                "str: user_id": "The UUID of the token's user."
            }
        ]

    **Response codes**

    * :http:statuscode:`200`
    """
    with Session() as s:
        tokens = s.query(Tokens).where(Tokens.user_id == user_id).all()
        return autonet_response(tokens, 200)


@blueprint.route('/<user_id>/tokens', methods=['POST'])
def create_user_token(user_id: str):
    """
    .. :quickref: Token; Create a user token.

    A token will be generated for the given user.  The response data
    will include the token in its plaintext format, rather than it's
    stored hash.  This is the only time the token data will be
    available and as such it should be recorded.

    **Request data**

    .. code-block:: json

        {
            "str: description": "Description of the token.",
        }

    **Response data**

    .. code-block:: json

        {
            "str: created_on": "Timestamp of the token object creation.",
            "str: description": "Description of the token.",
            "str: id": "The token object UUID",
            "str: token": "The token's stored hash.",
            "str: updated_on": "Timestamp for the last time the token object was updated.",
            "str: user_id": "The UUID of the token's user."
        }

    .. note::

        An additional :http:header:`X-API-Key` will be set with the
        plaintext value of the newly created token.

    **Response codes**

    * :http:statuscode:`201`
    * :http:statuscode:`404`
    """
    generated_token = generate_token()
    with Session() as s:
        try:
            user = s.query(Users).where(Users.id == user_id).one()
        except NoResultFound:
            return autonet_response(None, 404)
        token = Tokens(token=hash_password(generated_token), description='Default Token', user_id=user.id)
        s.add(token)
        s.commit()
        return autonet_response(token, 201, {'X-API-Key': generated_token})


@blueprint.route('/<user_id>/tokens/<token_id>', methods=['DELETE'])
def delete_user_token(user_id: str, token_id: str):
    """
    .. :quickref: Token; Delete a user's token.

    Delete a user token identified by its UUID.

    **Response codes**

    * :http:statuscode:`204`
    * :http:statuscode:`404`
    """
    with Session() as s:
        try:
            token = s.query(Tokens).where(Tokens.id == token_id, Tokens.user_id == user_id).one()
            s.delete(token)
            s.commit()
            return autonet_response(None, 204)
        except NoResultFound:
            return autonet_response(None, 404)
