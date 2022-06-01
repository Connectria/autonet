YAML Driver
===========

The YAML driver will read a device inventory from a yaml (or json)
file.  This driver allows for a self contained implementation that does
not rely on an external data source.


Configuration
-------------

The YAML driver has only one option which is the filepath to the YAML file itself.
If not specified it will default to `devices.yaml`.

**[backend_yamlfile]**

=========== =====================================
Option      Description
=========== =====================================
path        The path to the YAML inventory file.
=========== =====================================
