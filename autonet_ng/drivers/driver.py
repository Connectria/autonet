from typing import Callable, Union

from autonet_ng.core.device import AutonetDevice
from autonet_ng.core.exceptions import DriverOperationUnsupported

DRIVER_CAPABILITIES_ACTIONS = [
    'create',
    'read',
    'update',
    'delete'
]
DRIVER_CAPABILITIES_TYPES = [
    'interface:route',
    'interface:bridge',
    'interface',
    'tunnels:vxlan'
    'tunnels:gre'
    'tunnels:geneve'
    'tunnels:ipip'
    'tunnels:mpls'
    'vrf'
    'bridge'
    'bridge:domain'
    'protocols:static'
    'protocols:bgp'
    'protocols:ospf'
    'runtime:routing'
    'runtime:bgp'
]


class DeviceDriver(object):
    """
    Base class that defines the interface for a device driver.

    The class `__init__()` method will be passed an `AutonetDevice` object to
    be used to establish communication with the device.  Any specialized
    information that the driver may need should be passed via the metadata
    dictionary on the `AutonetDevice`.

    The DeviceDriver class implements the `execute()` method for asking
    the driver to execute pre-defined task on the device and the `capabilities`
    property for enumerating what tasks the driver can support.  `capabilities`
    is defined as a class level attribute and should remain as such in child
    classes since its enumeration may be used to build documentation.

    The `DeviceDriver` class creates a reference implementation where each request
    type is mapped to a method on the class itself.  This allows for an easy starting
    point for inheriting from the base class and moving straight to implementing
    device specific functionality without having to work through any boilerplate
    requirements from Autonet. However, these things are optional and the driver
    author may override them since implementation details of the driver are
    ultimately up to the driver's author.

    Device drivers need not support any specific subset of capabilities, though
    at a minimum it would be preferable to support basic interface and VLAN
    configuration actions.  If a driver does not support a given capability then
    it should raise a `DriverOperationUnsupported` exception.

    It's important to note that `capabilities` defines what the driver is capable
    of doing and not necessarily the capabilities of the device itself.  For example
    a driver for Juniper Junos can be used to drive a QFX series or EX series switch.
    The driver can implement the `vxlan*` capability set for QFX switches, but would
    not be able to use it with EX series switches.  In this case the driver would
    report that it's capable of performing `vxlan*` actions, but when asked to operate
    on an EX series switch it would raise a `DeviceOperationUnsupported` exception.
    """

    _enumerated_capabilities = {}

    def __init__(self, device: AutonetDevice):
        """
        :param device: An AutonetDevice object to act upon.
        """
        self.device = device

    @property
    def capabilities(self):
        def _enumerate_capabilities():
            capabilities = {}
            for capability in DRIVER_CAPABILITIES_TYPES:
                capabilities[capability] = {}
                for action in DRIVER_CAPABILITIES_ACTIONS:
                    f_name = self._generate_func_name(capability, action)
                    capabilities[capability][action] = hasattr(self, f_name)
            return capabilities

        if not self._enumerated_capabilities:
            self._enumerated_capabilities = _enumerate_capabilities()
        return self._enumerated_capabilities

    @staticmethod
    def _generate_func_name(capability, action) -> str:
        """
        Determine the function name to call for a given capability and action.
        :param capability: The capability to be utilized
        :param action: The requested action.
        :return:
        """
        # will yield name formatted as `_type_subtype_action'
        return '_'.join(('', capability.replace(':', '_'), action))

    def _get_cap_function(self, capability, action) -> Union[Callable]:
        """
        Returns the function appropriate to the capability and action requested.
        If the function doesn't exist (or the capability isn't mapped) then it will
        return a factory that raises the appropriate exception.
        :param capability: The capability to be utilized
        :param action: The requested action.
        :return:
        """
        def unsupported(*args, **kwargs):
            raise DriverOperationUnsupported(self.__class__.__name__, f_name)

        f_name = self._generate_func_name(capability, action)
        if hasattr(self, f_name) and self.capabilities[capability][action]:
            return getattr(self, f_name)
        else:
            return unsupported

    def execute(self, capability: str, action: str, request_data: object = None, **kwargs):
        """
        Execute should be called on the driver from a given endpoint.  The capability and
        action should correspond to the endpoint called and be used by the execute method
        to determine the action or actions the driver must take.  Optionally (and likely)
        request data will be passed in as well which will be a pre-defined dataclass
        appropriate to the endpoint called.

        For example, if a user issues an HTTP POST to `/device/{id}/interfaces` then
        execute will be called with `capability=interface` and `action=create`.  The
        request_data object will be a `Interface` object with appropriate details
        filled out.  The function would then need to return an appropriate object
        and response or raise (or bubble up) and appropriate exception.
        :param capability: The capability to be utilized
        :param action: The request action
        :param request_data: The request data
        :return:
        """
        func = self._get_cap_function(capability, action)
        return func(request_data=request_data, **kwargs)
