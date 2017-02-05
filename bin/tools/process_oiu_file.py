#!/usr/bin/env python3
"""Switchmap-NG  Script to create OUI YAML file.

Takes content of http://standards-oui.ieee.org/oui.txt and outputs it to YAML.

ARGV[1] must be the out.txt file

"""

# Standard imports
import sys
import re
import os
import csv

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
    input_filename = sys.argv[1]
    config = configuration.Config()
    mac_addresses = {}
    mac_hex_regex = (
        '[0-9a-fA-F][0-9a-fA-F]-[0-9a-fA-F][0-9a-fA-F]-[0-9a-fA-F][0-9a-fA-F]')
    regex = re.compile(
        r'^{}\s+.*?\(hex\)\s+.*?$'.format(mac_hex_regex))

    # Ingest file
    if os.path.isfile(input_filename) is False:
        log_message = 'Filename {} not found.'.format(input_filename)
        log.log2die(1000, log_message)
    if input_filename.endswith('oui.txt') is False:
        log_message = (
            'Filename {} is invalid. It must end with '
            '\'oui.txt\'.'.format(input_filename))
        log.log2die(1000, log_message)

    with open(input_filename) as f_handle:
        lines = f_handle.readlines()

    # Read data
    for line in lines:
        # Create dictionary of mac addresses
        if bool(regex.match(line)) is True:
            (field1, field2) = line.split('(hex)')
            mac_address = field1.strip().lower().replace('-', '')
            company = field2.strip().replace(':', ' ')
            mac_addresses[mac_address] = company

    # Output the file to the metadata directory
    output_file = config.mac_address_file()
    if bool(mac_addresses) is True:
        with open(output_file, 'w') as csvfile:
            spamwriter = csv.writer(
                csvfile, delimiter=':', quoting=csv.QUOTE_NONE)
            for key, value in sorted(mac_addresses.items()):
                spamwriter.writerow([key, value])


if __name__ == '__main__':
    # Run main
    main()
