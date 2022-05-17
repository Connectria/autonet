import logging
import macaddress

from dataclasses import dataclass, field
from ipaddress import ip_interface
from typing import Optional, Union

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
            raise exc.RequestValueError('virtual_type', self.virtual_type,
                                        valid_values=valid_virtual_types)


@dataclass
class InterfaceBridgeAttributes(object):
    dot1q_enabled: bool
    dot1q_vids: list[int] = field(default_factory=list)
    dot1q_pvid: Optional[int] = field(default=None)

    def __post_init__(self):
        v.validate(self)

    def merge(self, update: 'InterfaceBridgeAttributes'):
        if update.dot1q_enabled is not None:
            self.dot1q_enabled = update.dot1q_enabled
        if update.dot1q_pvid is not None:
            self.dot1q_pvid = update.dot1q_pvid
        if update.dot1q_vids is not None and update.dot1q_enabled:
            self.dot1q_vids = update.dot1q_vids


@dataclass
class InterfaceRouteAttributes(object):
    addresses: list[InterfaceAddress]
    vrf: Optional[str] = field(default=None)

    def __post_init__(self):
        v.validate(self)

    def merge(self, update: 'InterfaceRouteAttributes'):
        if update.vrf is not None:
            self.vrf = update.vrf
        if update.addresses is not None:
            # For addresses, we convert to a set for the merge action so that
            # duplicates are removed. Then cast back to a list on assignment.
            self.addresses = list(set(self.addresses).union(set(update.addresses)))


@dataclass
class Interface(object):
    name: Optional[str] = field(default=None)
    mode: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    virtual: Optional[bool] = field(default=None)
    attributes: Optional[Union[InterfaceBridgeAttributes, InterfaceRouteAttributes]] = field(default=None)
    admin_enabled: Optional[bool] = field(default=None)
    physical_address: Optional[str] = field(default=None)
    child: bool = field(default=False)
    parent: Optional[str] = field(default=None)
    speed: Optional[int] = field(default=None)
    duplex: Optional[str] = field(default=None)
    mtu: Optional[int] = field(default=None)

    def __post_init__(self):
        v.validate(self)

        valid_modes = ['routed', 'bridged', 'aggregated']
        # Validate physical address and enforce format
        try:
            if self.physical_address:
                self.physical_address = str(macaddress.parse(
                    self.physical_address, macaddress.EUI48))
        except Exception:
            raise exc.RequestValueError('physical_address', self.physical_address)
        # Validate parent is set if child is true.
        if self.child and not self.parent:
            raise exc.RequestValueError('parent', self.parent)
        # Validate modes
        if self.mode and self.mode not in valid_modes:
            raise exc.RequestValueError('parent', self.mode, valid_values=valid_modes)
        # Validate attribute matches mode
        if self.mode == 'routed' and not isinstance(
                self.attributes, InterfaceRouteAttributes):
            raise exc.RequestTypeError('attributes', self.attributes, type(self.attributes))
        if self.mode == 'bridged' and not isinstance(
                self.attributes, InterfaceBridgeAttributes):
            raise exc.RequestTypeError('attributes', self.attributes, type(self.attributes))
        if self.mode == 'aggregated' and self.attributes:
            raise exc.RequestTypeError('mode', self.attributes, type(self.attributes),
                                       None)

    def merge(self, update: 'Interface'):
        """
        Performs a merge of the "updated" object into this one.  Any attributes
        on `update` that are set to `None` will be ignored.
        :param update:
        :return:
        """
        special_consideration = ['mode', 'attributes']
        for key in update.__annotations__:
            new_value = getattr(update, key, None)
            if new_value is not None and key not in special_consideration:
                setattr(self, key, new_value)
        # If the mode is the same, or likewise, the attribute object passed is
        # of the same time then perform a merge.  Otherwise, a mode change is being
        # performed, and so overwrite these attributes.
        if self.mode == update.mode or isinstance(update.attributes, type(self.attributes)):
            self.attributes.merge(update.attributes)
        else:
            self.mode = update.mode
            self.attributes = update.attributes
