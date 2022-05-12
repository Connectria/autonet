import pytest

from autonet_ng.core import exceptions as an_exc
from autonet_ng.core.response import autonet_response
from werkzeug import exceptions as wz_exc


def test_autonet_response(flask_app, setup_request):
    """
    Verify Response class is returned.
    """
    from flask import Response
    with flask_app.app_context():
        setup_request()
        r, s, h = autonet_response()
        assert isinstance(r, Response)


def test_autonet_response_jsonification(flask_app, setup_request, test_response_payload):
    """
    Verify that properly formatted json payload is returned.
    """
    with flask_app.app_context():
        setup_request()
        r, s, h = autonet_response(test_response_payload)
        assert r.json
        for expected_key in ['data', 'errors', 'status', 'request-id']:
            assert expected_key in r.json


def test_autonet_response_header_handling(flask_app, setup_request):
    """
    Verify that response correctly sets headers.
    """
    with flask_app.app_context():
        setup_request()
        headers = {'X-Test-Header': 'test_header_value'}
        r, s, h = autonet_response(None, 200, headers)
        assert h == headers


def test_autonet_response_status_handling(flask_app, setup_request):
    """
    Verify that response propagates status code correctly.
    """
    with flask_app.app_context():
        setup_request()
        status = 201
        r, s, h = autonet_response(None, 201)
        assert r.json['status'] == s == status


def test_autonet_response_status_error_handling_implicit_status(flask_app, setup_request):
    """
    Verify that response propagates status code correctly.
    """
    with flask_app.app_context():
        setup_request()
        from flask import g
        g.errors.append("test error message should trigger a 500 with no data")
        r, s, h = autonet_response()
        assert r.json['status'] == s == 500


def test_autonet_response_status_error_handling_explicit_status(flask_app, setup_request):
    """
    Verify that response propagates status code correctly.
    """
    with flask_app.app_context():
        setup_request()
        from flask import g
        g.errors.append("test error message should trigger a 404 with no data")
        r, s, h = autonet_response(None, 404)
        assert r.json['status'] == s == 404


@pytest.mark.parametrize('exception, expected_status', [
    (an_exc.ObjectExists(), 409),
    (an_exc.ObjectNotFound(), 404),
    (an_exc.DeviceOperationUnsupported('test', 'test_op', 1), 501),
    (wz_exc.MethodNotAllowed(), 405),
    (wz_exc.NotFound(), 404),
])
def test_autonet_response_status_error_handling(
        exception, expected_status, flask_app, setup_request):
    """
    Verify that response propagates status code correctly.
    """
    with flask_app.app_context():
        setup_request()
        from flask import g
        g.errors.append(exception)
        r, s, h = autonet_response(None)
        assert r.json['status'] == s == expected_status


def test_autonet_response_error_list(flask_app, setup_request):
    """
    Verify that errors are collected correctly.
    """
    with flask_app.app_context():
        setup_request()
        from flask import g
        error1, error2 = 'error1', 'error2'
        g.errors.append(error1)
        g.errors.append(error2)
        r, s, h = autonet_response()
        assert error1 in r.json['errors']
        assert error2 in r.json['errors']
