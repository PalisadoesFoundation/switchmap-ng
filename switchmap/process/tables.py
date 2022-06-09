1171# Standard libraries
import os
from collections import defaultdict
import socket
from multiprocessing import Pool

from pprint import pprint
import sys

# switchmap.libraries
from switchmap.utils import log
from switchmap import CONFIG
from switchmap.utils import general


class SearchFiles(object):
    """Switchmap-NG class for managing search files."""

    def __init__(self):
        """Initialize the class.

        Args:
            hostname: Hostname to poll

        Returns:
            None

        """
        # Initialize key variables
        self._config = CONFIG
        topology_directory = self._config.topology_directory()
        self._filepaths = []

        # Cycle through list of files in directory
        for filename in os.listdir(topology_directory):
            # Examine all the '.yaml' files in directory
            if filename.endswith('.yaml'):
                # Read file
                device_name = filename[0:-5]
                filepath = self._config.topology_device_file(device_name)
                self._filepaths.append(filepath)
        self._filepaths.sort()

    def create(self):
        """Create YAML files used for Switchmap-NG search.

        Args:
            None

        Returns:
            None

        """
        # Send log message
        log_message = ('Starting search file creation.')
        log.log2info(1059, log_message)

        # Create files
        self._arp()
        self._rarp()
        self._interface()

        # Send log message
        log_message = ('Completed search file creation.')
        log.log2info(1055, log_message)

    def _arp(self):
        """Create ARP and host table YAML search files.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        arp_table = defaultdict(lambda: defaultdict(dict))
        host_table = {}

        # Get the number of threads to use in the pool
        threads_in_pool = self._config.agent_threads()

        # Create host, ARP table files
        # Cycle through list of files in directory
        for filepath in self._filepaths:
            # Read file
            device_dict = general.read_yaml_file(filepath)

            # Get the device name
            device_name = device_dict['misc']['host']

            # Send log message
            log_message = (
                'Getting ARP and host table for {}.'
                ''.format(device_name))
            log.log2debug(1171, log_message)

            # Populate ARP and RARP table
            if 'layer3' in device_dict:
                keys = ['cInetNetToMediaPhysAddress', 'ipNetToMediaTable']
                for key in keys:
                    if key in device_dict['layer3']:
                        arp_dict = device_dict['layer3'][key]

                        for ip_address, mac_addr in arp_dict.items():
                            # Skip if IP address is already in table
                            if ip_address in arp_table:
                                continue
                            # Populate ARP table
                            arp_table[ip_address]['mac_address'] = mac_addr

            # Send log message
            log_message = (
                'Completed ARP and host table for {}.'
                ''.format(device_name))
            log.log2debug(1073, log_message)

        # Create a list of IP addresses
        ipv4 = sorted(arp_table.keys())

        # Send log message
        log_message = ('Performing IP address hostname lookups.')
        log.log2debug(1173, log_message)

        # Create a pool of sub process resources
        # Faster lookups
        with Pool(processes=threads_in_pool) as pool:

            # Create sub processes from the pool
            results = pool.map(_nslookup, ipv4)

        # Process results
        for (ipv4, hostname) in results:
            arp_table[ipv4]['hostname'] = hostname
            if bool(hostname) is True:
                host_table[hostname] = ipv4

        # Create yaml files
        general.create_yaml_file(arp_table, self._config.arp_file())
        log_message = ('Created ARP table search file.')
        log.log2debug(1082, log_message)

        general.create_yaml_file(host_table, self._config.hosts_file())
        log_message = ('Created hosts table search file.')
        log.log2debug(1054, log_message)

    def _rarp(self):
        """Create RARP, ARP and host table YAML search files.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        rarp_table = {}

        # Create host, ARP table files
        # Cycle through list of files in directory
        for filepath in self._filepaths:
            # Read file
            device_dict = general.read_yaml_file(filepath)

            # Get the device name
            device_name = device_dict['misc']['host']

            # Send log message
            log_message = (
                'Creating RARP table for {}.'
                ''.format(device_name))
            log.log2debug(1172, log_message)

            # Populate ARP and RARP table
            if 'layer3' in device_dict:
                keys = ['cInetNetToMediaPhysAddress', 'ipNetToMediaTable']
                for key in keys:
                    if key in device_dict['layer3']:
                        arp_dict = device_dict['layer3'][key]

                        for ip_address, mac_addr in arp_dict.items():
                            # Populate RARP table (Using ARP entries)
                            if mac_addr in rarp_table:
                                # Only append unique entries
                                if ip_address not in rarp_table[mac_addr]:
                                    rarp_table[mac_addr].append(ip_address)
                            else:
                                rarp_table[mac_addr] = [ip_address]

            # Populate entries in rarp_table that correspond to multicast
            if 'layer1' in device_dict:
                layer1_dict = device_dict['layer1']

                # Process each port on device
                for _, port_dict in layer1_dict.items():
                    # Skip non ethernet ports
                    if 'jm_ethernet' not in port_dict:
                        continue

                    # Process MAC addresses
                    if ('jm_macs' in port_dict) and (
                            bool(port_dict['jm_macs']) is True):

                        # Create an ifIndex and device entry
                        # for each RARP entry
                        for mac_addr in port_dict['jm_macs']:
                            # Populate RARP table. Not all MACs have
                            # an associated ARP IP address (eg. multicast)
                            if mac_addr not in rarp_table:
                                rarp_table[mac_addr] = []

            # Send log message
            log_message = (
                'Completed RARP table for {}.'
                ''.format(device_name))
            log.log2debug(1075, log_message)

        # Create yaml files
        general.create_yaml_file(rarp_table, self._config.rarp_file())
        log_message = ('Created RARP table search file.')
        log.log2debug(1085, log_message)

    def _interface(self):
        """Create Layer 3 YAML files used for Switchmap-NG search.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        ifalias_table = defaultdict(lambda: defaultdict(dict))
        ifindex_table = defaultdict(
            lambda: defaultdict(lambda: defaultdict(dict)))

        # Read RARP file
        rarp_table = general.read_yaml_file(self._config.rarp_file())

        # Create host, ARP table files
        # Cycle through list of files in directory
        for filepath in self._filepaths:
            # Read file
            device_dict = general.read_yaml_file(filepath)

            # Get the device name
            device_name = device_dict['misc']['host']

            # Send log message
            log_message = (
                'Creating ifAlias and ifIndex table for {}.'
                ''.format(device_name))
            log.log2debug(1072, log_message)

            # Populate ifIndex table
            if 'layer1' in device_dict:
                layer1_dict = device_dict['layer1']

                # Process each port on device
                for ifindex, port_dict in sorted(layer1_dict.items()):
                    # Do a quick validation of required keys
                    if _layer3_ok(port_dict) is False:
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
                        for mac_addr in port_dict['jm_macs']:
                            # Skip unknown MAC addresses
                            if mac_addr not in rarp_table:
                                continue

                            # Create ifindex entry
                            for ip_address in rarp_table[mac_addr]:
                                if mac_addr not in ifindex_table:
                                    ifindex_table[mac_addr][device_name][
                                        ifindex] = [ip_address]
                                else:
                                    if device_name not in ifindex_table[
                                            mac_addr]:
                                        ifindex_table[mac_addr][device_name][
                                            ifindex] = [ip_address]
                                    else:
                                        ifindex_table[mac_addr][device_name][
                                            ifindex].append(ip_address)

            # Send log message
            log_message = (
                'Completed ifAlias, ifIndex table for {}.'
                ''.format(device_name))
            log.log2debug(1079, log_message)

        general.create_yaml_file(ifindex_table, self._config.ifindex_file())
        log_message = ('Created ifIndex table search file.')
        log.log2debug(1051, log_message)

        general.create_yaml_file(ifalias_table, self._config.ifalias_file())
        log_message = ('Created ifAlias table search file.')
        log.log2debug(1053, log_message)


def _layer3_ok(port_dict):
    """Deterimine port's suitability for ifIndex and ifAlias processing.

    Args:
        port_dict: Dict of device port information

    Returns:
        valid: True if valid

    """
    # Initialize key variables
    valid = True

    # Do a quick validation of required keys
    keys = ['jm_ethernet', 'jm_trunk', 'ifAlias']
    for key in keys:
        if key not in port_dict:
            valid = False
            return valid

    # Only interested in Ethernet ports
    if bool(port_dict['jm_ethernet']) is False:
        valid = False

    # We are not interested in populating trunk port MAC data
    if bool(port_dict['jm_trunk']) is True:
        valid = False

    # Return
    return valid


def _nslookup(ipv4):
    """Lookup the hostname of an IPv4 address.

    Args:
        ipv4: IPv4 address

    Returns:
        hostname: Name of host

    """
    # Initialize key variables
    hostname = None

    # Return result
    try:
        ip_results = socket.gethostbyaddr(ipv4)
        if len(ip_results) > 1:
            hostname = ip_results[0]

    except:
        hostname = None

    return (ipv4, hostname)
