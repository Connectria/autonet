from dataclasses import dataclass, field
from ipaddress import IPv4Interface, IPv6Interface
from typing import Union

import autonet.core.objects.validators as v


@dataclass
class InterfaceAddress(object):
    family: str
    address: str
    virtual: bool
    virtual_type: Union[str, None] = field(default=None)

    def __post_init__(self):
        v.validate(self)


@dataclass
class InterfaceBridgeAttributes(object):
    dot1q_enabled: bool
    dot1q_vids: list[int]
    dot1q_pvid: int


@dataclass
class InterfaceRouteAttributes(object):
    vrf: Union[str, None]
    addresses: list[InterfaceAddress]


@dataclass
class Interface(object):
    name: str
    mode: str
    description: str
    virtual: bool
    mode: str
    attributes: Union[InterfaceBridgeAttributes, InterfaceRouteAttributes]
    admin_enabled: bool = field(default=True)
    physical_address: str = field(default='00:00:00:00:00:00')
    child: bool = field(default=False)
    parent: Union[str, None] = field(default=None)
    speed: Union[int, None] = field(default=None)
    duplex: Union[str, None] = field(default=None)
    mtu: int = field(default=1500)

    def __post_init__(self):
        v.validate(self)
