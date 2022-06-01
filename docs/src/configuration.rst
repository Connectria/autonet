Configuration
=============

Autonet uses the `config-engine` package as it's application configuration
provider.  ConfigEngine allows Autonet to read configuration from multiple
sources as required.  For more information on how ConfigEngine works, please
see the `documentation <https://connectria.github.io/conf-engine>`_.
Autonet requires a minimal amount of configuration to get going.  Autonet's
built in authentication database must be configured to store users and token
data.

Additional configuration may be required for various backend and device
drivers.  See the documentation for those drivers for more details.

Application Configuration
-------------------------

**[DEFAULT]**

=========== ========= ========= ===============================================
Option      Type      Default   Description
=========== ========= ========= ===============================================
debug       boolean   False     Enables debug mode.
bind_host   string    0.0.0.0   Sets the IP address that Autonet will
                                attempt to listen on.  By default Autonet will
                                listen on all available interfaces.
port        integer   8800      Sets the TCP port that Autonet will listen on.
backend     string    config    Specifies the backend driver to be used for
                                device inventory
=========== ========= ========= ===============================================

**[database]**

=========== ========= ========== ===============================================
Option      Type      Default    Description
=========== ========= ========== ===============================================
connection  string    sqlite:/// Database connection string that points to
                                 the user database.
=========== ========= ========== ===============================================

