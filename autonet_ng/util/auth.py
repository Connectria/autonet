from passlib.hash import pbkdf2_sha512
from uuid import uuid4


def hash_password(password: str):
    return pbkdf2_sha512.hash(password)


def verify_password(password: str, password_hash: str):
    return pbkdf2_sha512.verify(password, password_hash)


def generate_token():
    return uuid4().hex.lower()[0:32]
