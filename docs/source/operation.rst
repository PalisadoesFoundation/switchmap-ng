Operation
=========

``switchmap-ng`` has two major components. These are:

1. **The Poller**: Periodically retrieves data from devices and stores it in the cache directory.
2. **The API**: Retrieves data from the cache for display via a web server

Explanations of how to permanently run each component will be given shortly, but first we'll cover how to test your installation.

Testing Operation After Installation
------------------------------------

There are a number of steps to take to make sure you have installed ``switchmap-ng`` correctly. This section explains how to do basic testing before putting ``switchmap-ng`` into production.

Start the API Interactively
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start the ``switchmap-ng`` API interactively.

::

    $ bin/switchmap-ng-api --start


Start the Poller Interactively
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The poller will need to be running prior to testing.

::

    $ bin/switchmap-ng-poller --start


Test API Functionality
~~~~~~~~~~~~~~~~~~~~~~

Now that both the API and poller are running, it's time to test functionality by running the ``bin/tools/test_installation.py`` script

Here is an example of a successful test:

::

    $ bin/tools/test_installation.py
    2016-12-03 18:12:56,640 - switchmap_console - INFO - [peter] (1054S): Successfully posted test data for agent ID 558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749
    2016-12-03 18:12:56,656 - switchmap_console - INFO - [peter] (1054S): Successfully retrieved test data for agent ID 558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749

    OK

    $

Refer to the Troubleshooting section of this page to rectify any issues.

Stop After Successful Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that you have tested the functionality successsfully it is time to stop the interactive API session until you decide the best method to run ``switchmap-ng``, either interactively as you did during the testing or as system daemons. 

::

    $ bin/switchmap-ng-api --stop
    $ bin/switchmap-ng-poller --stop


The procedures to operate ``switchmap-ng`` using the various types of daemons will be covered next.


Poller Operation
------------------

The ``poller`` can be operated in one of two modes:

#.  **System Daemon**: As a system daemon which will automatically restart after a reboot.
#.  **User Daemon**: Interactively run by a user from the CLI. The ``poller`` will not automatically restart after a reboot.


Usage of the ``poller`` in each mode will be discussed next.


The Poller as a System Daemon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is the preferred mode of operation for production systems. This mode is automatically configured if you installed ``switchmap-ng`` using the ``root`` user.

The ``poller`` can be started like this:

::

    $ sudo systemctl start switchmap-ng-poller.service

The ``poller`` can be stopped like this:

::

    $ sudo systemctl stop switchmap-ng-poller.service

You can get the status of the ``poller`` like this:

::

    $ sudo systemctl status switchmap-ng-poller.service

You can get the ``poller`` to automatically restart on boot like this:

::

    $ sudo systemctl enable switchmap-ng-poller.service
    
A sample system startup script can be found in the
``examples/linux/systemd/switchmap-ng-poller.service`` file. Follow the instructions in the file to make changes to the startup operation of the ``poller`` daemon.

**Note:** There will be no visible output when the ``poller`` is running. The ``poller`` logs its status to the ``log/switchmap-ng.log`` file by default. You will be able to see this interaction dynamically by running the following command:

::

    $ tail -f etc/switchmap-ng.log


The Poller as a User Daemon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This mode is available if you want to run the ``poller`` in a standalone mode. The ``poller`` can be started like this:

::

    $ bin/switchmap-ng-poller --start

The poller can be stopped like this:

::

    $ bin/switchmap-ng-poller --stop

You can get the status of the poller like this:

::

    $ bin/switchmap-ng-poller --status

You may want to make sure that the poller is running correctly. This will be covered next.

**Note:** There will be no visible output when the ``poller`` is running. The ``poller`` logs its status to the ``etc/switchmap-ng.log`` file by default. You will be able to see this interaction dynamically by running the following command:

::

    $ tail -f etc/switchmap-ng.log

API Operation
-------------
The ``API`` can be operated in one of two modes:

#.  **System Daemon**: As a system daemon which will automatically restart after a reboot.
#.  **User Process**: Run by a user from the CLI. The ``API`` will not automatically restart after a reboot.

Usage of the ``API`` in each mode will be discussed next.


The API as a System Daemon
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the preferred mode of operation for production systems. This mode is automatically configured if you installed ``switchmap-ng`` using the ``root`` user.

The ``API`` can be started like this:

::

    $ sudo systemctl start switchmap-ng-api.service

The ``API`` can be stopped like this:

::

    $ sudo systemctl stop switchmap-ng-api.service

You can get the status of the ``API`` like this:

::

    $ sudo systemctl status switchmap-ng-api.service

You can get the ``API`` to automatically restart on boot like this:

::

    $ sudo systemctl enable switchmap-ng-api.service
    
A sample system startup script can be found in the
``examples/linux/systemd/switchmap-ng-api.service`` file. Follow the instructions in the file to make changes to the startup operation of the ``API`` daemon.

**Note:** There will be no visible output when the ``API`` is running. The ``API`` logs its status to the ``etc/api-web.log`` file by default. You will be able to see this interaction dynamically by running the following command:

::

    $ tail -f etc/api-web.log


The API as a User Process
~~~~~~~~~~~~~~~~~~~~~~~~~

You can run the API in standalone mode using the  ``bin/switchmap-ng-api`` script. The standalone ``API`` can be started like this:

::

    $ bin/switchmap-ng-api --start

The API can be stopped like this:

::

    $ bin/switchmap-ng-api --stop

You can get the status of the API like this:

::

    $ bin/switchmap-ng-api --status

**Note:** There will be no visible output when the API is running. Web traffic to the API is logged to the ``etc/api-web.log`` file by default. You will be able to see this interaction dynamically by running the following command:

::

    $ tail -f etc/api-web.log

