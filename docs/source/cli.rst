Command Line Interface (CLI)
============================

This page outlines how to use the ``switchmap-ng`` command line interface (CLI)

Viewing ``switchmap-ng`` status
-------------------------------

There are two important ``switchmap-ng`` daemons. 

1) **poller:** Gets data from devices
2) **API:** Displays device data on web pages

You can get the status of  each daemon using the following CLI commands:

Poller status
~~~~~~~~~~~~~

You can get the status of the poller using this command:

::

    $ bin/switchmap-ng-cli show poller status


API status
~~~~~~~~~~

You can get the status of the API using this command:

::

    $ bin/switchmap-ng-cli show api status
    

Managing the ``switchmap-ng`` Daemons
-------------------------------------

You can manage the daemons using the CLI. Here's how:

Poller Management
~~~~~~~~~~~~~~~~~

The poller can be started, stopped and restarted using the following commands. Use the ``--force`` option only if the daemon may be hung. 

::

    $ bin/switchmap-ng-cli poller start
    
    $ bin/switchmap-ng-cli poller stop
    $ bin/switchmap-ng-cli poller stop --force
    
    $ bin/switchmap-ng-cli poller restart
    $ bin/switchmap-ng-cli poller restart --force

**Note:** You will need to do a restart whenever you modify a configuration parameter.

API Management
~~~~~~~~~~~~~~

The API can be started, stopped and restarted using the following commands. Use the ``--force`` option only if the daemon may be hung. 

::

    $ bin/switchmap-ng-cli api start
    
    $ bin/switchmap-ng-cli api stop
    $ bin/switchmap-ng-cli api stop --force
    
    $ bin/switchmap-ng-cli api restart
    $ bin/switchmap-ng-cli api restart --force

**Note:** You will need to do a restart whenever you modify a configuration parameter.

Testing The Ability to Poll Devices
-----------------------------------

You will need to verify that the poller can access the hosts in the configuration.


Viewing Configured Hosts
~~~~~~~~~~~~~~~~~~~~~~~~

You can view the configured hosts using this command.

::

    $ bin/switchmap-ng-cli show hostnames


Testing Host Pollability
~~~~~~~~~~~~~~~~~~~~~~~~

You can test a host using this command.

::

    $ bin/switchmap-ng-cli test poller --hostname HOSTNAME


You can test all hosts using this command.

::

    $ bin/switchmap-ng-cli test poller --all
    

Viewing ``switchmap-ng`` logs
-----------------------------

When troubleshooting it is a good practice to view the ``switchmap-ng`` log files.

Poller logs
~~~~~~~~~~~

You can view the poller logs using this command:

::

    $ bin/switchmap-ng-cli show poller logs


API logs
~~~~~~~~

You can view the API logs using this command:

::

    $ bin/switchmap-ng-cli show api logs

Viewing the ``switchmap-ng`` Configuration
------------------------------------------

You can view the configuration using this command:

::

    $ bin/switchmap-ng-cli show configuration
