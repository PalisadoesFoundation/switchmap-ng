Testing & Troubleshooting
=========================

Here's how you can test your installation of ``switchmap-ng``.

Testing Operation After Installation
------------------------------------

There are a number of steps to take to make sure you have installed ``switchmap-ng`` correctly. This section explains how to do basic testing before putting ``switchmap-ng`` into production.

Start the API Interactively
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start the ``switchmap-ng`` API interactively.

::

    $ bin/switchmap_dashboard --start


Start the Poller Interactively
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The poller will need to be running prior to testing.

::

    $ bin/switchmap_poller --start


Test Poller Functionality
~~~~~~~~~~~~~~~~~~~~~~~~~

Now that both the API and poller are running, it's time to test functionality by running the ``bin/tools/test_installation.py`` script

Here is an example of a successful test:

::

    $ bin/tools/test_installation.py --all_hosts
    Valid credentials found: hostname1
    Valid credentials found: hostname2
    $

You will see errors if none of the configured SNMP groups can be used to contact a host, or the host is not contactable. If this happens, check your configuration and the network access from your server to the remote host.

Test API Functionality
~~~~~~~~~~~~~~~~~~~~~~

Testing the API is easy. Just visit the following URL:

::

    http://hostname/switchmap-ng


A sample system startup script can be found in the
``examples/linux/systemd/switchmap_poller.service`` file. Follow the instructions in the file to make changes to the startup operation of the ``poller`` daemon.

**Note:** There will be no visible output when the ``poller`` is running. The ``poller`` logs its status to the ``log/switchmap.log`` file by default. You will be able to see this interaction dynamically by running the following command:

::

    $ tail -f etc/switchmap.log


Troubleshooting Using System Logs
---------------------------------

There are different log files to check.

Troubleshooting the API
~~~~~~~~~~~~~~~~~~~~~~~

There will be no visible output when the ``API`` is running. The ``API`` logs its status to the ``log/switchmap_dashboard.log`` file by default. You will be able to see this interaction dynamically by running the following command:

::

    $ tail -f etc/switchmap_dashboard.log

Troubleshooting the Poller
~~~~~~~~~~~~~~~~~~~~~~~~~~

There will be no visible output when the ``Poller`` is running. The ``Poller`` logs its status to the ``log/switchmap.log`` file by default. You will be able to see this interaction dynamically by running the following command:

::

    $ tail -f etc/switchmap.log

