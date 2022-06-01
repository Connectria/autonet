import pytest

from autonet.core.device import AutonetDevice, AutonetDeviceCredentials


@pytest.mark.parametrize('test_device_id, expected', [
    ('test_device1', AutonetDevice(
        device_id='test_device1',
        address='198.18.0.1',
        credentials=AutonetDeviceCredentials(
            username='user', password='password'
        ),
        enabled=True,
        device_name=None,
        driver='dummy',
        metadata={})
     ),
    ('test_device2', None)
])
def test_get_device(test_device_id, expected, test_device_config):
    from autonet.drivers.backend.deviceconf import DeviceConf

    deviceconf = DeviceConf()
    device = deviceconf.get_device(test_device_id)
    assert device == expected
