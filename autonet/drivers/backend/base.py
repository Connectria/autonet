from typing import Union
from autonet.core.device import AutonetDevice, AutonetDeviceCredentials


class AutonetDeviceBackend:
    """
    Reference implementation of a backend device driver.  The driver must
    implement two methods: `get_device` and `get_device_credentials`, which must
    return an `AutonetDevice` and `AutonetDeviceCredentials` object respectively,
    None if the lookup fails.  At present `get_device_credentials` is not used
    explicitly by Autonet but there maybe be core changes in the future which
    will use the method.
    """
    @staticmethod
    def get_device(self, device_id) -> Union[None, AutonetDevice]:
        return None

    @staticmethod
    def get_device_credentials(self, device_id) -> Union[None, AutonetDeviceCredentials]:
        return None
