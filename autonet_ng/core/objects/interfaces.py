import logging
import macaddress

from dataclasses import dataclass, field
from ipaddress import ip_interface
from typing import Union

import autonet_ng.core.exceptions as exc
import autonet_ng.core.objects.validators as v


@dataclass
class InterfaceAddress(object):
    family: str
    address: str
    virtual: bool
    virtual_type: Union[str, None] = field(default=None)

    def __post_init__(self):
        v.validate(self)

        valid_families = ['ipv4', 'ipv6']
        valid_virtual_types = ['anycast', 'vrrp']
        # Verify family
        if self.family not in valid_families:
            raise exc.RequestValueError('family', self.family,
                                        valid_values=valid_families)
        # Verify valid IP address formatted as address/mask
        try:
            ip_interface(self.address)
        except Exception as e:
            logging.exception(e)
            raise exc.RequestValueError('address', self.address)
        # Verify virtual type, as appropriate.
        if self.virtual and self.virtual_type not in valid_virtual_types:
            raise exc.RequestValueError('family', self.virtual_type,
                                        valid_values=valid_virtual_types)


@dataclass
class InterfaceBridgeAttributes(object):
    dot1q_enabled: bool
    dot1q_vids: list[int]
    dot1q_pvid: int

    def __post_init__(self):
        v.validate(self)


@dataclass
class InterfaceRouteAttributes(object):
    vrf: Union[str, None]
    addresses: list[InterfaceAddress]

    def __post_init__(self):
        v.validate(self)


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

        valid_modes = ['routed', 'bridged']
        # Validate physical address and enforce format
        try:
            self.physical_address = str(macaddress.parse(
                self.physical_address, macaddress.EUI48))
        except Exception:
            raise exc.RequestValueError('physical_address', self.physical_address)
        # Validate parent is set if child is true.
        if self.child and not self.parent:
            raise exc.RequestValueError('parent', self.parent)
        # Validate modes
        if self.mode not in valid_modes:
            raise exc.RequestValueError('parent', self.mode, valid_values=valid_modes)
        # Validate attribute matches mode
        if self.mode == 'routed' and not isinstance(
                self.attributes, InterfaceRouteAttributes):
            raise exc.RequestTypeError('parent', self.attributes, type(self.attributes))
        if self.mode == 'bridged' and not isinstance(
                self.attributes, InterfaceBridgeAttributes):
            raise exc.RequestTypeError('parent', self.attributes, type(self.attributes))