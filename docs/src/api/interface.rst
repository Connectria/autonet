Interfaces
==========

The endpoints below are slightly more complicated than other device
management endpoints for objects such as VLANs and even VXLANs.
This is because an interface can have many combinations of
configuration attributes, some applicable only when others have a
certain value.

Interface Modes
---------------

Autonet views all interfaces roughly equal in the manner in which
they may be configured but differentiates them into the mode in
which the interface operates: Routing or Bridging.  Each interface
has an `attributes` object which will be formatted according to its
current mode.

Routed Interface Attributes
+++++++++++++++++++++++++++

Route mode interfaces are interface that perform IP forwarding functions.
Typically this includes SVI and Loopback interfaces, but can be any kind of
interface that the device supports IP forwarding operations with.  When in
routed mode the interface may belong to a dedicated virtual routing and
forwarding instance identified by the `vrf` field.

All IPv4 and IPv6 addresses on the interface are then contained in the
`addresses` list.  An address may be assigned directly to the interface as
is typical in most deployments.  However support exists for virtualized or
shared addresses as well.  Currently there is only support for EVPN anycast
and VRRP addresses within Autonet itself, but the support for each is also
driver and device dependent.

.. code-block:: json

    {
        "array: addresses": [
            {
                "str: address": "The address and mask of the interface, in CIDR notation.",
                "str: family": "The interface address family: 'ipv4' or 'ipv6'",
                "bool: virtual": "Indicates if the address is a virtualized in some form.",
                "virtual_type": "The virtual address type."
            }
        ],
        "vrf": "The name of the VRF to which this interface belongs."
    }

.. qrefflask:: autonet.core.app:flask_app
   :blueprints: interfaces
   :autoquickref:

.. autoflask:: autonet.core.app:flask_app
   :blueprints: interfaces


