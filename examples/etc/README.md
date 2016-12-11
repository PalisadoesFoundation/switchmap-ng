# infoset Configuration Details

This page has detailed information on how to configure `infoset`. It includes examples for:

1. The main `_infosetd` server agent
2. Linux agents
3. SNMP agents

[TOC]

## infoset Configuration Samples

The `examples/configuration` directory includes a sample files that can be edited. `infoset` assumes all files in this directory, or any other specified configuration directory, only contains `infoset` configuration files. Most user will only need to edit the three files supplied.

You must place your configuration file in the `etc/` directory as your permanent configuration file location.
## Server Configuration

```
server:
    ingest_cache_directory: /opt/infoset/cache/ingest
    ingest_threads: 20
    bind_port: 6000
    db_hostname: localhost
    db_username: infoset
    db_password: wt8LVA7J5CNWPf75
    db_name: infoset
```
|Parameter|Description|
| --- | --- |
| server: | YAML key describing the server configuration.|
| ingest_cache_directory: | Location where the agent data ingester will store its data in the event it cannot communicate with either the database or the server's API|
| ingest_threads: | The maximum number of threads used to ingest data into the database|
| bind_port: | The TCP port the API will be listening on|
| db_hostname: | The hostname or IP address of the database server.|
| db_username: | The database username|
| db_password: | The database password|
| db_name: | The name of the database|

## Shared Configuration
There is some information that both the server and agents need to share. This is covered in the `common` section of the configuration.
```
common:
    log_file: /opt/infoset/logs/infoset.log
```
|Parameter|Description|
| --- | --- |
| common: | YAML key describing the shared server / agent configuration.|
| log_file: | The name of the log file `infoset` uses|

## Agent Configuration
An `infoset` agent processes data in the background.

### Sample Agent Configuration
In this example the `infoset` ingester agent named `ingestd` is configured:
```
agents:
	...
    ...
    ...
    - agent_name: ingestd
      agent_enabled: True
      agent_filename: bin/ingestd.py
      monitor_agent_pid: True
```
|Parameter|Description|
| --- | --- |
| agents: | YAML key describing configured agents. All agents are listed under this key.|
| agent_name: | Name of the agent (Don't change)|
| agent_enabled: | True if enabled|
| agent_filename: | Name of the agent's filename (Don't change)|
| monitor_agent_pid: | Set to True if the agent monitor needs to monitor the PID file to determine whether the ingester has hung|
