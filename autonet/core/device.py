from typing import Union
from ipaddress import IPv4Address


class AutonetDeviceCredentials:
    def __init__(self, username: str = None, password: str = None, private_key: str = None):
        self.username = username
        self.password = password
        self.private_key = private_key


class AutonetDevice:
    def __init__(self, device_id: int, address: Union[str, IPv4Address], credentials: AutonetDeviceCredentials,
                 enabled: bool = True, device_name: str = None, driver: str = None, metadata: dict = None):
        """
        :param device_id: Object ID for the device.
        :param address: Management address.
        :param credentials: AutonetDeviceCredentials object.
        :param device_name: Optional friendly name for the device, may be used in logs.
        :param driver: The driver used to implement devices interaction.
        :param metadata: Autonet specific metadata.
        :return:
        """
        self.device_id = device_id
        self.address = address
        self.credentials = credentials
        self.enabled = enabled
        self.device_name = device_name or 'Unnamed Device'
        self.driver = driver
        self.metadata = metadata or {}

    def __repr__(self):
        return f"{self.device_name}({self.driver}): {self.address}"
