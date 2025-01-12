---
title: Architecture
sidebar_label: Architecture
sidebar_position: 9
---
# Architecture

This page outlines the architecture and components of `switchmap-ng`

## Poller

This section explains how polling operates.

### How Devices are Polled

The following refers to files in the `switchmap.poller.snmp` folder:

1. Modules supporting all MIBs are imported from `__init__.py`.

2. The `iana_enterprise.py` module to determine the manufacturer which
    is then used in collating the data.

3. For each device OIDs in the MIBs are polled using `snmp_info.py`. OIDs not supported by the app are ignored.

    1. Some Layer 1 and Layer 2 data may be found using the
            `ifIndex` id (some Cisco devices), or that of the spanning
            tree port index. The
            `switchmap/poller/snmp/mib/generic/mib_bridge.py` determines
            which methodology is used by the device and returns values
            keyed by `ifIndex` for consistency.

4. This results in a `dict` with keys for Layer 1, Layer 2 and Layer 3 information in the [OSI model](https://en.wikipedia.org/wiki/OSI_model).

    1. The Layer 1 and Layer 2 information are keyed by `ifIndex`.

### Processing Polled OSI Model Data

The following refers to files in the `switchmap.poller.update` folder.

Different manufacturers use different MIBs to do the same thing. The
`device.py` module attempts to update the `dict` obtained from polled
data to create a uniform format suitable for updating the database.

1. Iterates through each Layer 1 interface by `ifIndex` number.

2. Extracts data to be more suitable for updating the database. This includes:

    1. VLAN (Some manufacturers assign them to the physical
    interface, others to a virtual subinterface.)
    2. Duplex
    3. Speed
    4. Trunk status

3. This data is then posted to the API in JSON format.

## Ingester

This section explains how database updates operate.

The posted polled data is stored on disk on the API server in YAML
format for ease of human readability. The ingester reads the datafiles
and processes them like this:

1. Network devices in the same routing or VLAN domain will often
    observe the same information such as IP and MAC addresses.

2. The ingester processes these and deduplicates the information before adding it to the database. This information is often needed before processing the interface information to help cross referencing.

    1. All IP address, MAC address and VLAN data in a particular
        Zone in the configuration file are processed first.
    2. The remaining information is then processed linking to the
        IP address, MAC address and VLAN database foreign keys
        previously created.

3. The update is done using the Python multiprocessing module for
    speed.
