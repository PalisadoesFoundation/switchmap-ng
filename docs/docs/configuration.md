---
title: Configuration
sidebar_label: Configuration
sidebar_position: 3
---

# Configuration
The `examples/etc` directory includes a sample file that can be edited.
`switchmap-ng` assumes all files in this directory, or any other
specified configuration directory, only contains `switchmap-ng`
configuration files. Most user will only need to edit the three files
supplied.

# Setting Your Configuration File

All switchmap executables default to searching for configuration files
in the `etc/` directory of the `switchmap-ng` code base.

This can be changed by setting the `SWITCHMAP_CONFIGDIR` environmental
variable to the location of your choice. This can be done like this:

    export SWITCHMAP_CONFIGDIR=/path/to/the/configuration/directory

# Sample Configuration File

Here is a sample configuration file that will be explained later in
detail. `switchmap-ng` will attempt to contact hosts with each of the
parameter sets in the `snmp_group` section till successful.

**NOTE:** If a default value is mentioned in the documentation it means
that if the corresponding parameter is left out of the configuration,
that the default value will be assumed.

``` yaml
core:
  agent_subprocesses: 20
  system_directory: /path/to/system/directory
  log_level: debug
  log_directory: /path/to/log/directory
  daemon_directory: /path/to/daemon/directory
  multiprocessing: True

dashboard:
  bind_port: 7001
  api_listen_address: localhost

server:
  username: switchmap
  api_listen_address: localhost
  bind_port: 7000
  ingest_interval: 86400
  purge_after_ingest: True
  cache_directory: /path/to/cache/directory
  db_host: localhost
  db_name: switchmap
  db_user: switchmap
  db_pass: CHANGE_ME_NOW
  db_pool_size: 30

poller:
  username: switchmap
  polling_interval: 86400
  server_address: localhost
  server_bind_port: 7000
  server_username: null
  server_password: None
  server_https: false
  zones:
    - zone: TEST
      hostnames:
        - 192.168.1.1
        - 192.168.1.2
        - 192.168.1.3
        - 192.168.1.4
  snmp_groups:

    - group_name: V2
      snmp_version: 2
      snmp_secname:
      snmp_community: YOUR_SNMP_COMMUNITY
      snmp_port: 161
      snmp_authprotocol:
      snmp_authpassword:
      snmp_privprotocol:
      snmp_privpassword:
      enabled: True

  snmp_groups:
      - group_name: Corporate Campus
        snmp_version: 3
        snmp_secname: woohoo
        snmp_community:
        snmp_port: 161
        snmp_authprotocol: sha
        snmp_authpassword: YOUR_AUTH_PASSWORD
        snmp_privprotocol: des
        snmp_privpassword: YOUR_PRIV_PASSWORD

      - group_name: Remote Sites
        snmp_version: 3
        snmp_secname: foobar
        snmp_community:
        snmp_port: 161
        snmp_authprotocol: sha
        snmp_authpassword: YOUR_AUTH_PASSWORD
        snmp_privprotocol: aes
        snmp_privpassword: YOUR_PRIV_PASSWORD
```

## Configuration File Sections

This section explains the purpose of the various sections of the configuration.

1)  `switchmap-ng` runs three separate daemon processes. A Dashboard
    server, an API server, and the poller.
2)  Each daemon can run on the same physical device or VM. You can also
    split them up to run separately in a distributed architecture. The
    separation of the `dashboard`, `server` and `poller` sections makes
    it easier for you to do this.
3)  You can have multiple pollers located in different geographies
    posting data to a central API server. Each poller would have unique
    `poller` sections to match the devices in their location.
4)  You must only have one API server. You can have multiple dashboard
    and poller servers.

### The `core:` Section

This is the section of the configuration file that governs the general
operation of `switchmap-ng`. Here is how it is configured.

| Parameter | Description |
| --------- | ----------- |
| `core:` | YAML key describing the server configuration.|
| `system_directory:` | Location where temporary data files are stored. Make sure that the switchmap username has write access to it. defaults to the `var/` directory in the `switchmap-ng` root directory. |
| `log_directory:` | The directory where `switchmap-ng` places its log files. Make sure that the switchmap username has write access to it. Defaultsto the `log/`subdirectory of `system_directory`|
| `daemon_directory:` | The directory where `switchmap-ng` places its files necessary for proper daemon operation. Make sure that the switchmap username has write access to it. Defaults to the `daemon/`subdirectory of `system_directory`. <p>This directory needs to be empty on a reboot. So we recommend a few possible solutions:</p><p>1)  Place this directory in small RAM disk.The total storage required will be about 1 kB.</p><p>2)  If you plan to run the `switchmap-ng` executables as Linux daemons, then this should be set to `/var/run/switchmap` after testing with the default values.</p> |
| `log_level:` | Defines the logging level. `debug` level is the most verbose, followed by `info`, `warning` and `critical`|
| `agent_subprocesses:` | The maximum number of subprocesses used to process data. Defaults to the number of CPU cores in the system. |
| `multiprocessing:` | If set to False, the poller and ingester daemons will run as a single process. This is useful for troubleshooting. Defaults to `True` for better performance. |

### The `dashboard:` Section

This section of the file is used to configure the web dashboard used in
`switchmap-ng`.

Here is how it is configured:

| Parameter| Description |
| --------- | -----------|
| `dashboard:` | YAML key describing the poller configuration.|
| `api_listen_address:` | IP address the dashboard server will be using to host web pages. The default is `localhost`. This should be changed to the IP address of the dashboard server\'s network interface that web browsers can access.|
| `api_bind_port:` | The TCP port the dashboard server will use. Defaults to `7001`. In most cases this won\'t have to be changed.|
| `api_https:` | Set this to `true`if web browsers need to use HTTPs to access the dashboard server pages. Switchmap only uses the SSL capabilities of the pre-installed webserver of your choice to encrypt data sent over the network. Default `False`.|
| `api_password:` | The HTTPS simple authentication password that the dashboard server uses. Defaults to `None`.|
| `api_username:` | The HTTPS simple authentication username that the dashbord server uses. Defaults to `None`.|
| `username:` | The username under which all switchmap-ng dashboard server daemons will run. This is set to ensure that unauthorized users run the daemon code.|
| `server_address:` | The IP address to use for contacting the switchmap-ng server. The default is `localhost`.|
| `server_bind_port:` | The TCP port the switchmap-ng API server uses. This must match the `api_bind_port` setting in the API server\'s configuration. Defaults to `7000`. In most cases this won\'t have to be changed.|
| `server_https:` | Set this to `true`if the dashboard server needs to use HTTPs to access the switchmap-ng API server. Switchmap only uses the SSL capabilities of the pre-installed webserver of your choice to encrypt data sent over the network. Default `False`.|
| `server_password:` | The HTTPS simple authentication password that the switchmap-ng API server uses.|
| `server_username:` | The HTTPS simple authentication username that the switchmap-ng API server uses.|

### The `server:` Section

This section of the configuration file:

1)  needs to be added to the `core:` section if you plan to configure
    your server to be an API server.
2)  governs the API server operation of `switchmap-ng`. Here is how it
    is configured.

Here is how it is configured:

| Parameter| Description |
| --------- | -----------|
| `server:` | YAML key describing the poller configuration.|
| `username:` | The username under which all switchmap-ng poller daemons will run. This is set to ensure that unauthorized users run the daemon code.|
| `api_listen_address:` | IP address the server will be using to host web pages. The default is `localhost`. This should be changed to the IP address of a server network interface that the poller can access over the network. If the poller daemon resides on the same server then the default is OK.|
| `api_bind_port:` | The TCP port the API will use. Defaults to `7000`. In most cases this won\'t have to be changed.|
| `api_https:` | Set this to `true`if web browsers need to use HTTPs to access the API pages. Switchmap only uses the SSL capabilities of the pre-installed webserver of your choice to encrypt data sent over the network. Default `False`.|
| `api_password:` | The HTTPS simple authentication password that the API server uses. Defaults to `None`.|
| `api_username:` | The HTTPS simple authentication username that the dashbord server uses. Defaults to `None`.|
| `cache_directory:` | The directory where `switchmap-ng` places files containing polling data from the poller. Make sure that the switchmap username has write access to it. Defaults to the `cache/`subdirectory of `system_directory`|
| `db_host:` | MySQL database server hostname|
| `db_user:` | MySQL database username|
| `db_name:` | MySQL database name|
| `db_pass:` | MySQL database password|
| `db_pool_size:` | Size of the database connection pool. The default value is sufficient in most cases.|
| `db_max_overflow:` | TBD|
| `ingest_interval:` | The frequency with which the ingester daemon checks for new cache files in seconds. This must not be less than the poller\'s `polling_interval`value.|
| `purge_after_ingest:` | When `true`(default) only the most recently polled data is stored in the database.|

### The `poller:` Section

This section of the configuration file:

1)  needs to be added to the `core:` section if you plan to configure
    your server to be SNMP poller server.
2)  governs the polling operation of `switchmap-ng`.

Here is how it is configured.

| Parameter| Description |
| --------- | -----------|
| `poller:` | YAML key describing the poller configuration.|
| `username:` | The username under which all switchmap-ng poller daemons will run. This is set to ensure that unauthorized users run the daemon code.|
| `polling_interval:` | The frequency in seconds with which the poller will query devices|
| `server_address:` | The IP address to use for contacting the server. The default is `localhost`.|
| `server_bind_port:` | The TCP port the API server uses. This must match the `api_bind_port`setting in the API server\'s configuration. Defaults to `7000`. In most cases this won\'t have to be changed.|
| `server_https:` | Set this to `true`if the poller needs to use HTTPs to access the API server. Switchmap only uses the SSL capabilities of the pre-installed webserver of your choice to encrypt data sent over the network. Default `False`.|
| `server_password:` | The HTTPS simple authentication password that the API server uses.|
| `server_username:` | The HTTPS simple authentication username that the API server uses.|
| `hostnames:` | A list of hosts that will be polled for data.|

### The `zones:` Poller Section

This is the section of the configuration file that lists the devices
that will be polled for data. This is how `switchmap-ng` uses this
information.

| Parameter| Description |
| --------- | -----------|
| `zones:` | YAML key describing groups of devices grouped in zones.|
| `zone:` | Name of the zone|
| `notes:` | A brief line of text describing the zone|
| `hostnames:` | A list of devices that need to be polled|

#### The `snmp_groups:` Poller Section

This is the section of the configuration file that governs the SNMP
credentials to be used to retrieve data from devices. You can have
multiple groups, each with a separate `group_name`. This is how
`switchmap-ng` uses this information.

1.  `switchmap-ng` will attempt to use each set of group credentials
    until it is successful. It will skip devices that it cannot
    authenticate against or reach.
2.  `switchmap-ng` will keep track of the most recently used credentials
    to successfully obtain data and will use these credentials first.

| Parameter| Description |
| --------- | -----------|
| `snmp_groups:` | YAML key describing groups of SNMP authentication parameter. All parameter groups are listed under this key.|
| `group_name:` | Descriptive name for the group|
| `snmp_version:` | SNMP version. Must be present even if blank. Only SNMP versions 2 and 3 are supported by the project.|
| `snmp_secname:` | SNMP security name (SNMP version 3 only). Must be present even if blank.|
| `snmp_community:` | SNMP community (SNMP version 2 only). Must be present even if blank.|
| `snmp_authprotocol:` | SNMP AuthPassword (SNMP version 3 only). Must be present even if blank.|
| `snmp_authpassword:` | SNMP PrivProtocol (SNMP version 3 only). Must be present even if blank.|
| `snmp_privprotocol:` | SNMP PrivProtocol (SNMP version 3 only). Must be present even if blank.|
| `snmp_privpassword:` | SNMP PrivPassword (SNMP version 3 only). Must be present even if blank.|
| `snmp_port:` | SNMP UDP port|
