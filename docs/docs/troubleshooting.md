---
title: Troubleshooting
sidebar_label: Troubleshooting
sidebar_position: 8
---
# Troubleshooting

Here\'s how you can test your installation of `switchmap-ng`.

## Testing Operation After Installation

There are a number of steps to take to make sure you have installed
`switchmap-ng` correctly. This section explains how to do basic testing
before putting `switchmap-ng` into production.

### Start the API Interactively

Start the `switchmap-ng` API interactively.

``` bash
(venv) $ bin/switchmap_dashboard --start
```

### Start the Poller Interactively

The poller will need to be running prior to testing.

``` bash
(venv) $ bin/switchmap_poller --start
```

### Testing Polling

You can test your SNMP configuration and connectivity to your devices
using the `switchmap_poller_test.py` utility like this:

``` bash
(venv) $ bin/tools/switchmap_poller_test.py --hostname HOSTNAME
```

If you have setup switchmap-ng as a system daemon with a
`daemon_directory:` value `/var/run` you will need to specify the `venv`
path to `python3` first.

``` bash
(venv) $ sudo venv/bin/python3 bin/tools/switchmap_poller_test.py --hostname HOSTNAME
```

If successful it will print the entire contents of the polled data on
the screen.

### Test API Functionality

Testing the API is easy. Just visit the following URL:

    http://hostname/switchmap

A sample system startup script can be found in the
`examples/linux/systemd/switchmap_poller.service` file. Follow the
instructions in the file to make changes to the startup operation of the
`poller` daemon.

**Note:** There will be no visible output when the `poller` is running.
The `poller` logs its status to the `log/switchmap.log` file by default.
You will be able to see this interaction dynamically by running the
following command:

```bash
$ tail -f etc/switchmap.log
```
## Troubleshooting Using System Logs

There are different log files to check.

### Troubleshooting the API

There will be no visible output when the `API` is running. The `API`
logs its status to the `log/switchmap_dashboard.log` file by default.
You will be able to see this interaction dynamically by running the
following command:

```bash
$ tail -f etc/switchmap_dashboard.log
```
### Troubleshooting the Poller

There will be no visible output when the `Poller` is running. The
`Poller` logs its status to the `log/switchmap.log` file by default. You
will be able to see this interaction dynamically by running the
following command:

```bash
$ tail -f etc/switchmap.log
```
