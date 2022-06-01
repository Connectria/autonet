Device Config Driver
====================

The DeviceConf driver grabs it's inventory from Autonet's configuration
directly.  As a result it can only contain a single device definition.
It's purpose is for development, demo, and testing scenarios only and
not specifically meant to be used in any sort of production capacity.

Configuration
-------------

No additional configuration is required to enable he DeviceConf driver,
as it is the default driver when no other is explicitly configured.
The table below details the configuration options required to define
the device to be managed.

**[device]**

=========== =======================================================
Option      Description
=========== =======================================================
id          The device id, to be referenced in calls to the API.
address     The ip address of the device's management interface.
username    The username to be used when connecting to the device.
password    The password to be used when connecting to the device.
driver      The device driver used to manage the device.
=========== =======================================================
