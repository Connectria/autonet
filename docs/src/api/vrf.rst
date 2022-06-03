Virtual Routing and Forwarding
==============================

Autonet's VRF management features includes the creation and deletion of VRFs
as well as the configuration of BGP IP-VPN for IPv4 and IPv6 so that the
VRF can be used in an IP-VPN.  BGP configuration parameters are entirely
optional if the device is not participating in an IP-VPN.

.. note::
    VRFs can have IPv4 and IPv6 forwarding enabled independently, however they
    do not allow for independent definition of route targets for each address
    family.  Defined route targets are applied equally to both address families.

.. qrefflask:: autonet.core.app:flask_app
   :blueprints: vrf
   :autoquickref:

.. autoflask:: autonet.core.app:flask_app
   :blueprints: vrf
