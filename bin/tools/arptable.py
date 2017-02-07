#!/usr/bin/env python3
"""Switchmap-NG  Script to create OUI YAML file.

Takes content of http://standards-oui.ieee.org/oui.txt and outputs it to YAML.

ARGV[1] must be the out.txt file

"""

# Standard imports
import sys
import yaml
import os
from collections import defaultdict
import socket
from copy import deepcopy
from pprint import pprint

# Try to create a working PYTHONPATH
script_directory = os.path.dirname(os.path.realpath(__file__))
bin_directory = os.path.abspath(os.path.join(script_directory, os.pardir))
root_directory = os.path.abspath(os.path.join(bin_directory, os.pardir))
if script_directory.endswith('/switchmap-ng/bin/tools') is True:
    sys.path.append(root_directory)
else:
    print(
        'This script is not installed in the "switchmap-ng/bin/tools" '
        'directory. Please fix.')
    sys.exit(2)

# Switchmap-NG standard imports
from switchmap.utils import log
from switchmap.utils import configuration
from switchmap.utils import general

from switchmap.topology import postpoll


def _create_search_files():
    """Creates YAML files used for Switchmap-NG search.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    config = configuration.Config()
    topology_directory = config.topology_directory()
    search_directory = config.search_directory()
    arp_table = defaultdict(lambda: defaultdict(dict))
    host_table = {}
    ifalias_table = defaultdict(lambda: defaultdict(dict))
    rarp_table = {}
    ifindex_table = defaultdict(
        lambda: defaultdict(lambda: defaultdict(dict)))

    # Create ARP and RARP table files
    # Cycle through list of files in directory
    for filename in os.listdir(topology_directory):
        # Examine all the '.yaml' files in directory
        if filename.endswith('.yaml'):
            # Read file and add to string
            filepath = config.topology_device_file(filename[0:-5])
            try:
                with open(filepath, 'r') as file_handle:
                    yaml_from_file = file_handle.read()
            except:
                log_message = (
                    'Error reading file %s. Check permissions, '
                    'existence and file syntax.'
                    '') % (filepath)
                log.log2die_safe(1065, log_message)

            device_dict = yaml.load(yaml_from_file)
            # Populate ARP table
            if 'layer3' in device_dict:
                keys = ['cInetNetToMediaPhysAddress', 'ipNetToMediaTable']
                for key in keys:
                    if key in device_dict['layer3']:
                        arp_dict = device_dict['layer3'][key]
                        for ip_address, mac_address in arp_dict.items():
                            # Populate ARP table
                            arp_table[ip_address]['mac_address'] = mac_address
                            try:
                                ip_results = socket.gethostbyaddr(ip_address)
                                if len(ip_results) > 1:
                                    hostname = ip_results[0]
                                    arp_table[
                                        ip_address]['hostname'] = hostname
                                    host_table[hostname] = ip_address

                            except:
                                arp_table[ip_address]['hostname'] = None

                            # Populate RARP table (Using ARP entries)
                            if mac_address in rarp_table:
                                # Only append unique entries
                                if ip_address not in rarp_table[mac_address]:
                                    rarp_table[mac_address].append(ip_address)
                            else:
                                rarp_table[mac_address] = [ip_address]

    # Create ifIndex file after creating complete ARP and RARP table files
    # Cycle through list of files in directory
    for filename in os.listdir(topology_directory):
        # Examine all the '.yaml' files in directory
        if filename.endswith('.yaml'):
            # Read file and add to string
            filepath = config.topology_device_file(filename[0:-5])
            try:
                with open(filepath, 'r') as file_handle:
                    yaml_from_file = file_handle.read()
            except:
                log_message = (
                    'Error reading file %s. Check permissions, '
                    'existence and file syntax.'
                    '') % (filepath)
                log.log2die_safe(1065, log_message)

            device_dict = yaml.load(yaml_from_file)

            # Get the device name
            device_name = device_dict['misc']['host']

            # Populate ifIndex table
            if 'layer1' in device_dict:
                layer1_dict = device_dict['layer1']
                # Process each port on device
                for ifindex, port_dict in layer1_dict.items():
                    # Only interested in Ethernet ports
                    if bool(port_dict['jm_ethernet']) is False:
                        continue

                    # We are not interested in populating trunk port MAC data
                    if bool(port_dict['jm_trunk']) is True:
                        continue

                    # Create ifalias entry
                    ifalias = port_dict['ifAlias'].strip()
                    if bool(ifalias) is True:
                        if ifalias not in ifalias_table:
                            ifalias_table[ifalias][device_name] = [ifindex]
                        else:
                            if device_name not in ifalias_table[ifalias]:
                                ifalias_table[ifalias][device_name] = [ifindex]
                            else:
                                ifalias_table[
                                    ifalias][device_name].append(ifindex)

                    # Process MAC addresses
                    if ('jm_macs' in port_dict) and (
                            bool(port_dict['jm_macs']) is True):

                        # Create an ifIndex and device entry
                        # for each RARP entry
                        for mac_address in port_dict['jm_macs']:
                            # Populate RARP table. Not all MACs have
                            # an associated ARP IP address (eg. multicast)
                            if mac_address not in rarp_table:
                                rarp_table[mac_address] = []

                            # Create ifindex entry
                            for ip_address in rarp_table[mac_address]:
                                if bool(ifindex_table[mac_address][
                                        device_name][ifindex]) is True:
                                    ifindex_table[mac_address][device_name][
                                        ifindex].append(ip_address)
                                else:
                                    ifindex_table[mac_address][device_name][
                                        ifindex] = [ip_address]

    # Create yaml files
    general.create_yaml_file(arp_table, config.arp_file())
    general.create_yaml_file(rarp_table, config.rarp_file())
    general.create_yaml_file(ifindex_table, config.ifindex_file())
    general.create_yaml_file(ifalias_table, config.ifalias_file())
    general.create_yaml_file(host_table, config.hosts_file())


def main():
    """Initialize the class.

    Args:
        None

    Returns:
        None

    """
    postpoll.all_devices()



if __name__ == '__main__':
    # Run main
    main()
