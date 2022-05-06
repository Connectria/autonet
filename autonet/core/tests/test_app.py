def test_setup_request(flask_app, setup_request):
    """
    Verify Response class is returned.
    """
    from flask import g
    from uuid import UUID
    with flask_app.app_context():
        setup_request()
        assert isinstance(g.errors, list)
        # UUID will throw ValueError if value is not valid.
        assert UUID(g.request_id, version=4)


def test_get_device_object():
    pass


def test_append_exception_to_errors(flask_app, setup_request):
    from autonet.core.app import append_exception_to_errors
    from flask import g
    e_message = 'test exception'
    e = Exception(e_message)
    with flask_app.app_context():
        setup_request()
        r, s, h = append_exception_to_errors(e)
        assert e in g.errors
        assert e_message in r.json['errors']
