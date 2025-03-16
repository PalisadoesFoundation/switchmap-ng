<a id="agent"></a>

# agent

Module to manage Agent classes.

Description:

    This module:
        1) Processes a variety of information from agents
        2) Posts the data using HTTP to a server listed
           in the configuration file

<a id="agent.Agent"></a>

## Agent Objects

```python
class Agent()
```

Agent class for daemons.

<a id="agent.Agent.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent, child=None, config=None)
```

Initialize the class.

**Arguments**:

- `parent` - Name of parent daemon
- `child` - Name of child daemon
- `config` - ConfigCore object
  

**Returns**:

  None

<a id="agent.Agent.name"></a>

#### name

```python
def name()
```

Return agent name.

**Arguments**:

  None
  

**Returns**:

- `value` - Name of agent

<a id="agent.Agent.query"></a>

#### query

```python
def query()
```

Create placeholder method. Do not delete.

**Arguments**:

  None

**Returns**:

  None

<a id="agent._AgentRun"></a>

## \_AgentRun Objects

```python
class _AgentRun()
```

Class that defines basic run function for AgentDaemons.

<a id="agent._AgentRun.__init__"></a>

#### \_\_init\_\_

```python
def __init__(agent)
```

Initialize the class.

**Arguments**:

- `agent` - agent object
  

**Returns**:

  None

<a id="agent._AgentRun.run"></a>

#### run

```python
def run()
```

Start Polling.

**Arguments**:

  None
  

**Returns**:

  None

<a id="agent.AgentDaemon"></a>

## AgentDaemon Objects

```python
class AgentDaemon(_AgentRun, Daemon)
```

Class that manages base agent daemonization.

<a id="agent.AgentDaemon.__init__"></a>

#### \_\_init\_\_

```python
def __init__(agent)
```

Initialize the class.

**Arguments**:

- `agent` - agent object
  

**Returns**:

  None

<a id="agent.GracefulAgentDaemon"></a>

## GracefulAgentDaemon Objects

```python
class GracefulAgentDaemon(_AgentRun, GracefulDaemon)
```

Class that manages graceful agent daemonization.

<a id="agent.GracefulAgentDaemon.__init__"></a>

#### \_\_init\_\_

```python
def __init__(agent, timeout=30)
```

Initialize the class.

**Arguments**:

- `agent` - agent object
- `timeout` - agent timeout
  

**Returns**:

  None

<a id="agent.AgentCLI"></a>

## AgentCLI Objects

```python
class AgentCLI()
```

Class that manages the agent CLI.

**Arguments**:

  None
  

**Returns**:

  None

<a id="agent.AgentCLI.__init__"></a>

#### \_\_init\_\_

```python
def __init__(graceful=False)
```

Initialize the class.

**Arguments**:

- `graceful` - True if graceful restart is required
  

**Returns**:

  None

<a id="agent.AgentCLI.process"></a>

#### process

```python
def process(additional_help=None)
```

Return all the CLI options.

**Arguments**:

- `additional_help` - CLI additional help string for argparse
  

**Returns**:

- `args` - Namespace() containing all of our CLI arguments as objects
  - filename: Path to the configuration file

<a id="agent.AgentCLI.control"></a>

#### control

```python
def control(agent, timeout=60)
```

Control the agent from the CLI.

**Arguments**:

- `agent` - Agent object
- `timeout` - Agent timeout
  

**Returns**:

  None

<a id="agent.AgentAPI"></a>

## AgentAPI Objects

```python
class AgentAPI(Agent)
```

Applcication API agent that serves web pages.

**Arguments**:

  None
  

**Returns**:

  None

<a id="agent.AgentAPI.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent, child, app, config=None)
```

Initialize the class.

**Arguments**:

- `parent` - Name of parent daemon
- `child` - Name of child daemon
- `app` - Flask App
- `config` - ConfigCore object
  

**Returns**:

  None

<a id="agent.AgentAPI.query"></a>

#### query

```python
def query()
```

Query all remote targets for data.

**Arguments**:

  None
  

**Returns**:

  None

<a id="agent._StandaloneApplication"></a>

## \_StandaloneApplication Objects

```python
class _StandaloneApplication(BaseApplication)
```

Class to integrate the Gunicorn WSGI with the Flask application.

Modified from: http://docs.gunicorn.org/en/latest/custom.html

<a id="agent._StandaloneApplication.__init__"></a>

#### \_\_init\_\_

```python
def __init__(app, parent, options=None)
```

Initialize the class.

**Arguments**:

- `app` - Flask application object of type Flask(__name__)
- `parent` - Name of parent process that is invoking the API
- `options` - Gunicorn CLI options

**Returns**:

  None

<a id="agent._StandaloneApplication.load_config"></a>

#### load\_config

```python
def load_config()
```

Load the configuration.

**Arguments**:

  None

**Returns**:

  None

<a id="agent._StandaloneApplication.load"></a>

#### load

```python
def load()
```

Run the Flask application throught the Gunicorn WSGI.

**Arguments**:

  None
  

**Returns**:

- `self.application` - Flask application object

<a id="configuration"></a>

# configuration

switchmap classes that manage various configurations.

<a id="configuration._Config"></a>

## \_Config Objects

```python
class _Config()
```

Class gathers all configuration information.

<a id="configuration._Config.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Intialize the class.

**Arguments**:

  None
  

**Returns**:

  None

<a id="configuration.ConfigCore"></a>

## ConfigCore Objects

```python
class ConfigCore(_Config)
```

Class gathers all configuration information.

<a id="configuration.ConfigCore.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Intialize the class.

**Arguments**:

  None
  

**Returns**:

  None

<a id="configuration.ConfigCore.agent_subprocesses"></a>

#### agent\_subprocesses

```python
def agent_subprocesses()
```

Get agent_subprocesses.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigCore.api_log_file"></a>

#### api\_log\_file

```python
def api_log_file(daemon)
```

Get api_log_file.

**Arguments**:

- `daemon` - Name of API daemon
  

**Returns**:

- `result` - result

<a id="configuration.ConfigCore.daemon_directory"></a>

#### daemon\_directory

```python
def daemon_directory()
```

Determine the daemon_directory.

**Arguments**:

  None
  

**Returns**:

- `result` - daemon_directory

<a id="configuration.ConfigCore.log_directory"></a>

#### log\_directory

```python
def log_directory()
```

Determine the log_directory.

**Arguments**:

  None
  

**Returns**:

- `result` - configured log_directory

<a id="configuration.ConfigCore.log_file"></a>

#### log\_file

```python
def log_file()
```

Get log_file.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigCore.log_level"></a>

#### log\_level

```python
def log_level()
```

Get log_level.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigCore.multiprocessing"></a>

#### multiprocessing

```python
def multiprocessing()
```

Get multiprocessing.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigCore.system_directory"></a>

#### system\_directory

```python
def system_directory()
```

Determine the system_directory.

**Arguments**:

  None
  

**Returns**:

- `result` - configured system_directory

<a id="configuration.ConfigAPIClient"></a>

## ConfigAPIClient Objects

```python
class ConfigAPIClient(ConfigCore)
```

Class gathers all configuration information.

<a id="configuration.ConfigAPIClient.__init__"></a>

#### \_\_init\_\_

```python
def __init__(section)
```

Intialize the class.

**Arguments**:

- `section` - Section of the config file to read
  

**Returns**:

  None

<a id="configuration.ConfigAPIClient.server_address"></a>

#### server\_address

```python
def server_address()
```

Get server_address.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigAPIClient.server_bind_port"></a>

#### server\_bind\_port

```python
def server_bind_port()
```

Get server_bind_port.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigAPIClient.server_https"></a>

#### server\_https

```python
def server_https()
```

Get server_https.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigAPIClient.server_password"></a>

#### server\_password

```python
def server_password()
```

Get server_password.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigAPIClient.server_username"></a>

#### server\_username

```python
def server_username()
```

Get server_username.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigAPIClient.server_url_root"></a>

#### server\_url\_root

```python
def server_url_root()
```

Return server_url_root value.

**Arguments**:

  None
  

**Returns**:

- `result` - server_url_root value

<a id="configuration.ConfigAPI"></a>

## ConfigAPI Objects

```python
class ConfigAPI(ConfigCore)
```

Class gathers all configuration information.

<a id="configuration.ConfigAPI.__init__"></a>

#### \_\_init\_\_

```python
def __init__(section)
```

Intialize the class.

**Arguments**:

- `section` - Section of the config file to read
  

**Returns**:

  None

<a id="configuration.ConfigAPI.api_bind_port"></a>

#### api\_bind\_port

```python
def api_bind_port()
```

Get api_bind_port.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigAPI.api_listen_address"></a>

#### api\_listen\_address

```python
def api_listen_address()
```

Get api_listen_address.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigAPI.api_https"></a>

#### api\_https

```python
def api_https()
```

Get api_https.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigAPI.api_password"></a>

#### api\_password

```python
def api_password()
```

Get api_password.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigAPI.api_username"></a>

#### api\_username

```python
def api_username()
```

Get api_username.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigAPI.api_url_root"></a>

#### api\_url\_root

```python
def api_url_root()
```

Return api_url_root value.

**Arguments**:

  None
  

**Returns**:

- `result` - api_url_root value

<a id="log"></a>

# log

Logging module.

<a id="log.ExceptionWrapper"></a>

## ExceptionWrapper Objects

```python
class ExceptionWrapper()
```

Class to handle unexpected exceptions with multiprocessing.

Based on:
    https://stackoverflow.com/questions/6126007/python-getting-a-traceback-from-a-multiprocessing-process

    _NOTE_ The subprocess needs to return a value for this to work.
    Returning an implicit "None" isn't sufficient

<a id="log.ExceptionWrapper.__init__"></a>

#### \_\_init\_\_

```python
def __init__(error_exception)
```

Initialize the class.

**Arguments**:

- `error_exception` - Exception object
  

**Returns**:

  None

<a id="log.ExceptionWrapper.re_raise"></a>

#### re\_raise

```python
def re_raise()
```

Extend the re_raise method.

**Arguments**:

  None
  

**Returns**:

  None

<a id="log._GetLog"></a>

## \_GetLog Objects

```python
class _GetLog()
```

Class to manage the logging without duplicates.

<a id="log._GetLog.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Initialize the class.

**Arguments**:

  None
  

**Returns**:

  None

<a id="log._GetLog.logfile"></a>

#### logfile

```python
def logfile()
```

Return logger for file IO.

**Arguments**:

  None
  

**Returns**:

- `value` - Value of logger

<a id="log._GetLog.stdout"></a>

#### stdout

```python
def stdout()
```

Return logger for terminal IO.

**Arguments**:

  None
  

**Returns**:

- `value` - Value of logger

<a id="log.log2console"></a>

#### log2console

```python
def log2console(code, message)
```

Log message to STDOUT only and die.

**Arguments**:

- `code` - Message code
- `message` - Message text
  

**Returns**:

  None

<a id="log.log2die_safe"></a>

#### log2die\_safe

```python
def log2die_safe(code, message)
```

Log message to STDOUT only and die.

**Arguments**:

- `code` - Message code
- `message` - Message text
  

**Returns**:

  None

<a id="log.log2warning"></a>

#### log2warning

```python
def log2warning(code, message)
```

Log warning message to file only, but don't die.

**Arguments**:

- `code` - Message code
- `message` - Message text
  

**Returns**:

  None

<a id="log.log2debug"></a>

#### log2debug

```python
def log2debug(code, message)
```

Log debug message to file only, but don't die.

**Arguments**:

- `code` - Message code
- `message` - Message text
  

**Returns**:

  None

<a id="log.log2info"></a>

#### log2info

```python
def log2info(code, message)
```

Log status message to file only, but don't die.

**Arguments**:

- `code` - Message code
- `message` - Message text
  

**Returns**:

  None

<a id="log.log2see"></a>

#### log2see

```python
def log2see(code, message)
```

Log message to file and STDOUT, but don't die.

**Arguments**:

- `code` - Message code
- `message` - Message text
  

**Returns**:

  None

<a id="log.log2die"></a>

#### log2die

```python
def log2die(code, message)
```

Log to STDOUT and file, then die.

**Arguments**:

- `code` - Error number
- `message` - Descriptive error string
  

**Returns**:

  None

<a id="log.log2exception_die"></a>

#### log2exception\_die

```python
def log2exception_die(code, sys_exc_info, message=None)
```

Log trace message to file and STDOUT, but don't die.

**Arguments**:

- `code` - Message code
- `sys_exc_info` - Tuple from exception from sys.exc_info
- `message` - Descriptive error string
  

**Returns**:

  None

<a id="log.log2exception"></a>

#### log2exception

```python
def log2exception(code, sys_exc_info, message=None, die=False)
```

Log trace message to file and STDOUT, but don't die.

**Arguments**:

- `code` - Message code
- `sys_exc_info` - Tuple from exception from sys.exc_info
- `message` - Message to log
- `die` - Die if True
  

**Returns**:

  None

<a id="log.check_environment"></a>

#### check\_environment

```python
def check_environment()
```

Check environmental variables. Die if incorrect.

**Arguments**:

  None
  

**Returns**:

- `path` - Path to the configurtion directory

<a id="log.root_directory"></a>

#### root\_directory

```python
def root_directory()
```

Determine the root directory in which switchmap is installed.

**Arguments**:

  None
  

**Returns**:

- `result` - Root directory

<a id="graphene"></a>

# graphene

Module with graphene functions.

<a id="graphene.normalize"></a>

#### normalize

```python
def normalize(data)
```

Remove all 'edges' and 'node' keys from graphene results.

**Arguments**:

- `data` - Dict of graphene results
  

**Returns**:

- `result` - Dict withoug 'edges' and 'node' keys

<a id="graphene.nodes"></a>

#### nodes

```python
def nodes(_nodes)
```

Strip the 'node' key from a list of graphene nodes.

**Arguments**:

- `_nodes` - List of graphene node dicts
  

**Returns**:

- `result` - List without the 'node' key

<a id="daemon"></a>

# daemon

Generic linux daemon base class for python 3.x.

<a id="daemon.Daemon"></a>

## Daemon Objects

```python
class Daemon()
```

A generic daemon class.

Usage: subclass the daemon class and override the run() method.

Modified from http://www.jejik.com/files/examples/daemon3x.py

<a id="daemon.Daemon.__init__"></a>

#### \_\_init\_\_

```python
def __init__(agent)
```

Initialize the class.

**Arguments**:

- `agent` - Agent object
  

**Returns**:

  None

<a id="daemon.Daemon.delpid"></a>

#### delpid

```python
def delpid()
```

Delete the PID file.

**Arguments**:

  None
  

**Returns**:

  None

<a id="daemon.Daemon.delskip"></a>

#### delskip

```python
def delskip()
```

Delete the skip file.

**Arguments**:

  None
  

**Returns**:

  None

<a id="daemon.Daemon.dellock"></a>

#### dellock

```python
def dellock()
```

Delete the lock file.

**Arguments**:

  None
  

**Returns**:

  None

<a id="daemon.Daemon.start"></a>

#### start

```python
def start()
```

Start the daemon.

**Arguments**:

  None
  

**Returns**:

  None

<a id="daemon.Daemon.force"></a>

#### force

```python
def force()
```

Stop the daemon by deleting the lock file first.

**Arguments**:

  None
  

**Returns**:

  None

<a id="daemon.Daemon.stop"></a>

#### stop

```python
def stop()
```

Stop the daemon.

**Arguments**:

  None
  

**Returns**:

  None

<a id="daemon.Daemon.restart"></a>

#### restart

```python
def restart()
```

Restart the daemon.

**Arguments**:

  None
  

**Returns**:

  None

<a id="daemon.Daemon.status"></a>

#### status

```python
def status()
```

Get daemon status.

**Arguments**:

  None
  

**Returns**:

- `result` - True if the PID and PID file exists

<a id="daemon.Daemon.run"></a>

#### run

```python
def run()
```

Override this method when you subclass Daemon.

This method will be called after the process has been daemonized by
start() or restart(). The base implementation does nothing and should
be overridden in derived classes to add actual daemon functionality.

**Arguments**:

  None
  

**Returns**:

  None

<a id="daemon.GracefulDaemon"></a>

## GracefulDaemon Objects

```python
class GracefulDaemon(Daemon)
```

Daemon that allows for graceful shutdown.

This daemon should allow for stop/restart commands to perform graceful
shutdown of a given process. A graceful shutdown involves checking that
whether a current process is running and only ending the process once the
current process has completed its currently running task.

<a id="daemon.GracefulDaemon.__init__"></a>

#### \_\_init\_\_

```python
def __init__(agent, timeout=30)
```

Initialize the class.

**Arguments**:

- `agent` - Agent object
- `timeout` - Timeout for graceful shutdown
  

**Returns**:

  None

<a id="daemon.GracefulDaemon.graceful_shutdown"></a>

#### graceful\_shutdown

```python
def graceful_shutdown(callback)
```

Initializes the wrapper with the callback function `fn`.

**Arguments**:

- `callback` - callback method
  

**Returns**:

- `wrapper` - Wrapper function

<a id="daemon.GracefulDaemon.stop"></a>

#### stop

```python
def stop()
```

Stop the daemon gracefully.

Uses parent class stop method after checking that daemon is no longer
processing data or making use of a resource.

**Arguments**:

  None
  

**Returns**:

  None

<a id="daemon.GracefulDaemon.restart"></a>

#### restart

```python
def restart()
```

Restarts the daemon gracefully.

Uses parent class restart method after checking that daemon is not
processing data or making use of a resource.

**Arguments**:

  None
  

**Returns**:

  None

<a id="data"></a>

# data

Module for data handling.

<a id="data.hashstring"></a>

#### hashstring

```python
def hashstring(string, sha=256, utf8=False)
```

Create a UTF encoded SHA hash string.

**Arguments**:

- `string` - String to hash
- `sha` - Length of SHA hash
- `utf8` - Return utf8 encoded string if true
  

**Returns**:

- `result` - Result of hash

<a id="data.dictify"></a>

#### dictify

```python
def dictify(data)
```

Convert NamedTuple to dict.

**Arguments**:

- `data` - NamedTuple
  

**Returns**:

- `result` - Dict representation of object

<a id="general"></a>

# general

Module with general purpose functions.

<a id="general.check_user"></a>

#### check\_user

```python
def check_user(config)
```

Check to make sure the user environment is correct.

**Arguments**:

- `config` - Config object
  

**Returns**:

  None

<a id="general.check_sudo"></a>

#### check\_sudo

```python
def check_sudo()
```

Check user isn't running as sudo.

**Arguments**:

  None
  

**Returns**:

  None

<a id="general.cleanstring"></a>

#### cleanstring

```python
def cleanstring(data)
```

Remove multiple whitespaces and linefeeds from string.

**Arguments**:

- `data` - String to process
  

**Returns**:

- `result` - Stipped data

<a id="general.octetstr_2_string"></a>

#### octetstr\_2\_string

```python
def octetstr_2_string(bytes_string)
```

Convert SNMP OCTETSTR to string.

**Arguments**:

- `bytes_string` - Binary value to convert
  

**Returns**:

- `result` - String equivalent of bytes_string

<a id="general.random_hash"></a>

#### random\_hash

```python
def random_hash()
```

Create a random Hex hash.

**Arguments**:

  None
  

**Returns**:

- `result` - Hex hash

<a id="general.mac"></a>

#### mac

```python
def mac(_mac)
```

Convert MAC address to a standardized format.

**Arguments**:

- `_mac` - MAC address
  

**Returns**:

- `result` - MacAddress object

<a id="general.root_directory"></a>

#### root\_directory

```python
def root_directory()
```

Determine the root directory in which switchmap is installed.

**Arguments**:

  None
  

**Returns**:

- `result` - Root directory

<a id="general.ipaddress"></a>

#### ipaddress

```python
def ipaddress(_ip)
```

Validate an IP address.

**Arguments**:

- `_ip` - IP address
  

**Returns**:

- `result` - IP Object

<a id="general.make_bool"></a>

#### make\_bool

```python
def make_bool(result)
```

Create a boolean version of the argument.

**Arguments**:

- `result` - Object to transform
  

**Returns**:

- `result` - boolean

<a id="general.consistent_keys"></a>

#### consistent\_keys

```python
def consistent_keys(_data)
```

Convert dict keys to ints if possible.

**Arguments**:

- `_data` - Multidimensional dict
  

**Returns**:

- `result` - dict

<a id="general.group_consecutive"></a>

#### group\_consecutive

```python
def group_consecutive(data)
```

Group consecutive numbers in a list.

https://stackoverflow.com/questions/2154249/
identify-groups-of-consecutive-numbers-in-a-list

**Arguments**:

- `data` - list
  

**Returns**:

- `ranges` - List of lists

<a id="general.human_readable"></a>

#### human\_readable

```python
def human_readable(num, suffix="B", storage=False)
```

Convert number to human readable value.

https://stackoverflow.com/questions/1094841/
get-human-readable-version-of-file-size

**Arguments**:

- `num` - Number to convert
- `suffix` - The suffix for the human readable output
- `storage` - Use binary 1024 for evaluating storage
  otherwise use regular decimal.
  

**Returns**:

- `result` - Numeric string

<a id="general.padded_list_of_lists"></a>

#### padded\_list\_of\_lists

```python
def padded_list_of_lists(data, width=4, pad=None)
```

Create a padded list of list.

**Arguments**:

- `data` - List to process
- `width` - Width of the list of lists
- `pad` - Value to pad the last row of the list of lists with
  

**Returns**:

- `result` - list of lists

<a id="rest"></a>

# rest

Functions for creating URIs.

<a id="rest.post"></a>

#### post

```python
def post(uri, data, config, server=True)
```

Create URI for datacenter RRD and oid_id data.

**Arguments**:

- `uri` - URI for posting
- `data` - Data to post
- `config` - ConfitAPIClient object
- `server` - Posting to a server if True, API if False
  

**Returns**:

- `data` - Post named tuple

<a id="rest.get"></a>

#### get

```python
def get(uri, config, server=True, die=True)
```

Get data fro URI from API server.

**Arguments**:

- `uri` - URI for posting
- `config` - ConfigAPIClient object
- `server` - True if getting data from an database API server
- `die` - Die if the connection fails if True
  

**Returns**:

- `success` - True if successful

<a id="rest.get_graphql"></a>

#### get\_graphql

```python
def get_graphql(query, config, die=True)
```

Get data fro URI from API server.

**Arguments**:

- `query` - Query string from GraphQL server
- `config` - ConfigAPIClient object
- `die` - Die if the connection fails if True
  

**Returns**:

- `success` - True if successful

<a id="files"></a>

# files

Switchmap files library.

<a id="files._Directory"></a>

## \_Directory Objects

```python
class _Directory()
```

A class for creating the names of system directories.

<a id="files._Directory.__init__"></a>

#### \_\_init\_\_

```python
def __init__(config)
```

Initialize the class.

**Arguments**:

- `config` - Config object
  

**Returns**:

  None

<a id="files._Directory.pid"></a>

#### pid

```python
def pid()
```

Define the system pid directory.

**Arguments**:

  None
  

**Returns**:

- `value` - pid directory

<a id="files._Directory.lock"></a>

#### lock

```python
def lock()
```

Define the system lock directory.

**Arguments**:

  None
  

**Returns**:

- `value` - lock directory

<a id="files._Directory.snmp"></a>

#### snmp

```python
def snmp()
```

Define the system snmp directory.

**Arguments**:

  None
  

**Returns**:

- `value` - snmp directory

<a id="files._File"></a>

## \_File Objects

```python
class _File()
```

A class for creating the names of system files.

<a id="files._File.__init__"></a>

#### \_\_init\_\_

```python
def __init__(config)
```

Initialize the class.

**Arguments**:

- `config` - Config object
  

**Returns**:

  None

<a id="files._File.pid"></a>

#### pid

```python
def pid(prefix)
```

Define the pid file.

**Arguments**:

- `prefix` - Prefix of file
  

**Returns**:

- `value` - pid directory

<a id="files._File.lock"></a>

#### lock

```python
def lock(prefix)
```

Define the lock file.

**Arguments**:

- `prefix` - Prefix of file
  

**Returns**:

- `value` - lock directory

<a id="files._File.skip"></a>

#### skip

```python
def skip(prefix)
```

Define the skip file.

**Arguments**:

- `prefix` - Prefix of file
  

**Returns**:

- `value` - skip directory

<a id="files._File.snmp"></a>

#### snmp

```python
def snmp(prefix, create=True)
```

Define the system snmp directory.

**Arguments**:

- `prefix` - Prefix of file
- `create` - Create file if True
  

**Returns**:

- `value` - snmp directory

<a id="files.move_yaml_files"></a>

#### move\_yaml\_files

```python
def move_yaml_files(src, dst)
```

Move all yaml files from source to destination directory.

**Arguments**:

- `src` - Source directory
- `dst` - Destination directory
  

**Returns**:

  None

<a id="files.read_yaml_files"></a>

#### read\_yaml\_files

```python
def read_yaml_files(directories)
```

Read the contents of all yaml files in a directory.

**Arguments**:

- `directories` - List of directory names with configuration files
  

**Returns**:

- `config_dict` - Dict of yaml read

<a id="files.read_yaml_file"></a>

#### read\_yaml\_file

```python
def read_yaml_file(filepath, as_string=False, die=True)
```

Read the contents of a YAML file.

**Arguments**:

- `filepath` - Path to file to be read
- `as_string` - Return a string if True
- `die` - Die if there is an error
  

**Returns**:

- `result` - Dict of yaml read

<a id="files.mkdir"></a>

#### mkdir

```python
def mkdir(directory)
```

Create a directory if it doesn't already exist.

**Arguments**:

- `directory` - Directory name
  

**Returns**:

  None

<a id="files.pid_file"></a>

#### pid\_file

```python
def pid_file(agent_name, config)
```

Get the pidfile for an agent.

**Arguments**:

- `agent_name` - Agent name
- `config` - Config object
  

**Returns**:

- `result` - Name of pid file

<a id="files.lock_file"></a>

#### lock\_file

```python
def lock_file(agent_name, config)
```

Get the lockfile for an agent.

**Arguments**:

- `agent_name` - Agent name
- `config` - Config object
  

**Returns**:

- `result` - Name of lock file

<a id="files.skip_file"></a>

#### skip\_file

```python
def skip_file(agent_name, config)
```

Get the skip file for an agent.

**Arguments**:

- `agent_name` - Agent name
- `config` - Config object
  

**Returns**:

- `result` - Name of skip file

<a id="files.snmp_file"></a>

#### snmp\_file

```python
def snmp_file(hostname, config)
```

Get the snmpfile for an agent.

**Arguments**:

- `hostname` - hostname
- `config` - Config object
  

**Returns**:

- `result` - Name of snmp file

<a id="files.execute"></a>

#### execute

```python
def execute(command, die=True)
```

Run the command UNIX CLI command and record output.

**Arguments**:

- `command` - CLI command to execute
- `die` - Die if errors found
  

**Returns**:

- `returncode` - Return code of command execution

<a id="files.config_filepath"></a>

#### config\_filepath

```python
def config_filepath()
```

Get the configuration filename.

**Arguments**:

  None
  

**Returns**:

- `result` - Filename

<a id="variables"></a>

# variables

Module for classes that format variables.

<a id="variables.AgentAPIVariable"></a>

## AgentAPIVariable Objects

```python
class AgentAPIVariable()
```

Variable representation for data required by the AgentAPI.

<a id="variables.AgentAPIVariable.__init__"></a>

#### \_\_init\_\_

```python
def __init__(ip_bind_port=20201, ip_listen_address="0.0.0.0")
```

Initialize the class.

**Arguments**:

- `ip_bind_port` - ip_bind_port
- `ip_listen_address` - TCP/IP address on which the API is listening.
  

**Returns**:

  None

<a id="variables.AgentAPIVariable.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__()
```

Return a representation of the attributes of the class.

**Arguments**:

  None
  

**Returns**:

- `result` - String representation.

<a id="__init__"></a>

# \_\_init\_\_

Define the switchmap.core package.

**Arguments**:

  None
  

**Returns**:

  None

