Web API User Guide
==================

Using Autonet
-------------

Authentication
++++++++++++++

Autonet utilizes user names and API tokens to perform it's authentication.
All endpoints have authentication enforced.  In order to authenticate a
request the :http:header:`X-API-Key` header must be set to the username
and token joined with a :code:`:`.  For example, the default user `admin` may
have a token assigned `436c46117abb410991092f42fa679ce3`.  To authenticate
with that token the request would need to have the :http:header:`X-API-Key`
set to :code:`admin:436c46117abb410991092f42fa679ce3`.

Basic Use Patterns
++++++++++++++++++

Autonet manages device configuration by abstracting that configuration to
a standardized set of JSON objects.  The object hierarchy and interaction
are (as much as possible) setup in the manner of a RESTful web service.
Read actions are performed using :http:method:`get`.  Create actions are
performed using :http:method:`post`.  Delete actions are done using
:http:method:`delete` on the object's resource URI.

Updating Objects
++++++++++++++++

Updates can be done with :http:method:`put` to perform a replacement
operation, and :http:method:`patch` to perform an update operation.  When
using :http:method:`put`, if the object does not exist, it may be created.
Also, any object attributes that are set to `null` will be defaulted or
unset, as appropriate.  When using :http:method:`patch` the object must
exists or an :http:statuscode:`404` will be returned.  Additionally, any
object attributes that are set to `null` will be ignored for the sake
of the update as though the user did not wish for them to be modified.

Object create and update should always return the configuration object in it's
finalized form on the device.  This means that if Autonet or the device
driver has applied any sort of modification to the original request,
as may be required to make an otherwise valid request work, those
modifications will be reflected in the returned object representation.

Endpoints
---------

.. toctree::
    :maxdepth: 2

    users.rst
    bridge_vlan.rst
    interface.rst
    interface_lag.rst
    vrf.rst
    vxlan.rst
