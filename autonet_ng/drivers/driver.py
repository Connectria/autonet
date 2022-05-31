from typing import Callable, List, Union

from autonet_ng.core.device import AutonetDevice
from autonet_ng.core.exceptions import DriverOperationUnsupported
from autonet_ng.core.objects import interfaces as an_if
from autonet_ng.core.objects import lag as an_lag
from autonet_ng.core.objects import vlan as an_vlan
from autonet_ng.core.objects import vrf as an_vrf
from autonet_ng.core.objects import vxlan as an_vxlan

DRIVER_CAPABILITIES_ACTIONS = [
    'create',
    'read',
    'update',
    'delete'
]
DRIVER_CAPABILITIES_TYPES = [
    'interface:route',
    'interface:bridge',
    'interface:lag',
    'interface',
    'tunnels:vxlan',
    'tunnels:gre',
    'tunnels:geneve',
    'tunnels:ipip',
    'tunnels:mpls',
    'vrf',
    'bridge:vlan',
    'bridge:domain',
    'protocols:static',
    'protocols:bgp',
    'protocols:ospf',
    'runtime:routing',
    'runtime:bgp',
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

    def _interface_read(self, request_data: str = None) -> [an_if.Interface]:
        """
        Interface read function may be called with `request_data` set to the
        interface name provided by the user.  If so, then only that interface
        should be returned.  Otherwise, the driver should return all
        interfaces.
        :param request_data: The name of the interface, if requested.
        :return:
        """

    def _interface_create(self, request_data: an_if.Interface) -> an_if.Interface:
        """
        Interface create is to be called with an `Interface` object.  Autonet will
        perform some basic input validation, but the driver may need to do
        additional validations to ensure that the request can be completed by the
        device.  The driver should return a completed `Interface` object that
        represents the interface as created once any defaults or other modifications
        have been made by the driver.
        :param request_data: An `Interface` object.
        :return:
        """

    def _interface_update(self, request_data: an_if.Interface, update) -> an_if.Interface:
        """
        Interface update may be called by either a PUT or PATCH request.  When called with
        patch then `update` will be set to `True`.  PUT should be interpreted such that any
        attributes not present in the request is defaulted, such as in a create operation.
        PATCH operations, where `update` is `True`, should ignore any unset items and only
        update attributes that are provided.

        The driver should return a complete `Interface` object that represents the updated
        configuration of the interface.
        :param request_data: An `Interface` object.
        :param update: True if called with HTTP PATCH. False if called with HTTP PUT.
        :return:
        """

    def _interface_delete(self, request_data: str):
        """
        Interface delete is called with only an interface name provided as `request_data`.
        The driver should determine if the interface is virtual, or physical and then take
        action to remove or reset to default respectively.  Return should be `None` on
        success or an exception should be raised.
        :param request_data: Interface name, as a string.
        :return:
        """

    def _tunnels_vxlan_read(self, request_data: str = None) -> Union[List[an_vxlan.VXLAN], an_vxlan.VXLAN]:
        """
        VXLAN read should return a list of all VXLAN objects present on the device
        unless called with `request_data` set, in which case only the requested
        VXLAN should be returned. Autonet will check for None or [] and raise an
        appropriate exception if the requested VXLAN is not defined.
        :param request_data: The VXLAN VNID, as a string.  Used to filter results
                             for a specific VXLAN object.
        :return:
        """

    def _tunnels_vxlan_create(self, request_data: an_vxlan.VXLAN) -> an_vxlan.VXLAN:
        """
        VXLAN tunnel create method is called with `request_data` set to a fully
        formed `VXLAN` object.  The driver should process the object accordingly
        and return a `VXLAN` object that is complete with any default values that
        may have been applied during the resultant configuration process.
        :param request_data: A `VXLAN` object.
        :return:
        """

    def _tunnels_vxlan_update(self, request_data: an_vxlan.VXLAN, update: bool) -> an_vxlan.VXLAN:
        """
        VXLAN tunnel update will be passed two arguments: `request_data` which
        is a possibly partially complete `VXLAN` object, and update, which is
        boolean flag to signal if request was called with PUT or PATCH as the
        HTTP verb. Rreplace operations should set to their default values or
        removed, as appropriate. any attributes passed as `None` Update
        operations should ignore attributes set to `None`.
        :param request_data: A `VXLAN` object.
        :param update: True if called with HTTP PATCH. False if called with HTTP PUT.
        :return:
        """

    def _tunnels_vxlan_delete(self, request_data: str):
        """
        VXLAN tunnel delete receives the VNID as a string via `request_data`.  The
        driver should take care of any tunnel configuration removal as well as
        removal of any related BGP EVPN configuration.  VRF configuration should
        be left in-tact, except as relates to EVPN-VXLAN.
        :param request_data: The VXLAN VNID, as a string.
        :return:
        """

    def _vrf_read(self, request_data: str = None) -> Union[List[an_vrf.VRF], an_vrf.VRF]:
        """
        VRF read may be passed a specific VRF name via `request_data`.  If
        `request_data` is set, then only the requested VRF should be returned.
        Otherwise, a list of all mutable VRFs should be returned.  Immutable VRFs,
        such as the default VRF, or a management-only VRF, should be omitted.
        :param request_data: The VRF name, as a string.
        :return:
        """

    def _vrf_create(self, request_data: an_vrf.VRF) -> an_vrf.VRF:
        """
        VRF create will receive a `VRF` object as it's `request_data`.  When
        the driver has completed configuration of the VRF it should return
        a `VRF` object representative of the created VRF including any
        default values that may have been set during the request process.
        :param request_data: A `VRF` object.
        :return:
        """

    def _vrf_update(self, request_data: an_vrf.VRF, update: bool) -> an_vrf.VRF:
        """
        VRF update receives a `VRF` object as it's `request_data` as well as
        having `update` set as a flag to indicate if the request is a replace
        or update operation.  Replace operations should set any attributes set
        to `None` to their defaults or remove the configuration entirely, as
        appropriate.  Update operations should ignore attributes set to `None`.

        When the configuration is complete the driver should return a `VRF`
        object that represents the resultant configuration state for the VRF.
        :param request_data: A `VRF` object.
        :param update: True if called with HTTP PATCH. False if called with HTTP PUT.
        :return:
        """

    def _vrf_delete(self, request_data: str) -> None:
        """
        VRF delete will receive the name of the VRF to be deleted as a
        string via `request_data`.  A successful delete operation should
        return `None`
        :param request_data: The VRF name, as a string.
        :return:
        """

    def _bridge_vlan_read(self, request_data: Union[str, int]) -> Union[List[an_vlan.VLAN], an_vlan.VLAN]:
        """
        VLAN read requests may receive a VLAN ID as `request_data`.  If a VLAN ID is
        received then only the `VLAN` object for that VLAN ID should be returned.
        Otherwise, a list of all mutable VLANs should be returned.  Immutable VLANs
        such as dynamic VLANs and device reserved VLANs should not be exposed.
        :param request_data: The VLAN ID requested, or `None` for all VLANs.
        :return:
        """

    def _bridge_vlan_create(self, request_data: an_vlan.VLAN) -> an_vlan.VLAN:
        """
        VLAN create will receive a `VLAN` object as `request_data`.  The driver should
        return a `VLAN` object that represents the final configured state of the VLAN
        including any default values.
        :param request_data: A `VLAN` object.
        :return:
        """

    def _bridge_vlan_update(self, request_data: an_vlan.VLAN, update: bool) -> an_vlan.VLAN:
        """
        VLAN update receives a `VLAN` object as `request_data` as well as the `update`
        flag which indicates if the operation is a replace or update operation.  For
        replace operations any attributes set to `None` should default or remove the
        related configuration, as appropriate.  Update operations should ignore `None`
        values any only modify configuration related to attribute that have a value
        other than `None`.  The driver should return a `VLAN` object that reflects the
        final configuration state.
        :param request_data: A `VLAN` object.
        :param update: True if called with HTTP PATCH. False if called with HTTP PUT.
        :return:
        """

    def _bridge_vlan_delete(self, request_data: str) -> None:
        """
        VLAN delete receives the VLAN ID of the vlan to be removed via `request_data`.
        Removal of the VLAN is required, and removal of any related configuration is
        up to the driver implementation as required by the target device's constraints.
        The driver should return `None` on success.
        :param request_data: The VLAN ID, as a string.
        :return:
        """

    def _interface_lag_read(self, request_data: str) -> Union[List[an_lag.LAG], an_lag.LAG]:
        """
        LAG read may receive a LAG name as a string via `request_data`.  If so, then only
        the requested LAG should be returned.  Otherwise, all LAGs should be returned.
        :param request_data: The LAG name, or `None` for all LAGs.
        :return:
        """

    def _interface_lag_create(self, request_data: an_lag.LAG) -> an_lag.LAG:
        """
        LAG create will receive a `LAG` object as `request_data`.  Once
        configuration is completed the driver needs to return a `LAG` object
        that represents the final configuration state on the device including
        any generated defaults.
        :param request_data: A `LAG` object.
        :return:
        """

    def _interface_lag_update(self, request_data: an_lag.LAG, update: bool) -> an_lag.LAG:
        """
        LAG update receives a `LAG` object as `request_data` and an `update` flag which
        indicates if the request is a replace or update operation.  Replace operations
        should default or remove configuration for any attributes that are set to `None`.
        Update operations should ignore attributes that are set to `None`.
        :param request_data: A `LAG` object.
        :param update: True if called with HTTP PATCH. False if called with HTTP PUT.
        :return:
        """

    def _interface_lag_delete(self, request_data: str) -> None:
        """
        LAG delete receives the lag name as a string.  Removal of the LAG
        configuration should include resetting or defaulting the configuration
        of any member interfaces as well.  The driver should return `None` in
        the event of a successful removal.
        :param request_data: The LAG name, as as string.
        :return:
        """