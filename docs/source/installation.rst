Installation
============

This section outlines how to install and do basic configuration of ``switchmap-ng``.

Install Prerequisite Packages
-----------------------------

``switchmap-ng`` has the following requirements:

* python >= 3.5
* python3-pip

It will not work with lower versions.

Ubuntu / Debian / Mint
~~~~~~~~~~~~~~~~~~~~~~

The commands for installing the dependencies are:

::

    $ sudo apt-get -y install python3 python3-pip snmp libsnmp-dev snmp-mibs-downloader gcc python-dev


Centos / Fedora
~~~~~~~~~~~~~~~

The commands for installing the dependencies are:

::

    $ sudo dnf -y install python3 python3-pip net-snmp-utils net-snmp-devel gcc python-devel


Install Switchmap-NG
--------------------

Installation is simple. Follow these steps


Clone the Repository
~~~~~~~~~~~~~~~~~~~~

Now clone the repository and copy the sample configuration file to its
final location.

::

    $ git clone https://github.com/PalisadoesFoundation/switchmap-ng
    $ cd switchmap-ng


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

**Installing as a regular user**

There are some things to keep in mind when installing `switchmap-ng` as a regular user.

1) Use this method if you don't have ``root`` access to your system.
2) The ``switchmap-ng`` daemons `will not` automatically restart on reboot using this method.

To make ``switchmap-ng`` run with your username, then execute this command:

::

    $ maintenance/install.py

**Installing as the "root" user**

There are some things to keep in mind when installing `switchmap-ng` as the `root` user.

1) The ``switchmap-ng`` daemons `will` automatically restart on reboot using this installation method.
2) **Note**: Do not run setup using ``sudo``. Use ``sudo`` to become the ``root`` user first.

To install ``switchmap-ng`` as the ``root`` user execute this command:

::

    # maintenance/install.py


Testing Installation
--------------------

There are a number of ways to test your installation.

Testing Polling
~~~~~~~~~~~~~~~
You can test your SNMP configuration and connectivity to your devices using the ``switchmap-ng-cli`` utility like this:

::

    $ bin/switchmap-ng-cli test poller --all

Testing the Web Interface
~~~~~~~~~~~~~~~~~~~~~~~~~
You can test whether the API is working by visiting this url. (You will need to make adjustments if you installed the application on a remote server):

::

   http://localhost:7000/switchmap-ng/

The Webserver help page provides the necessary steps to view switchmap on port 80 using Apache or Nginx


Next Steps
----------

It is now time to review the various configuration options.
