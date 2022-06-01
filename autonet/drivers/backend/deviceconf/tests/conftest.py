import pytest


@pytest.fixture
def test_device_id():
    return 'test_device1'


@pytest.fixture
def test_device_config(monkeypatch, test_device_id):
    monkeypatch.setenv('DEVICE_ID', test_device_id)
    monkeypatch.setenv('DEVICE_ADDRESS', '198.18.0.1')
    monkeypatch.setenv('DEVICE_USERNAME', 'user')
    monkeypatch.setenv('DEVICE_PASSWORD', 'password')
    monkeypatch.setenv('DEVICE_DRIVER', 'dummy')
