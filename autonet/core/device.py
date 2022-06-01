from dataclasses import dataclass, field
from typing import Optional, Union
from ipaddress import IPv4Address


@dataclass
class AutonetDeviceCredentials:
    username: str
    password: Optional[str] = field(default=None)
    private_key: Optional[str] = field(default=None)


@dataclass
class AutonetDevice:
    """
    :param device_id: Object ID for the device.
    :param address: Management address.
    :param credentials: AutonetDeviceCredentials object.
    :param device_name: Optional friendly name for the device, may be used in logs.
    :param driver: The driver used to manage the network device.
    :param metadata: Autonet specific metadata.
    """
    device_id: Union[str, int]
    address: Union[str, IPv4Address]
    credentials: AutonetDeviceCredentials
    driver: str
    enabled: Optional[bool] = field(default=True)
    device_name: Optional[str] = field(default=None)
    metadata: Optional[dict] = field(default_factory=dict)

    def __repr__(self):
        return f"{self.device_name}({self.driver}): {self.address}"
