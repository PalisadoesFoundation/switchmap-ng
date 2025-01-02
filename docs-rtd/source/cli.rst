Command Line Interface (CLI)
============================

This page outlines how to use the ``switchmap-ng`` command line interface (CLI)

Viewing ``switchmap-ng`` status
-------------------------------

There are a few important ``switchmap-ng`` daemons. 

1) **Dashboard** Displays device data on web pages
2) **poller:** Gets data from devices
3) **server:** An API server that interacts with a backend database. It accepts data from the poller and stores it in a cache. It also provides data to the dashboard.
4) **ingester:** Updates the database with data from the cache.

You can get the status of each daemon using the following CLI commands:

**NOTE:** Remember before running any of these commands to first activate ``venv``

.. code-block:: bash

    $ source venv/bin/activate

Poller status
~~~~~~~~~~~~~

You can get the status of the poller using this command:

.. code-block:: bash

    (venv) $ bin/systemd/switchmap_poller --status


API server status
~~~~~~~~~~~~~~~~~

You can get the status of the API server using this command:

.. code-block:: bash

    (venv) $ bin/systemd/switchmap_server --status
    
Ingester status
~~~~~~~~~~~~~~~

You can get the status of the ingester using this command:

.. code-block:: bash

    (venv) $ bin/systemd/switchmap_ingester --status

Dashboard status
~~~~~~~~~~~~~~~~

You can get the status of the dashboard using this command:

.. code-block:: bash

    (venv) $ bin/systemd/switchmap_dashboard --status

Managing the ``switchmap-ng`` Daemons
-------------------------------------

**Note:** You will need to do a restart whenever you modify a configuration parameter.


Poller Management
~~~~~~~~~~~~~~~~~

The poller can be started, stopped and restarted using the following commands. Use the ``--force`` option only if the daemon may be hung. 

.. code-block:: bash

    (venv) $ bin/systemd/switchmap_poller --start
    
    (venv) $ bin/systemd/switchmap_poller --stop
    (venv) $ bin/systemd/switchmap_poller --stop --force
    
    (venv) $ bin/systemd/switchmap_poller --restart
    (venv) $ bin/systemd/switchmap_poller --restart --force


API Server Management
~~~~~~~~~~~~~~~~~~~~~

The server can be started, stopped and restarted using the following commands. Use the ``--force`` option only if the daemon may be hung. 

.. code-block:: bash

    (venv) $ bin/systemd/switchmap_server --start
    
    (venv) $ bin/systemd/switchmap_server --stop
    (venv) $ bin/systemd/switchmap_server --stop --force
    
    (venv) $ bin/systemd/switchmap_server --restart
    (venv) $ bin/systemd/switchmap_server --restart --force

Ingester Management
~~~~~~~~~~~~~~~~~~~

The ingester can be started, stopped and restarted using the following commands. Use the ``--force`` option only if the daemon may be hung. 

.. code-block:: bash

    (venv) $ bin/systemd/switchmap_ingester --start
    
    (venv) $ bin/systemd/switchmap_ingester --stop
    (venv) $ bin/systemd/switchmap_ingester --stop --force
    
    (venv) $ bin/systemd/switchmap_ingester --restart
    (venv) $ bin/systemd/switchmap_ingester --restart --force

Dashboard Management
~~~~~~~~~~~~~~~~~~~~

The dashboard can be started, stopped and restarted using the following commands. Use the ``--force`` option only if the daemon may be hung. 

.. code-block:: bash

    (venv) $ bin/systemd/switchmap_dashboard --start
    
    (venv) $ bin/systemd/switchmap_dashboard --stop
    (venv) $ bin/systemd/switchmap_dashboard --stop --force
    
    (venv) $ bin/systemd/switchmap_dashboard --restart
    (venv) $ bin/systemd/switchmap_dashboard --restart --force


Testing The Ability to Poll Devices
-----------------------------------

You may want to verify that the poller can access the hosts in the configuration. This can be done using the ``switchmap_poller_test.py`` command.

.. code-block:: bash

    (venv) $ bin/tools/switchmap_poller_test.py --hostname HOSTNAME

Viewing ``switchmap-ng`` logs
-----------------------------

When troubleshooting it is a good practice to view the ``switchmap-ng`` log files. 

These can be found in the directory configured with the ``log_directory`` in the configuration. The default is in the ``logs/`` directory.

1) ``switchmap.log``: The general log file
2) ``switchmap-server.log``: The log file used by the API server
3) ``switchmap-poller.log``: The log file used by the poller
4) ``switchmap-ingester.log``: The log file used by the ingester
5) ``switchmap-dashboard.log``: The log file used by the dashboard

