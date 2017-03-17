Advanced Operation
==================

The ``switchmap-ng`` CLI is meant for ease of use. This page shows some advanced features.


Operating the Poller as a System Daemon
---------------------------------------
This is the preferred mode of operation for **production systems**. This mode is automatically configured if you installed ``switchmap-ng`` using the ``root`` user.

**Note:** Sample ``systemd`` files can be found in the ``examples/linux/systemd/`` directory.


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



Operating the API as a System Daemon
------------------------------------

This is the preferred mode of operation for production systems. This mode is automatically configured if you installed ``switchmap-ng`` using the ``root`` user.

**Note:** Sample ``systemd`` files can be found in the ``examples/linux/systemd/`` directory.

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
