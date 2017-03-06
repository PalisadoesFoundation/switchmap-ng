Operation
=========

``switchmap-ng`` has two major components. These are:

1. **The Poller**: Periodically retrieves data from devices and stores it in the cache directory.
2. **The API**: Retrieves data from the cache for display via a web server


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
    

**Note:** Refer to the Troubleshooting page for details on how to test the functionality of your installation.

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

**Note:** Refer to the Troubleshooting page for details on how to test the functionality of your installation.



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

**Note:** Refer to the Troubleshooting page for details on how to test the functionality of your installation.

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

**Note:** Refer to the Troubleshooting page for details on how to test the functionality of your installation.



Setup Webserver For ``switchmap-ng``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``switchmap-ng`` has sample configurations for the Apache webserver. This step is mandatory.

:Apache: Run the following commands from the top directory of ``switchmap-ng``

::

    $ sudo cp examples/linux/apache/switchmap-ng-apache.conf /etc/apache2/conf-available
    $ sudo ln -s /etc/apache2/conf-available/switchmap-ng-apache.conf /etc/apache2/conf-enabled/switchmap-ng-apache.conf 

    # (Ubuntu only)
    $ sudo a2enmod proxy_http
    $ systemctl restart apache2.service

    # (RedHat / CentOS)    
    $ systemctl restart httpd.service


