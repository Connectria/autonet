import re

from conf_engine.options import StringOption
from conf_engine.exceptions import ValueNotFound
from typing import Union

from autonet.core.device import AutonetDevice, AutonetDeviceCredentials
from autonet.drivers.backend.base import AutonetDeviceBackend
from autonet.config import config

configfile_opts = [
    StringOption('id'),
    StringOption('address'),
    StringOption('username'),
    StringOption('password'),
    StringOption('driver'),
    StringOption('name', default=None)
]

config.register_options(configfile_opts, 'device')


class DeviceConf(AutonetDeviceBackend):
    @staticmethod
    def _verify_device_id_format():
        """
        Returns True if the device ID matches the one configured and device ID
        is properly formatted, otherwise returns False.
        :return:
        """
        try:
            if re.search(r'^[\dA-z-]*$', config.device.id):
                return True
        except ValueNotFound:
            pass

        return False

    def get_device(self, device_id) -> Union[None, AutonetDevice]:
        if device_id == config.device.id and self._verify_device_id_format():
            return AutonetDevice(
                device_id=device_id,
                address=config.device.address,
                credentials=self.get_device_credentials(device_id),
                enabled=True,
                device_name=config.device.name,
                driver=config.device.driver
            )

        return None

    def get_device_credentials(self, device_id) -> Union[None, AutonetDeviceCredentials]:
        if device_id == config.device.id and self._verify_device_id_format():
            return AutonetDeviceCredentials(
                username=config.device.username,
                password=config.device.password,
                private_key=None
            )

        return None
