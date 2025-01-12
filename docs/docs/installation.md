---
title: Installation
sidebar_position: 2
sidebar_label: Installation
---
# Installation

This section outlines how to install and do basic configuration of
`switchmap-ng`.

## Setup and Configure MySQL Database Server

`switchmap-ng` uses a MySQL database to store data. This section
outlines how to set it up.

### Install Database Packages

Install MySQL on a database server as outlined in the MySQL
documentation.

### Database Configuration

Create the database, and grant privileges to a switchmap user. In this
case both the database and the database user are named `switchmap`.

```bash
$ sudo mysql
```
```sql
CREATE DATABASE switchmap;
GRANT ALL PRIVILEGES ON switchmap.* TO 'switchmap'@'localhost' IDENTIFIED BY 'CHANGE_ME_NOW';
FLUSH PRIVILEGES;
EXIT;
```
## Install Prerequisite Supporting Operating System Packages

`switchmap-ng` has the following requirements:

-   python \>= 3.5
-   python3-pip

It will not work with lower versions.

### Ubuntu / Debian / Mint

The commands for installing the dependencies are:

```bash
$ sudo apt-get -y install python3 python3-pip snmp libsnmp-dev snmp-mibs-downloader gcc python-dev-is-python3 python3-venv
```

### Centos / Fedora

The commands for installing the dependencies are:

```bash
$ sudo dnf -y install python3 python3-pip net-snmp-utils net-snmp-devel gcc python-devel python3-virtualenv
```

## Install Switchmap-NG

Installation is simple. Follow these steps

### Clone the Repository

Now clone the repository and copy the sample configuration file to its
final location.

```bash
$ git clone https://github.com/PalisadoesFoundation/switchmap-ng
$ cd switchmap-ng
```

### Install Prerequisite Python Packages

To ensure that switchmap will be using only the versions of python
packages it requires, independent of any other python applications you
may have installed, even after a operating system upgrade, we use the
python `venv` system.

In short, venv makes `switchmap-ng` work in a more predictable way which
improves reliability and simplifies troubleshooting.

The following commands will:

1)  create a directory named `venv/` in the top most `switchmap-ng`
    directory.
2)  copy your systems python files there

Here are the commands:

```bash
$ cd /path/to/switchmap-ng
$ python3 -m venv venv
```

You will now need to activate the use of these copied python files by
`switchmap-ng`.

1)  This can be done using the `source` command referencing a script
    that will do the activation.
2)  Your command prompt will change to have a `(venv)` prefix

Here are the commands:

```bash
$ source venv/bin/activate
(venv) $ 
```

Now you can install the extra python packages using `pip3` referencing
the packages in the `requirements.txt` file

```bash
(venv) $ pip3 install -r requirements.txt
```

Remember to always be in `venv` mode when running `switchmap-ng` by
running the source command first. You only need to run the command once
per terminal session.

### Edit The Configuration File

Please read the `configuration` file
beforehand before proceeding.

Edit your configuration file with the appropriate configuration options.
Here are the steps using the `vim` editor:

```bash
(venv) $ cp examples/etc/config.yaml etc/config.yaml
(venv) $ vim etc/config.yaml
```

Make the required changes.

### Run Installation Script

You will now need to run the database installation script. This creates
the database tables and populates some of them with important data.

```bash
(venv) $ bin/tools/create_db_tables.py
```

## Testing Installation

There are a number of ways to test your installation. Please refer to
the `troubleshooting` guide for additional
details if these methods fail.

### Testing Polling

You can test your SNMP configuration and connectivity to your devices
using the `switchmap_poller_test.py` utility like this:

```bash
(venv) $ bin/tools/switchmap_poller_test.py --hostname HOSTNAME
```

If you have setup switchmap-ng as a system daemon with a
`daemon_directory:` value `/var/run` you will need to specify the `venv`
path to `python3` first.

```bash
(venv) $ sudo venv/bin/python3 bin/tools/switchmap_poller_test.py --hostname HOSTNAME
```

If successful it will print the entire contents of the polled data on
the screen.

### Testing the API Server

You can test whether the API is working by starting it on the device
designated to receiving polling information and storing it in the
database.

```bash
(venv) $ bin/systemd/switchmap_server --start
(venv) $ bin/systemd/switchmap_server --status
```

The result of the status check should look like this:

```
Daemon is running - <bound method Agent.name of <switchmap.core.agent.AgentAPI object at>>
Daemon is running - <bound method Agent.name of <switchmap.core.agent.Agent object at>>
```

### Testing the Web Dashboard

You can test whether the web dashboard API is working by

1)  Correctly configuring and starting the API server as shown above
2)  Starting the web dashboard as shown below.

```bash
(venv) $ bin/systemd/switchmap_dashboard --start
(venv) $ bin/systemd/switchmap_dashboard --status
```

The result of the status check should look like this:

```
Daemon is running - <bound method Agent.name of <switchmap.core.agent.AgentAPI object at>>
Daemon is running - <bound method Agent.name of <switchmap.core.agent.Agent object at>>
```

You can then visit the dashboard URL. (You will need to make adjustments
if you installed the application on a remote server):

    http://localhost:7001/switchmap/

The Webserver help page provides the necessary steps to view switchmap
on port 80 using Apache or Nginx

## Testing Setup for Developers

Follow the installation steps above to have the application ready, then
add these steps for developing code.

### Database Configuration

Create the `switchmap_unittest` database, and grant privileges to a
`switchmap_unittest` user with the password `switchmap_unittest`.

```bash
$ sudo mysql
``` 
```sql
CREATE DATABASE switchmap_unittest;
GRANT ALL PRIVILEGES ON switchmap_unittest.* TO 'switchmap_unittest'@'localhost' IDENTIFIED BY 'switchmap_unittest';
FLUSH PRIVILEGES;
EXIT;
```

### Setup the Test Config File

Create the testing configuration file which will be stored in a hidden
directory in `$HOME`

```
(venv) $ tests/bin/test_db_config_setup.py
```

### Run the Test Suite

You can run all the tests with this command.
```
(venv) $ tests/bin/_do_all_tests.py
```
An alternative method is to use pytest.
```
(venv) $ pytest tests/switchmap_
```
You can run individual tests with this command.
```
(venv) $ tests/switchmap_/path/to/test.py
```