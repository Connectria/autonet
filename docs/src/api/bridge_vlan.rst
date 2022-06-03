Bridge VLAN
===========

Bridge VLAN endpoints allow for management of VLANs on the given device.
VLANs are identified by their numeric VLAN ID, but can be given a contextual
name in cases where the driver or device permits.

.. note::

    The VLAN object contains a field for description of a bridge domain.
    Currently Autonet does not support bridge domain management.  This is
    intended for use in a future release.

.. qrefflask:: autonet.core.app:flask_app
   :blueprints: bridge_vlan
   :autoquickref:

.. autoflask:: autonet.core.app:flask_app
   :blueprints: bridge_vlan


