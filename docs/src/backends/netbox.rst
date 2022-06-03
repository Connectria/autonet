NetBox Driver
=============

Autonet supports the popular DCIM NetBox via the NetBox backend driver.
Connectivity to NetBox is defined in the driver configuration.  For details
on setting NetBox up as an Autonet inventory source see the
`NetBox Setup`_ section below.  The NetBox driver will
attempt to gather credentials from the `/secrets` endpoint for older
versions of NetBox, or from the `plugins/netbox-secretstore` endpoint
for newer versions with the Netbox-Secretstore plugin installed.

NetBox Setup
------------

Autonet will attempt to piece together a complete Autonet Device
definition from various aspects of the NetBox data model.
Certain things have a direct relationship: Device ID will be
derived from the NetBox device id, and the NetBox primary IP
address for the device will be used to connect to the device
for management.

Config Context
++++++++++++++

The NetBox driver uses the device's configuration context to
define Autonet specific properties.  The configuration context
should be defined using the root key of `autonet`.  All other
properties should then be defined beneath the root key.  Autonet
only defines two properties `driver` and `enabled`, and only
requires that the former be defined.

It is recommend to create configuration contexts that apply
can be applied based on other device properties as a means of
scalable Autonet configuration.  For example, a configuration
context that defines the EOS driver can be created and then
applied to all devices with "Arista" as the platform.

Secrets
+++++++

The NetBox driver utilizes the secrets feature to gather
credentials for the device.  By default the driver will
attempt to use the first secret found with the role ID
defined in the driver configuration.  Otherwise it will
fall back to the first secret found.


Configuration
-------------

The NetBox driver the `backend_netbox` config section to define
its access to NetBox.

**[backend_yamlfile]**

=============== ===============================================================
Option          Description
=============== ===============================================================
url             The URL for NetBox, EG (https://mynetbox.local/
token           An API token with read privileges to devices and secrets.
private_key     The private_key used for decryption of secrets.
secret_role_id  The role ID to be used when doing a secret lookup.  Defaults to
                1.
tls_verify      Set to false to ignore TLS verification warnings.
=============== ===============================================================
