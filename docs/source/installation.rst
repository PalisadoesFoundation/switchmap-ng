Installation
============

This section outlines how to install and do basic configuration of ``switchmap-ng``.

Dependencies
------------

``switchmap-ng`` has the following requirements:

* python >= 3.5
* python3-pip

It will not work with lower versions.

Ubuntu / Debian / Mint
~~~~~~~~~~~~~~~~~~~~~~

The commands for installing the dependencies are:

::

    $ sudo apt-get -y install python3 python3-pip python3-dev



Centos / Fedora
~~~~~~~~~~~~~~~

The commands for installing the dependencies are:

::

    $ sudo dnf -y install python3 python3-pip python3-dev memcached


The Installation Process
------------------------

Installation is simple. Follow these steps

Verify Dependencies
~~~~~~~~~~~~~~~~~~~

The first thing to do is verify that your system has the correct prerequisites. Run this command to make sure all is OK:

::

    $ bin/tools/prerequisites.py

Do the appropriate remediation to fix any reported issues. Run any commands this script suggests.

Be prepared to install ``switchmap-ng`` on a newer version of your operating system.

Clone the Repository
~~~~~~~~~~~~~~~~~~~~

Now clone the repository and copy the sample configuration file to its
final location.

::

    $ git clone https://github.com/PalisadoesFoundation/switchmap-ng
    $ cd switchmap-ng
    $ export PYTHONPATH=`pwd`


Edit Configuration File
~~~~~~~~~~~~~~~~~~~~~~~

Edit the SNMP credential information in the configuration file.

::

    $ cp examples/etc/config.yaml etc/config.yaml
    $ vim etc/config.yaml

    snmp_groups:
        - group_name: Corporate Campus
          snmp_version: 3
          snmp_secname: woohoo
          snmp_community:
          snmp_port: 161
          snmp_authprotocol: sha
          snmp_authpassword: testing123
          snmp_privprotocol: des
          snmp_privpassword: secret_password
        

Run Installation Script
~~~~~~~~~~~~~~~~~~~~~~~

Run the installation script. There are two alternatives:

:Run Interactively: This is the preferred method if you don't have ``root`` access to your system. ``switchmap-ng`` `will not` automatically restart on reboot using this method. To make ``switchmap-ng`` run with your username, then execute this command:

::

    $ python3 setup.py

:Run as System Daemon: If you want ``switchmap-ng`` to be run as a system daemon, then execute these commands. ``switchmap-ng`` `will` automatically restart on reboot using this installation method. (**Note**: Do not run setup using ``sudo``. Use ``sudo`` to become the root user first)

This example assumes you have downloaded ``switchmap-ng`` in the ``/home/switchmap-ng`` directory. Change this to the appropiate directory in your case.

::

    $ pwd
    /home/switchmap-ng
    $ sudo su -
    # cd /home/switchmap-ng
    # python3 setup.py



Next Steps
----------

It is now time to review the various configuration options.
