import pytest

from autonet.core.device import AutonetDevice, AutonetDeviceCredentials


@pytest.mark.parametrize('test_devices, expected', [
    ({'test_device1': {'address': '198.18.0.1',
                       'driver': 'dummy',
                       'password': 'test',
                       'username': 'test'},
      'test_device2': {'address': '198.18.0.2',
                       'driver': 'dummy',
                       'password': 'test',
                       'username': 'test'}}, True),
    ({'test&device1': {'address': '198.18.0.1',
                       'driver': 'dummy',
                       'password': 'test',
                       'username': 'test'}}, False),
    ({'test&device1': {'driver': 'dummy',
                       'password': 'test',
                       'username': 'test'}}, False),
    ({'test&device1': {'address': '198.18.0.1',
                       'password': 'test',
                       'username': 'test'}}, False),
    ({'test&device1': {'address': '198.18.0.1',
                       'driver': 'dummy',
                       'username': 'test'}}, False),
    ({'test&device1': {'address': '198.18.0.1',
                       'driver': 'dummy',
                       'password': 'test'}}, False),
])
def test_verify_inventory(test_devices, expected):
    from autonet.drivers.backend.yamlfile import YAMLFile
    assert YAMLFile._verify_inventory(test_devices) == expected


@pytest.mark.parametrize('test_device_id, expected', [
    ('test_device1', AutonetDeviceCredentials(
        username='test1',
        password='test1'
    )),
    ('test_device2', AutonetDeviceCredentials(
        username='test2',
        password='test2'
    )),
    ('test_device3', None)
])
def test_get_device_credentials(test_device_id, expected,
                                test_yamlfile_path, monkeypatch):
    from autonet.drivers.backend.yamlfile import YAMLFile
    monkeypatch.setenv('BACKEND_YAMLFILE_PATH', test_yamlfile_path)

    yamlfile = YAMLFile()
    credentials = yamlfile.get_device_credentials(test_device_id)
    assert credentials == expected


@pytest.mark.parametrize('test_device_id, expected', [
    ('test_device1', AutonetDevice(
        device_id='test_device1',
        address='198.18.0.1',
        credentials=AutonetDeviceCredentials(
            username='test1', password='test1'
        ),
        enabled=True,
        device_name=None,
        driver='dummy',
        metadata={})
     ),
    ('test_device2', AutonetDevice(
        device_id='test_device2',
        address='198.18.0.2',
        credentials=AutonetDeviceCredentials(
            username='test2', password='test2'
        ),
        enabled=True,
        device_name=None,
        driver='dummy',
        metadata={'evpn_anycast_mac': 'fa:12:23:34:ab:cf'})),
    ('test_device3', None)

])
def test_get_device(test_device_id, expected,
                    test_yamlfile_path, monkeypatch):
    from autonet.drivers.backend.yamlfile import YAMLFile
    monkeypatch.setenv('BACKEND_YAMLFILE_PATH', test_yamlfile_path)

    yamlfile = YAMLFile()
    device = yamlfile.get_device(test_device_id)
    assert device == expected
