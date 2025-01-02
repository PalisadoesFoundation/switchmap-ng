Advanced Operation
==================

The ``switchmap-ng`` CLI is meant for ease of use. This page shows some advanced features.


Running Switchmap Processes as System Daemons
=============================================

All the switchmap daemon executables can be configured to run at the system level using systemd. This means that they will reliably restart after a reboot. This is therefore the preferred mode of operation for production systems. 

1) Sample ``systemd`` files can be found in the ``examples/linux/systemd/`` directory.
2) Each file contains instructions as to what to do 


Operating the Poller as a System Daemon
---------------------------------------


The ``poller`` can be started like this:

.. code-block:: bash

    $ sudo systemctl start switchmap_poller.service

The ``poller`` can be stopped like this:

.. code-block:: bash

    $ sudo systemctl stop switchmap_poller.service

You can get the status of the ``poller`` like this:

.. code-block:: bash

    $ sudo systemctl status switchmap_poller.service

You can get the ``poller`` to automatically restart on boot like this:

.. code-block:: bash

    $ sudo systemctl enable switchmap_poller.service


Operating the API server as a System Daemon
-------------------------------------------


The ``server`` can be started like this:

.. code-block:: bash

    $ sudo systemctl start switchmap_server.service

The ``server`` can be stopped like this:

.. code-block:: bash

    $ sudo systemctl stop switchmap_server.service

You can get the status of the ``server`` like this:

.. code-block:: bash

    $ sudo systemctl status switchmap_server.service

You can get the ``server`` to automatically restart on boot like this:

.. code-block:: bash

    $ sudo systemctl enable switchmap_server.service


Operating the Ingester as a System Daemon
-----------------------------------------


The ``ingester`` can be started like this:

.. code-block:: bash

    $ sudo systemctl start switchmap_ingester.service

The ``ingester`` can be stopped like this:

.. code-block:: bash

    $ sudo systemctl stop switchmap_ingester.service

You can get the status of the ``ingester`` like this:

.. code-block:: bash

    $ sudo systemctl status switchmap_ingester.service

You can get the ``ingester`` to automatically restart on boot like this:

.. code-block:: bash

    $ sudo systemctl enable switchmap_ingester.service


Operating the Dashboard as a System Daemon
------------------------------------------


The ``dashboard`` can be started like this:

.. code-block:: bash

    $ sudo systemctl start switchmap_dashboard.service

The ``dashboard`` can be stopped like this:

.. code-block:: bash

    $ sudo systemctl stop switchmap_dashboard.service

You can get the status of the ``dashboard`` like this:

.. code-block:: bash

    $ sudo systemctl status switchmap_dashboard.service

You can get the ``dashboard`` to automatically restart on boot like this:

.. code-block:: bash

    $ sudo systemctl enable switchmap_dashboard.service
