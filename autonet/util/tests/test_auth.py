import string
import re


def test_generate_token():
    from autonet.util.auth import generate_token
    token = generate_token()
    assert len(token) == 32
    assert all(c in string.hexdigits for c in token)


def test_password_hashing(test_token):
    from autonet.util.auth import hash_password
    hashed_password = hash_password(test_token)
    assert re.match(r'^\$pbkdf2-sha512\$25000\$\S{109}$', hashed_password)


def test_password_verification(test_token, test_token_hash):
    from autonet.util.auth import verify_password
    assert verify_password(test_token, test_token_hash)
    assert not verify_password('not a real token', test_token_hash)



