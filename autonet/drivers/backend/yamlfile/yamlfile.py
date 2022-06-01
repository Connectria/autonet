import re
import yaml

from conf_engine.options import StringOption
from typing import Union

from autonet.core.device import AutonetDevice, AutonetDeviceCredentials
from autonet.core import exceptions as exc
from autonet.drivers.backend.base import AutonetDeviceBackend
from autonet.config import config

yamlfile_opts = [
    StringOption('path', default='./devices.yaml')
]

config.register_options(yamlfile_opts, 'backend_yamlfile')


class YAMLFile(AutonetDeviceBackend):
    def __init__(self):
        inventory_file = config.backend_yamlfile.path
        with open(config.backend_yamlfile.path, 'r') as fh:
            self._devices = yaml.safe_load(fh)
        if not self._verify_inventory(self._devices):
            raise exc.AutonetException(f"Inventory file {inventory_file} "
                                       f"is not properly formatted.")

    @staticmethod
    def _verify_inventory(devices: dict) -> bool:
        """Verify that inventory loaded from YAML file is properly
        formatted.  Returns `True` or `False` accordingly.
        :param devices: Devices dictionary loaded from YAML inventory file.
        """
        required_fields = ['address', 'username', 'password', 'driver']
        for device_id, device_data in devices.items():
            match = re.search(r'^[\dA-z-]*$', device_id)
            if not match:
                return False
            for field in required_fields:
                if field not in device_data:
                    return False

        return True

    def get_device(self, device_id) -> Union[None, AutonetDevice]:
        if device_id in self._devices:
            return AutonetDevice(
                device_id=device_id,
                address=self._devices[device_id]['address'],
                credentials=self.get_device_credentials(device_id),
                enabled=True,
                device_name=self._devices[device_id].get('name', None),
                driver=self._devices[device_id]['driver'],
                metadata=self._devices[device_id].get('metadata', {})
            )

        return None

    def get_device_credentials(self, device_id) -> Union[None, AutonetDeviceCredentials]:
        if device_id in self._devices:
            return AutonetDeviceCredentials(
                username=self._devices[device_id]['username'],
                password=self._devices[device_id]['password'],
                private_key=None
            )

        return None
