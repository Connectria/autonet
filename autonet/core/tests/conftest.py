import ipaddress
import pytest

from autonet.core.device import AutonetDevice, AutonetDeviceCredentials


@pytest.fixture
def setup_request(flask_app):
    from autonet.core.app import setup_request
    return setup_request


@pytest.fixture
def test_response_payload():
    return {
        "key1": "value1",
        "key2": "value2",
        "list1": [
            "item1",
            "item2"
        ]
    }


@pytest.fixture
def autonet_device(request):
    device_id, credentials, driver = request.param
    return generate_autonet_device(device_id, credentials, driver)


def generate_autonet_device(device_id, credentials: bool, driver: bool):
    return AutonetDevice(
        device_id=device_id,
        address=ipaddress.IPv4Address('127.0.0.1'),
        device_name='Mock Device',
        enabled=True,
        driver='dummy' if driver else None,
        credentials=AutonetDeviceCredentials(
            username='dummy_driver',
            password='dummy_driver'
        ) if credentials else None,
        metadata={}
    ) if device_id else None


class MockBackend:
    def __init__(self, mocked_device):
        self._mocked_device = mocked_device

    def get_device(self, device_id):
        return self._mocked_device
