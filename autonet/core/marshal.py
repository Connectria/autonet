import logging

import autonet.core.exceptions as exc

from autonet.core.backends.netbox import NetBox
from autonet.core.device import AutonetDevice

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
    """
    Returns the class defined by the driver package's entry point.
    :param device:
    :return:
    """
    try:
        for driver_ep in __import__('pkg_resources').iter_entry_points(group='autonet.drivers'):
            if driver_ep.name == device.driver:
                return driver_ep.load()
    except Exception as e:
        logging.exception(e)
    raise exc.DeviceDriverNotFound(device.device_id, device.driver)

