import pytest


@pytest.fixture
def test_token():
    return 'f19da6fe9db446a3b8b501ad8cecb7d1'


@pytest.fixture
def test_token_hash():
    return '$pbkdf2-sha512$25000$jdFayzlHqPX.PyfEOKdUag$MXXGN/1fM0QNSjHFsRdXLh9CYPTwVtBBPTW8nDwttEOFQ9r2n/VHY4okEGA9DU1hlYTNjIdGxuwbU5ZkNsM2JQ'