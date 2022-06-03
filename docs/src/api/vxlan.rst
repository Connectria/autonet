Virtual Extensible LAN
======================

Autonet supports the creation of VXLAN tunnels for both bridging
and integrated routing and bridging functionality.  VXLAN tunnel
configuration optionally supports BGP EVPN configuration as well.
Autonet only supports VLAN based services and does not support VLAN
aware bundle services.

When creating tunnels for use in flood and learn type networks, or
in EVPN networks that do not do IRB, or asymmetric IRB, the tunnel
should have it's `layer` property set to `2` and the `bound_object_id`
property set to the VLAN ID to which the tunnel will participate in.
For EVPN symmetric IRB support, the L3VNI tunnel will have its
`layer` property set to `3` and the `bound_object_id` set to the
name of the VRF for which the L3VNI forwards routed traffic.

.. qrefflask:: autonet.core.app:flask_app
   :blueprints: tunnels_vxlan
   :autoquickref:

.. autoflask:: autonet.core.app:flask_app
   :blueprints: tunnels_vxlan
