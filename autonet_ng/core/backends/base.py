from typing import Union
from core.device import AutonetDevice, AutonetDeviceCredentials


class AutonetDeviceBackend:
    @staticmethod
    def get_device(self, device_id) -> Union[None, AutonetDevice]:
        return None

    @staticmethod
    def get_device_credentials(self, device_id) -> Union[None, AutonetDeviceCredentials]:
        return None
