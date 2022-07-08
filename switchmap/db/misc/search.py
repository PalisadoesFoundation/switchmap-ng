#!/usr/bin/env python3
"""switchmap.Search class.

Description:

    This files has classes that process searches for:
        1) IP and MAC address
        2) Port names
        3) Hostnames

"""
# Standard imports
import re

# Switchmap-NG imports
from switchmap.utils import general
from switchmap.core import general as _general
from switchmap.db.table import mac


class Search():
    """Class that manages searches.

    Methods return lists of dicts keyed 'layer 1' with ifindex values
    where search strings were found. This data is then used to create result
    tables.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, searchstring, config):
        """Initialize the class.

        Args:
            searchstring: search string to look for
            config: Config object

        Returns:
            None

        """
        # Initialize key variables
        self._search = []
        self.config = config

        # Generate various possible strings that could be used for searches
        self._search = searchstring

    def find(self):
        """Find search string.

        Args:
            None

        Returns:
            result: list of dicts that contain matching items

        """
        # Initialize key variables
        result = []

        # Do each successive search
        result.extend(self.macaddress())
        result.extend(self.ifalias())
        result.extend(self.ipaddress())
        result.extend(self.hostname())

        # Return
        return result

    def macaddress(self):
        """Search for macaddress.

        Args:
            None

        Returns:
            result: list of dicts that contain matching addresses

        """
        # Initialize key variables
        result = []
        # Return
        _mac = _general.mac(self._search)
        exists = mac.exists(_mac)
        if bool(exists) is True:
            pass

        result = _macaddress(self._search, self.ifindex_data)
        return result

    def ipaddress(self):
        """Search for ipaddress.

        Args:
            None

        Returns:
            result: list of dicts that contain matching addresses

        """
        # Initialize key variables
        result = []

        # Process the ifindex file
        for _, devices in self.ifindex_data.items():
            # Get all the hostnames and ifindexes that have the MAC
            for device, ifindexes in devices.items():
                for ifindex, ipaddresses in ifindexes.items():
                    for ipaddress in ipaddresses:
                        # Find search string in MAC address keys
                        for possible in self._search:
                            if possible in '{}'.format(ipaddress).lower():
                                data_dict = {}
                                data_dict[device] = int(ifindex)
                                result.append(data_dict)

        # Return
        return result

    def ifalias(self):
        """Search for string in ifalias names.

        Args:
            None

        Returns:
            result: list of dicts that contain matching addresses

        """
        # Initialize key variables
        result = []

        for ifalias, ifalias_dict in self.ifalias_data.items():
            # Find search string in ifalias keys
            for possible in self._search:
                if possible in '{}'.format(ifalias).lower():
                    # We have found something
                    for device, ifindexes in ifalias_dict.items():
                        for ifindex in ifindexes:
                            data_dict = {}
                            data_dict[device] = int(ifindex)
                            result.append(data_dict)

        # Return
        return result

    def hostname(self):
        """Search for string hostnames.

        Args:
            None

        Returns:
            result: list of dicts that contain matching addresses

        """
        # Initialize key variables
        result = []
        macaddresses = []

        for _, data_dict in self.arp_data.items():
            # Make sure we can get the hostname and MAC
            if 'hostname' not in data_dict:
                continue
            if 'mac_address' not in data_dict:
                continue

            # Find search string in MAC address keys
            hostname = data_dict['hostname']
            macaddress = data_dict['mac_address']

            # If there is no hostname return (multicast)
            if bool(hostname) is False:
                continue

            for possible in self._search:
                if possible in hostname.lower():
                    macaddresses.append(macaddress)

        # See if we can get the ifindex for the macaddress
        result.extend(_macaddress(macaddresses, self.ifindex_data))

        # Return
        return result


class Mac(object):
    """Class that creates the device's various HTML tables."""

    def __init__(self, config):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Get configuration
        mac_address_file = config.mac_address_file()
        self.oui = {}

        # Read file
        with open(mac_address_file, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=':')
            for row in spamreader:
                mac_address = row[0]
                manufacturer = row[1]
                self.oui[mac_address] = manufacturer

        # Read ARP, RARP tables
        self.rarp_table = general.read_yaml_file(config.rarp_file())
        self.arp_table = general.read_yaml_file(config.arp_file())

    def html(self, mac_addresses):
        """Create list of dicts of MAC, host, manufacturer, IP address.

        Args:
            mac_addresses

        Returns:
            oui: OUI dictionary

        """
        # Initialize key variables
        listing = self._listing(mac_addresses)
        html_manufacturer = ''
        html_mac_address = ''
        html_ip_address = ''
        html_hostname = ''
        result = {}

        for item in listing:
            html_hostname = '{}<p>{}<p>'.format(
                html_hostname, item['hostname'])
            html_manufacturer = '{}<p>{}<p>'.format(
                html_manufacturer, item['manufacturer'])
            html_ip_address = '{}<p>{}<p>'.format(
                html_ip_address, item['ip_address'])

            if bool(item['mac_address']) is True:
                html_mac_address = '{}<p>{}<p>'.format(
                    html_mac_address, item['mac_address'])
            else:
                html_mac_address = ''

        # Return
        result['ip_address'] = html_ip_address
        result['hostname'] = html_hostname
        result['manufacturer'] = html_manufacturer
        result['mac_address'] = html_mac_address
        return result

    def _listing(self, mac_addresses):
        """Create list of dicts of MAC, host, manufacturer, IP address.

        Args:
            None

        Returns:
            oui: OUI dictionary

        """
        # Initialize key variables
        preliminary_listing = []
        listing = []

        # Cycle through mac addresses, get the manufacturer
        for mac_address in mac_addresses:
            # Get manufacturer
            manufacturer = self._manufacturer(mac_address)
            data_dict = {}
            data_dict['mac_address'] = mac_address
            data_dict['manufacturer'] = manufacturer
            preliminary_listing.append(data_dict)

        # Get IP address and hostname for each mac address
        for item in preliminary_listing:
            mac_address = item['mac_address']
            manufacturer = item['manufacturer']

            if mac_address in self.rarp_table:
                # MAC address has related IP
                if bool(self.rarp_table[mac_address]) is True:
                    for ip_address in self.rarp_table[mac_address]:
                        data_dict = {}
                        data_dict['mac_address'] = mac_address
                        data_dict['manufacturer'] = manufacturer
                        data_dict['ip_address'] = ip_address
                        data_dict['hostname'] = ''

                        if ip_address in self.arp_table:
                            if 'hostname' in self.arp_table[ip_address]:
                                hostname = self.arp_table[
                                    ip_address]['hostname']
                                data_dict['hostname'] = hostname

                        listing.append(data_dict)
                else:
                    # MAC address has no related IP
                    data_dict = {}
                    data_dict['mac_address'] = mac_address
                    data_dict['manufacturer'] = manufacturer
                    data_dict['ip_address'] = ''
                    data_dict['hostname'] = ''
                    listing.append(data_dict)

        # Return
        return listing

    def _manufacturer(self, mac_address):
        """Return manufacturer of MAC address' device.

        Args:
            mac_address: MAC address

        Returns:
            manufacturer: Name of manufacturer

        """
        # Initialize key variables
        manufacturer = ''

        # Process data
        mac_oui = mac_address[0:6]
        if mac_oui in self.oui:
            manufacturer = self.oui[mac_oui]

        # Return
        return manufacturer


def _macaddress(_search, ifindex_data):
    """Search for macaddress.

    Args:
        _search: List of search values to Find
        ifindex_data: ifindex data to search through

    Returns:
        result: list of dicts that contain matching addresses

    """
    # Initialize key variables
    result = []

    # Process the ifindex file
    for macaddress, devices in ifindex_data.items():
        # Find search string in MAC address keys
        for possible in _search:

            if possible in '{}'.format(macaddress).lower():
                # Get all the devices and ifindexes that have the MAC
                for device, ifindexes in devices.items():
                    for ifindex, _ in ifindexes.items():
                        data_dict = {}
                        data_dict[device] = int(ifindex)
                        result.append(data_dict)

    # Return
    return result
