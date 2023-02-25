Configuration
=============

The ``examples/configuration`` directory includes a sample file that
can be edited. ``switchmap-ng`` assumes all files in this directory, or any
other specified configuration directory, only contains ``switchmap-ng``
configuration files. Most user will only need to edit the three files
supplied.

You must place your configuration file in the ``etc/`` directory as your
permanent configuration file location.

Sample Configuration File
-------------------------

Here is a sample configuration file that will be explained later in
detail. ``switchmap-ng`` will attempt to contact hosts with each of the
parameter sets in the ``snmp_group`` section till successful.

::

    main:
        log_directory: /home/switchmap-ng/log
        log_level: info
        system_directory: /opt/switchmap-ng/cache
        agent_subprocesses: 20
        bind_port: 7000
        listen_address: 0.0.0.0
        hostnames:
          - 192.168.1.1
          - 192.168.1.2
          - 192.168.1.3
          - 192.168.1.4
        polling_interval: 86400

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

        - group_name: Remote Sites
          snmp_version: 3
          snmp_secname: foobar
          snmp_community:
          snmp_port: 161
          snmp_authprotocol: sha
          snmp_authpassword: testing123
          snmp_privprotocol: aes
          snmp_privpassword: secret_password


The ``main:`` Section
~~~~~~~~~~~~~~~~~~~~~

This is the section of the configuration file that governs the general operation of ``switchmap-ng``. Here is how it is configured.

=================================== ========
Parameter                           Description
=================================== ========
``main:``                           YAML key describing the server configuration.
``log_directory:``                  The directory where ``switchmap-ng`` places its log files
``log_level:``                      Defines the logging level. ``debug`` level is the most verbose, followed by ``info``, ``warning`` and ``critical``
``system_directory:``                Location where data retrieved from devices will be stored.
``agent_subprocesses:``             The maximum number of subprocesses used to collect data from devices
``listen_address:``                 IP address the API will be using. The default is ``localhhost``. This should not need to be changed.
``bind_port:``                      The TCP port the API will use. This should not need to be changed.
``hostnames:``                      A list of hosts that will be polled for data.
``polling_interval:``               The frequency in seconds with which the poller will query devices
=================================== ========

The ``snmp_groups:`` Section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the section of the configuration file that governs the SNMP credentials to be used to retrieve data from devices. You can have multiple groups, each with a separate ``group_name``. This is how ``switchmap-ng`` uses this information.

1. ``switchmap-ng`` will attempt to use each set of group credentials until it is successful. It will skip devices that it cannot authenticate against or reach.
2. ``switchmap-ng`` will keep track of the most recently used credentials to successfully obtain data and will use these credentials first.


=================================== ========
Parameter                           Description
=================================== ========
snmp_groups:                        YAML key describing groups of SNMP authentication parameter. All parameter groups are listed under this key.
group_name:                         Descriptive name for the group
snmp_version:                       SNMP version. Must be present even if blank. Only SNMP versions 2 and 3 are supported by the project.
snmp_secname:                       SNMP security name (SNMP version 3 only). Must be present even if blank.
snmp_community:                     SNMP community (SNMP version 2 only). Must be present even if blank.
snmp_port:                          SNMP Authprotocol (SNMP version 3 only). Must be present even if blank.
snmp_authprotocol:                  SNMP AuthPassword (SNMP version 3 only). Must be present even if blank. 
snmp_authpassword:                  SNMP PrivProtocol (SNMP version 3 only). Must be present even if blank.
snmp_privprotocol:                  SNMP PrivProtocol (SNMP version 3 only). Must be present even if blank.
snmp_privpassword:                  SNMP PrivPassword (SNMP version 3 only). Must be present even if blank.
snmp_port:                          SNMP UDP port
=================================== ========
