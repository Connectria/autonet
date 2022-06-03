Link Aggregation Groups
=======================

Management and configuration of link aggregation on a given device is
managed via the interface LAG endpoints.  Autonet only supports 802.1ad
LACP based LAGs and has no direct support for any other type of LAG
configuration.

The LAG object describes the member interfaces on the given device.
These members are identified by their interface names, as seen in the
outputs of :http:get:`/(device_id)/interfaces/` and as used in calls to
:http:get:`/(device_id)/interfaces/(interface_name)`.  The LAG object
also has an `evpn_esi` property that can be used to define an EVPN MH
ESI for the LAG so that it may participate in EVPN Multi-homing
configurations.

Configuration of the LAG's forwarding properties is done via the
:http:patch:`/(device_id)/interfaces/(interface_name)/` endpoint by
passing the LAG's name as the `interface_name` parameter.

.. qrefflask:: autonet.core.app:flask_app
   :blueprints: interface_lag
   :autoquickref:

.. autoflask:: autonet.core.app:flask_app
   :blueprints: interface_lag
