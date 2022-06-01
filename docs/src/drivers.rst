Drivers
=======

Autonet supports two types of pluggable driver:  Backend drivers and
device drivers.  Backend drivers are used as a means of inventorying
devices to be managed by autonet.  Device drivers are used to convert
Autonet configuration objects to device native configuration and
vice-versa.

Autonet ships with three backend drivers in it's source tree.  Their
documentation is indexed in the table below.

.. toctree::
   :maxdepth: 1
   :caption: Backend Drivers:

   backends/deviceconf.rst
   backends/yamlfile.rst
   backends/netbox.rst

Device drivers are kept as their own packages and will have their own
external documentation. However, generally speaking, it's not expected
that a device driver will require any special configuration.  For more
information on developing device drivers, see
:py:mod:`autonet.drivers.device.driver`

