from dataclasses import dataclass, field
from typing import Union

import core.objects.validators as v

from core.exceptions import RequestTypeError

"""
Here we use python dataclasses to define the structure of 
given endpoints request/response data as well as implement
validation logic in the `__post_init__()` method.
"""


@dataclass
class InterfaceAddress(object):
    family: str
    address: str
    anycast: bool
    mac: str


@dataclass
class InterfaceBridgeAttributes(object):
    dot1q_enabled: bool
    qnq_enabled: bool
    dot1q_inner_tag: int
    dot1q_outer_tag: int
    dot1q_vids: list[int]
    dot1q_pvid: int


@dataclass
class InterfaceRouteAttributes(object):
    vrf: str
    addresses: list[InterfaceAddress]


@dataclass
class Interface(object):
    name: str
    mode: str
    description: str
    # attributes: Union[InterfaceBridgeAttributes, InterfaceRouteAttributes]
    type: str = field(default=None)
    admin_enabled: bool = field(default=True)
    speed: int = field(default=None)
    duplex: str = field(default=None)
    mtu: int = field(default=1500)

    def __post_init__(self):
        v.validate(self)
