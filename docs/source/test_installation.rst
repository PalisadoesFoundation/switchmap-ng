infoset
=======

``infoset`` is Python 3 inventory system that reports and tabulates the
status of network connected devices. The information reported includes:

1. Open Systems Interconnection model (OSI model) data such as:
2. Layer 1 information (Network port names, speed, state, neighbors)
3. Layer 2 information (VLANs, 802.1q trunk links)
4. Layer 3 information (ARP information)
5. System status

Features
--------

``infoset`` has the following features:

1. Open source.
2. Written in python, a modern language.
3. Easy configuration.
4. Threaded polling of devices for data. Fast.
5. Support for Cisco and Juniper gear. More are expected to be added with time.
6. Support for SNMPv2 and/or SNMPv3 for all configured network devices.

We are always looking for more contributors!

Inspiration
-----------

The project took inspiration from switchmap whose creator, Pete Siemsen,
has been providing guidance.

Oversight
---------

``infoset`` is a student collaboration between:

1. The University of the West Indies Computing Society. (Kingston,
   Jamaica)
2. The University of Techology, IEEE Student Branch. (Kingston, Jamaica)
3. The Palisadoes Foundation http://www.palisadoes.org

And many others.

Dependencies
------------

The only dependencies that must be manually installed for this project
are pip,python3 ### Ubuntu / Debian / Mint

The commands are:

::

    # sudo apt-get install python3 python3-pip python3-dev librrd-dev
    # pip3 install --user sqlalchemy

Fedora
~~~~~~

The commands are:

::

    # sudo dnf install python3 python3-pip python3-dev librrd-dev
    # pip3 install --user sqlalchemy

Installation
============

Installation is simple. Run the following commands:

::

    # git clone https://github.com/UWICompSociety/infoset
    # cd infoset
    # export PYTHONPATH=`pwd`
    # ./setup.py --install
    # source ~/.bashrc
    # sudo make
    # source venv/bin/activate
    # sudo make install

.. figure:: http://i.imgur.com/cJP2vks.gif?raw=true
   :alt: uh oh

   uh oh

Configuration and Usage
=======================

There are a number of required steps to configure ``infoset``. 1. Place
a valid configuration file in the ``etc/`` directory 2. Run the
``bin/agentsd.py --start`` script to start data collection 3. Run the
``server.py`` script to view the web pages

These will be convered in detail next:

Configuration Samples
---------------------

The ``examples/`` directory includes a number of sample files. These
will now be explained.

infoset Configuration Samples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``examples/configuration`` directory includes a sample file that can
be edited. The ``README.md`` file there explains the parameters.

You must place your configuration file in the ``etc/`` directory as your
permanent configuration file location.

Apache Configuration Samples (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``examples/linux/apache`` directory includes sample files to create
a:

1. Dedicated ``infoset`` site (``sites-available.example.org.conf``)
   running on port 80
2. URI of an existing site (``conf-available.example.conf``) running on
   port 80

Starting Data Collection
------------------------

**NOTE!** You must have a valid configuration file placed in the ``etc``
directory before activating data collection.

The ``bin/agentsd.py`` script starts all the configured data collection
agents automatically. It will only attempt to start and monitor the
agents that are ``enabled`` in the configuration file.

The script can be started like this:

::

    $ bin/agentsd.py --start

**NOTE!** Make sure this script runs at boot by placing the
``agentsd.py`` command in your ``/etc/rc.local`` file.

Viewing Data Web Pages
----------------------

Infoset also includes a web interface. To start the server run
``python3 server.py`` then navigate to http://localhost:5000

Other Useful Scripts
====================

``infoset`` has a number of auxilliary scripts that could be useful.

The Toolbox.py Script
---------------------

``infoset`` comes with a handy ``toolbox.py`` script. It provides all
the same functionality as creating or installing the executable.

Testing Host Connectivity
~~~~~~~~~~~~~~~~~~~~~~~~~

You can test connectivity to a host using this command where the
configuration directory is ``etc/`` and the host is ``host1``

::

    $ bin/toolbox.py test --directory etc/  --host host1

Polling All Devices
~~~~~~~~~~~~~~~~~~~

This command will execute against all configured hosts and create
appropriate YAML files in the configuration file's
``$DATA_DIRECTORY/snmp`` directory

::

    $ bin/toolbox.py poll --directory etc/

Next Steps
==========

There are many dragons to slay and kingdoms to conquer! ## Contribute
Here are a few things to know.

1. Contributions are always welcome. Contact our team for more.
2. View our contributor guidelines here:
   https://github.com/UWICompSociety/infoset/blob/master/CONTRIBUTING.md
3. View our guidelines for committing code here:
   https://github.com/UWICompSociety/infoset/blob/master/COMMITTERS.md

Mailing list
------------

Our current mailing list is:
https://groups.google.com/forum/#!forum/gdg-jamaica ## New Features
Visit our GitHub issues for a full list of features and bug fixes.
https://github.com/UWICompSociety/infoset/issues ## Design Overview
Visit our wiki's ``infoset`` document for the rationale of the design.
http://wiki.palisadoes.org/index.php/Infoset ## Sample Output Visit
http://calico.palisadoes.org/infoset to view ``infoset``'s latest stable
web output.
