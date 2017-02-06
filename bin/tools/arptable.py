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


def main():
    """Initialize the class.

    Args:
        config: Configuration object
        host: Hostname to process

    Returns:
        None

    """
    # Initialize key variables
    config = configuration.Config()
    topology_directory = config.topology_directory()
    arp_directory = config.arp_directory()
    arp_table = defaultdict(lambda: defaultdict(dict))
    rarp_table = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    rarp_device_table = defaultdict(
        lambda: defaultdict(lambda: defaultdict(dict)))

    # Cycle through list of files in directory
    for filename in os.listdir(topology_directory):
        # Examine all the '.yaml' files in directory
        if filename.endswith('.yaml'):
            # Read file and add to string
            file_path = ('%s/%s') % (topology_directory, filename)
            try:
                with open(file_path, 'r') as file_handle:
                    yaml_from_file = file_handle.read()
            except:
                log_message = (
                    'Error reading file %s. Check permissions, '
                    'existence and file syntax.'
                    '') % (file_path)
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
                                    arp_table[
                                        ip_address]['hostname'] = ip_results[0]
                            except:
                                arp_table[ip_address]['hostname'] = None

                            # Populate RARP table
                            if bool(rarp_table[mac_address]) is True:
                                # Only append unique entries
                                if ip_address not in rarp_table[mac_address]:
                                    rarp_table[mac_address].append(ip_address)
                            else:
                                rarp_table[mac_address] = [ip_address]

            # Populate RARP table
            if 'layer1' in device_dict:
                layer1_dict = device_dict['layer1']
                for ifindex, port_dict in layer1_dict.items():
                    # Only interested in Ethernet ports
                    if bool(port_dict['jm_ethernet']) is False:
                        continue

                    # We are not interested in populating trunk port MAC data
                    if bool(port_dict['jm_trunk']) is True:
                        continue

                    if ('jm_macs' in port_dict) and (
                            bool(port_dict['jm_macs']) is True):
                        # Create an ifIndex and device entry
                        # for each rarp entry
                        for mac_address in port_dict['jm_macs']:
                            device_name = device_dict['misc']['host']

                            for ip_address in rarp_table[mac_address]:
                                rarp_device_table[mac_address][device_name][
                                    ifindex] = ip_address

    # Output the file to the ARP file
    output_file = '{}/arpfile.yaml'.format(arp_directory)
    if bool(arp_table) is True:
        yaml_string = general.dict2yaml(arp_table)

        # Dump data
        with open(output_file, 'w') as file_handle:
            file_handle.write(yaml_string)

    # Output the file to the RARP file
    output_file = '{}/rarpfile.yaml'.format(arp_directory)
    if bool(rarp_table) is True:
        yaml_string = general.dict2yaml(rarp_table)

        # Dump data
        with open(output_file, 'w') as file_handle:
            file_handle.write(yaml_string)

    # Output the file to the RARP_DEVICE file
    output_file = '{}/rarp_device_file.yaml'.format(arp_directory)
    if bool(rarp_device_table) is True:
        yaml_string = general.dict2yaml(rarp_device_table)

        # Dump data
        with open(output_file, 'w') as file_handle:
            file_handle.write(yaml_string)

if __name__ == '__main__':
    # Run main
    main()
