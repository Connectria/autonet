import importlib

import core.exceptions as exc

from core.backends.netbox import NetBox
from core.device import AutonetDevice
from drivers.driver import DeviceDriver

DEVICE_BACKEND = NetBox()


def marshal_device(device_id):
    """
    Fetch the device info from the backing database.
    :param device_id:
    :return:
    """
    # Future versions of autonet may allow multiple, possibly simultaneous, backends
    # for devices and credentials.  This function is the intended breakout point for that.
    nb_device = DEVICE_BACKEND.get_device(device_id)
    if not nb_device:
        raise exc.DeviceNotFound(device_id, DEVICE_BACKEND)
    if not nb_device.credentials:
        raise exc.DeviceCredentialsNotFound(device_id, DEVICE_BACKEND)
    if not nb_device.driver:
        raise exc.DeviceDriverNotFound(device_id, DEVICE_BACKEND)
    return nb_device


def marshal_device_driver(device: AutonetDevice):
    driver_module_name = 'autonet_ng.drivers.' + device.driver
    try:
        driver_module = importlib.import_module(driver_module_name)
        driver = getattr(driver_module, 'driver', None)
    except Exception:
        raise exc.DeviceDriverNotFound(driver_module_name, device.device_id)

    return driver
