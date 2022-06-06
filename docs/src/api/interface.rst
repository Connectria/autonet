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

Bridged Interface Attributes
++++++++++++++++++++++++++++

Interfaces in bridge mode perform ethernet forwarding functions only and do
not participate directly in IP routing.  These interfaces are typically physical
interfaces.

The bridge mode attributes object defines how the interface handles tagged and
untagged traffic.  The `dot1q_enabled` property will determine if tagged traffic
is accepted.  If `False` then the interface will only forward traffic from the
VLAN ID specified in `dot1q_pvid`.  When `dot1q_enabled` is `True` then the
`dot1q_pvid` property will dictate which VLAN handles untagged traffic and the
`dot1q_vids` property will indicate which VLANs are permitted on the interface.
If `dot1q_vids` is emtpy, then all VLANs are permitted.

.. code-block:: json

    {
        "bool: dot1q_enabled": "Indicates interface uses 802.1Q VLAN tagging.",
        "int: dot1q_pvid": "The VLAN for untagged traffic."},
        "array: dot1q_vids": [
            "Allowed VLAN IDs as integers."
        ]
    }

.. qrefflask:: autonet.core.app:flask_app
   :blueprints: interfaces
   :autoquickref:

.. autoflask:: autonet.core.app:flask_app
   :blueprints: interfaces


