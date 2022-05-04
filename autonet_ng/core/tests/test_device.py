def test_autonet_device_credentials():
    from core.device import AutonetDeviceCredentials
    username = 'testuser'
    password = 'testpass'
    creds = AutonetDeviceCredentials(username=username, password=password)
    assert creds.username == username
    assert creds.password == password
    assert not creds.private_key


def test_autonet_device():
    from ipaddress import IPv4Address
    from core.device import AutonetDevice, AutonetDeviceCredentials
    username = 'testuser'
    password = 'testpass'
    device_id = 100
    address = IPv4Address('198.18.0.1')
    credentials = AutonetDeviceCredentials(username=username, password=password)
    enabled = True
    device_name = 'Test Device'
    driver = 'dummy'
    metadata = {'os': driver, 'state': 'enabled'}
    device = AutonetDevice(
        device_id=device_id,
        address=address,
        credentials=credentials,
        enabled=enabled,
        device_name=device_name,
        driver=driver,
        metadata=metadata
    )
    assert device.device_id == device_id
    assert device.address == address
    assert device.credentials == credentials
    assert device.enabled == enabled
    assert device.device_name == device_name
    assert device.driver == driver
    assert device.metadata == metadata
    assert str(device) == f"{device_name}({driver}): {address}"
