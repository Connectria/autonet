def test_404_returns_empty_dict(netbox, netbox_404_mock):
    assert netbox._exec_request('/dcim/devices/5555') == {}


def test_get_session_key(netbox, netbox_get_session_key_mock):
    assert netbox._get_session_key() == 'test_session_key'


def test_session_key_attr(netbox, netbox_get_session_key_mock):
    assert netbox._session_key == 'test_session_key'


def test_get_device_from_netbox(netbox, netbox_device_mock):
    device_id = 55
    device = netbox._get_device_from_netbox(device_id)
    assert device['id'] == device_id


def test_get_secret_single(netbox, netbox_single_secret_mock):
    secret = netbox._get_secret(device_id=1)
    assert secret['plaintext'] == 'secret_data'


def test_get_secret_multi(netbox, netbox_multi_secret_mock):
    secret = netbox._get_secret(device_id=1)
    assert secret['plaintext'] == 'secret_data'
    assert secret['id'] == 22


def test_get_device_credentials(netbox, netbox_single_secret_mock):
    from core.device import AutonetDeviceCredentials
    creds = netbox.get_device_credentials(15)
    assert isinstance(creds, AutonetDeviceCredentials)
    assert creds.username == 'name_1'
    assert creds.password == 'secret_data'


def test_get_device(netbox, netbox_device_and_credentials_mock):
    from core.device import AutonetDevice, AutonetDeviceCredentials
    from ipaddress import IPv4Address
    device = netbox.get_device(25)
    assert isinstance(device, AutonetDevice)
    assert isinstance(device.address, IPv4Address)
    assert str(device.address) == '127.0.0.1'
    assert isinstance(device.credentials, AutonetDeviceCredentials)
    assert device.device_id == 25
    assert device.device_name == 'Dummy Device 25'
    assert device.driver == 'dummy'
    assert device.enabled
    assert isinstance(device.metadata, dict)
    assert device.metadata['os'] == 'dummy'
    assert device.metadata['state'] == 'enabled'
