# Poller Service 

- This is the Python component that polls network devices via SNMP v2/v3.  

## Key Files/Modules

- **switchmap/poller/poll.py**  
  - The main Poller orchestration module (daemon entry point).  
  - It loads the configuration (devices, SNMP credentials, polling interval) and kicks off the polling threads.  
  - It coordinates scheduling polls and ensuring results are passed to the update/transfer stage.

- **switchmap/poller/snmp/snmp_info.py**  
  - Implements the core SNMP polling logic.  
  - Defines which OIDs to fetch for each device (covering port status, VLANs, ARP table, etc.) and uses the EasySNMP library (which wraps Net-SNMP) to perform the queries.  
  - The Poller uses this module to retrieve raw SNMP values for all relevant MIB objects on a device.

- **switchmap/poller/snmp/iana_enterprise.py**  
  - Helps determine the device vendor by checking the IANA enterprise OID.  
  - The Poller uses this to select vendor-specific polling logic. For example, Cisco vs Juniper switches may require different MIBs for the same info.  
  - This module maps the device’s SNMP sysObjectID to a manufacturer/type, guiding which MIB handlers to invoke.

- **MIB-specific modules** (in `switchmap/poller/snmp/mib/*`):  
  - There are Python modules for various MIBs and vendor extensions (for instance, `generic/mib_bridge.py` for Spanning Tree vs ifIndex alignment, Cisco-specific MIB handlers, etc.).  
  - These modules encapsulate knowledge of how to get Layer1/2 data from particular devices.  
  - The Poller imports all supported MIB modules in `snmp/__init__.py` so it can iterate through them as needed.  
  - The `mib_bridge.py` (in the generic subfolder) is especially important as it merges data from different MIB sources to ensure consistent interface indexing.

- **switchmap/poller/update/device.py**  
  - The Poller’s data post-processing module.  
  - It takes the raw SNMP results (often a nested dict keyed by OIDs or interim IDs) and produces a cleaned, normalized structure.  
  - For each interface, it attaches high-level info (admin status, oper status, speed, duplex, VLAN membership, neighbor info, etc.) to prepare a complete snapshot of the device.  
  - This module essentially translates low-level SNMP results into the Switchmap “object model” that the rest of the system uses.  
  - Finally, it serializes the device data to JSON (e.g. using Python’s json/yaml libraries) and hands it off to be sent to the API.

## Miscellaneous
- The Poller also uses config files (YAML) typically located in `etc/` for device lists and SNMP community strings.  
- It logs its activity to `switchmap-poller.log` by default.  
- The `bin/tools/switchmap_poller_test.py` script can be used to manually test polling of a single device.
