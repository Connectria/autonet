import string


def test_create_admin(db_session):
    from autonet.commands import createadmin
    token = createadmin._create_admin()
    assert len(token) == 32
    assert all(c in string.hexdigits for c in token)

