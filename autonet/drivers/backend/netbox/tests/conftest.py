import json
import pytest
import re
import responses

from requests import PreparedRequest


@pytest.fixture
def netbox_api_url():
    return 'https://netbox.pytest'


@pytest.fixture
def netbox():
    from autonet.drivers.backend.netbox.netbox import NetBox
    return NetBox()


def _get_dcim_device_callback(request: PreparedRequest):
    """
    Return a dummy_driver device object.
    """
    device_id = int(request.path_url.split('/')[4] or request.params.pop('id', 1))
    body = {
        'id': device_id,
        'url': f'https://{netbox_api_url}/api/dcim/devices/{device_id}/',
        'display': f'Dummy Device {device_id}',
        'name': f'Dummy Device {device_id}',
        'device_type': {
            'id': 1,
            'url': f'https://{netbox_api_url}/api/dcim/device-types/1/',
            'display': 'Dummy Switch',
            'manufacturer': {
                'id': 1,
                'url': f'https://{netbox_api_url}/api/dcim/manufacturers/1/',
                'display': 'Dummy Manufacturer',
                'name': 'Dummy',
                'slug': 'dummy_driver'
            },
            'model': 'dummy_driver',
            'slug': 'dummy_driver'
        },
        'device_role': {
            'id': 1,
            'url': f'https://{netbox_api_url}/api/dcim/device-roles/11/',
            'display': 'Dummy Role',
            'name': 'Dummy Role',
            'slug': 'dummy_driver-role'
        },
        'tenant': None,
        'platform': {
            'id': 1,
            'url': f'https://{netbox_api_url}/api/dcim/platforms/1/',
            'display': 'Dummy OS',
            'name': 'Dummy OS',
            'slug': 'dummy_driver'
        },
        'serial': '',
        'asset_tag': None,
        'site': None,
        'location': None,
        'rack': None,
        'position': None,
        'face': None,
        'parent_device': None,
        'status': {
            'value': 'active',
            'label': 'Active'
        },
        'primary_ip': {
            'id': 1,
            'url': f'https://{netbox_api_url}/api/ipam/ip-addresses/1/',
            'display': '127.0.0.1/32',
            'family': 4,
            'address': '127.0.0.1/32'
        },
        'primary_ip4': {
            'id': 1,
            'url': f'https://{netbox_api_url}/api/ipam/ip-addresses/1/',
            'display': '127.0.0.1/32',
            'family': 4,
            'address': '127.0.0.1/32'
        },
        'primary_ip6': None,
        'cluster': None,
        'virtual_chassis': None,
        'vc_position': None,
        'vc_priority': None,
        'comments': '',
        'local_context_data': None,
        'tags': [],
        'custom_fields': {
            'last_backup': None
        },
        'config_context': {
            'autonet_os': 'dummy_driver',
            'autonet_state': 'enabled'
        },
        'created': '2019-10-31',
        'last_updated': '2020-07-30T21:19:57.392546Z'
    }
    return 200, {}, json.dumps(body)


def _generate_secret(decrypted=True, secret_id: int = 1, secret_role_id: int = 1):
    """
    Generates a secret object.
    :param decrypted: Indicate if session key was passed and plaintext
                      value should be present.
    :param secret_id: Set the object ID.
    :param secret_role_id: Set the object's role ID.
    :return:
    """
    secret_plaintext = 'secret_data' if decrypted else None
    return {
        'id': int(secret_id),
        'url': f'https://{netbox_api_url}/api/plugins/netbox_secretstore/secrets/{secret_id}/',
        'display': 'admin',
        'assigned_object_type': 'dcim.device',
        'assigned_object_id': 36,
        'assigned_object': {
            'id': 36,
            'url': f'https://{netbox_api_url}/api/dcim/devices/36/',
            'display': 'lab-eos-leaf1',
            'name': 'lab-eos-leaf1'
        },
        'role': {
            'id': secret_role_id,
            'url': f'https://{netbox_api_url}/api/plugins/netbox_secretstore/secret-roles/{secret_role_id}/',
            'display': f'Secret Role {secret_role_id}',
            'name': f'Secret Role {secret_role_id}',
            'slug': f'secret-role-{secret_role_id}'
        },
        'name': f'name_{secret_id}',
        'plaintext': secret_plaintext,
        'hash': 'pbkdf2_sha256$1000$1234567890abcdefghijklmnopqrstuvwxyz!@#$%^&*()=',
        'tags': [],
        'custom_fields': {},
        'created': '2010-12-27',
        'last_updated': '2020-12-29T19:52:31.033947Z'
    }


def _get_single_secret_callback(request: PreparedRequest):
    """
    Returns a single secret in the response.
    :param request:
    :return:
    """
    decrypted = 'X-Session-Key' in request.headers
    body = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [_generate_secret(decrypted)]
    }
    return 200, {}, json.dumps(body)


def _get_multi_secret_callback(request: PreparedRequest):
    decrypted = 'X-Session-Key' in request.headers
    body = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            _generate_secret(decrypted=decrypted, secret_id=1, secret_role_id=2),
            _generate_secret(decrypted=decrypted, secret_id=22, secret_role_id=1),
            _generate_secret(decrypted=decrypted, secret_id=25, secret_role_id=3),
            _generate_secret(decrypted=decrypted, secret_id=88, secret_role_id=2),
        ]
    }
    return 200, {}, json.dumps(body)


@pytest.fixture
def netbox_device_mock(netbox_api_url):
    with responses.RequestsMock() as mock:
        mock.add_callback(
            responses.GET,
            re.compile(re.escape(netbox_api_url) + r"/api/dcim/devices/\d*"),
            content_type='application/json',
            callback=_get_dcim_device_callback
        )

        yield mock


@pytest.fixture
def netbox_device_and_credentials_mock(netbox_api_url):
    with responses.RequestsMock() as mock:
        mock.add(
            responses.POST,
            netbox_api_url + '/api/plugins/netbox_secretstore/get-session-key/',
            content_type='application/json',
            json={'session_key': 'test_session_key'}
        )
        mock.add_callback(
            responses.GET,
            netbox_api_url + '/api/plugins/netbox_secretstore/secrets',
            content_type='application/json',
            callback=_get_single_secret_callback
        )
        mock.add_callback(
            responses.GET,
            re.compile(re.escape(netbox_api_url) + r"/api/dcim/devices/\d*"),
            content_type='application/json',
            callback=_get_dcim_device_callback
        )

        yield mock


@pytest.fixture
def netbox_single_secret_mock(netbox_api_url):
    with responses.RequestsMock() as mock:
        mock.add(
            responses.POST,
            netbox_api_url + '/api/plugins/netbox_secretstore/get-session-key/',
            content_type='application/json',
            json={'session_key': 'test_session_key'}
        )
        mock.add_callback(
            responses.GET,
            netbox_api_url + '/api/plugins/netbox_secretstore/secrets',
            content_type='application/json',
            callback=_get_single_secret_callback
        )

        yield mock


@pytest.fixture
def netbox_multi_secret_mock(netbox_api_url):
    with responses.RequestsMock() as mock:
        mock.add(
            responses.POST,
            netbox_api_url + '/api/plugins/netbox_secretstore/get-session-key/',
            content_type='application/json',
            json={'session_key': 'test_session_key'}
        )
        mock.add_callback(
            responses.GET,
            netbox_api_url + '/api/plugins/netbox_secretstore/secrets',
            content_type='application/json',
            callback=_get_multi_secret_callback
        )

        yield mock


@pytest.fixture
def netbox_get_session_key_mock(netbox_api_url):
    with responses.RequestsMock() as mock:
        mock.add(
            responses.POST,
            netbox_api_url + '/api/plugins/netbox_secretstore/get-session-key/',
            content_type='application/json',
            json={'session_key': 'test_session_key'}
        )

        yield mock


@pytest.fixture
def netbox_404_mock(netbox_api_url):
    with responses.RequestsMock() as mock:
        mock.add(
            responses.GET,
            netbox_api_url + '/api/dcim/devices/5555',
            content_type='application/json',
            json={"detail": "Not found."},
            status=404
        )

        yield mock
