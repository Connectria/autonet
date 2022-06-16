import logging

from conf_engine.options import StringOption

from autonet.core import exceptions as exc
from autonet.config import config

opts = [
    StringOption('backend', default='config')
]
config.register_options(opts)


def marshal_driver(driver_ns: str, driver_name: str):
    """
    Returns the class defined by the driver's registered entrypoint.
    :return:
    """
    try:
        for driver_ep in __import__('pkg_resources').iter_entry_points(group=driver_ns):
            if driver_ep.name == driver_name:
                return driver_ep.load()
    except Exception as e:
        logging.exception(e)
        raise exc.DriverLoadError(driver_name, e)
    raise exc.DriverNotFound(driver_name)


DEVICE_BACKEND = marshal_driver('autonet.backends', config.backend)()


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
        raise exc.AutonetException(f"Device driver for device_id "
                                   f"{device_id} is not defined.")
    return nb_device
