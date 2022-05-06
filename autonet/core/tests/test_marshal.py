import pytest


@pytest.mark.parametrize('autonet_device', [(25, True, True)], indirect=True)
def test_marshal_device(monkeypatch, autonet_device):
    """
    Test that marshal_device will return the device without error.
    :param monkeypatch:
    :param autonet_device:
    :return:
    """
    from core.tests.conftest import MockBackend
    import core.marshal as cm

    monkeypatch.setattr(cm, 'DEVICE_BACKEND', MockBackend(autonet_device))
    device = cm.marshal_device(autonet_device.device_id)
    assert device is autonet_device


@pytest.mark.parametrize('autonet_device', [(False, False, False)], indirect=True)
def test_marshal_device_not_found(monkeypatch, autonet_device):
    """
    Verify DeviceNotFound exception is thrown when no device is returned.
    :param monkeypatch:
    :param autonet_device:
    :return:
    """
    from core.exceptions import DeviceNotFound as TestedException
    from core.tests.conftest import MockBackend
    import core.marshal as cm

    monkeypatch.setattr(cm, 'DEVICE_BACKEND', MockBackend(autonet_device))
    with pytest.raises(TestedException):
        cm.marshal_device(404)


@pytest.mark.parametrize('autonet_device', [(55, False, True)], indirect=True)
def test_marshal_device_credentials_not_found(monkeypatch, autonet_device):
    """
    Verify DeviceNotFound exception is thrown when no device is returned.
    :param monkeypatch:
    :param autonet_device:
    :return:
    """
    from core.exceptions import DeviceCredentialsNotFound as TestedException
    from core.tests.conftest import MockBackend
    import core.marshal as cm

    monkeypatch.setattr(cm, 'DEVICE_BACKEND', MockBackend(autonet_device))
    with pytest.raises(TestedException):
        cm.marshal_device(autonet_device.device_id)


@pytest.mark.parametrize('autonet_device', [(55, True, False)], indirect=True)
def test_marshal_device_credentials_not_found(monkeypatch, autonet_device):
    """
    Verify DeviceNotFound exception is thrown when no device is returned.
    :param monkeypatch:
    :param autonet_device:
    :return:
    """
    from core.exceptions import DeviceDriverNotFound as TestedException
    from core.tests.conftest import MockBackend
    import core.marshal as cm

    monkeypatch.setattr(cm, 'DEVICE_BACKEND', MockBackend(autonet_device))
    with pytest.raises(TestedException):
        cm.marshal_device(autonet_device.device_id)


@pytest.mark.parametrize('autonet_device', [(55, True, True)], indirect=True)
def test_marshal_device_driver(autonet_device):
    from core.marshal import marshal_device_driver
    from autonet.drivers.dummy_driver import driver
    assert marshal_device_driver(autonet_device) is driver
