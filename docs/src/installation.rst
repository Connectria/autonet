Installation and Setup
======================

Autonet is packages as a WSGI application and is available via PyPI.  Autonet
can be run by itself, but it's recommended to be run with a production ready
WSGI server such as `Gunicorn <https://gunicorn.org/>`_.

Pip Install
-----------

There are two ways to install the module via Pip:  Via PyPI, or install
directly from `Github <https://github.com`.

.. code-block:: shell
   :caption: Install from PyPI

    ~/# pip install autonet-api

.. code-block:: shell
   :caption: Install direct from Github.

    ~/# pip install git+https://github.com/Connectira/autonet


Once Autonet is installed it can be run directly.  If this is not
desirable then integration with a WSGI server and other
front end proxy applications is an exercise left up to the needs of
the user.

Quickstart Configuration
------------------------

To get started Autonet will require a small amount of configuration.
Autonet ships with the `conf` backend driver, as well as support for SQLite
as it's user DB.  The following example demonstrates how to get Autonet up
and going with minimal fuss to manage a single Arista switch.  Modify the
configuration according to your environment.

.. code-block:: shell
   :caption: Quickstart!

   ~# export DEVICE_ID=1
   ~# export DEVICE_ADDRESS=127.0.0.1
   ~# export DEVICE_USERNAME=username
   ~# export DEVICE_PASSWORD=password
   ~# export DEVICE_DRIVER=dummy
   ~# export DATABASE_CONNECTION=sqlite://autonet_quickstart.db
   ~# autonet-createadmin && autonet-server &
   Created token: d9725ebc9cb64f71b49a4a581bc8ed67
    * Serving Flask app 'autonet.core.app' (lazy loading)
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: off
   INFO:werkzeug: * Running on all addresses (0.0.0.0)
      WARNING: This is a development server. Do not use it in a production deployment.
    * Running on http://127.0.0.1:80
    * Running on http://192.168.0.8:80 (Press CTRL+C to quit)

   ~# curl -H 'X-API-Key: admin:d9725ebc9cb64f71b49a4a581bc8ed67' http://localhost/36/interfaces/



