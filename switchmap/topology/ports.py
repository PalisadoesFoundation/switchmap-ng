#!usr/bin/env python3
"""Class for creating device web pages."""

# Standard HTML
import csv

# Import switchmap.libraries
from switchmap.utils import general


class Lookup(object):
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
        with open(mac_address_file, "r") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=":")
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
        html_manufacturer = ""
        html_mac_address = ""
        html_ip_address = ""
        html_hostname = ""
        result = {}

        for item in listing:
            html_hostname = "{}<p>{}<p>".format(html_hostname, item["hostname"])
            html_manufacturer = "{}<p>{}<p>".format(
                html_manufacturer, item["manufacturer"]
            )
            html_ip_address = "{}<p>{}<p>".format(html_ip_address, item["ip_address"])

            if bool(item["mac_address"]) is True:
                html_mac_address = "{}<p>{}<p>".format(
                    html_mac_address, item["mac_address"]
                )
            else:
                html_mac_address = ""

        # Return
        result["ip_address"] = html_ip_address
        result["hostname"] = html_hostname
        result["manufacturer"] = html_manufacturer
        result["mac_address"] = html_mac_address
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
            data_dict["mac_address"] = mac_address
            data_dict["manufacturer"] = manufacturer
            preliminary_listing.append(data_dict)

        # Get IP address and hostname for each mac address
        for item in preliminary_listing:
            mac_address = item["mac_address"]
            manufacturer = item["manufacturer"]

            if mac_address in self.rarp_table:
                # MAC address has related IP
                if bool(self.rarp_table[mac_address]) is True:
                    for ip_address in self.rarp_table[mac_address]:
                        data_dict = {}
                        data_dict["mac_address"] = mac_address
                        data_dict["manufacturer"] = manufacturer
                        data_dict["ip_address"] = ip_address
                        data_dict["hostname"] = ""

                        if ip_address in self.arp_table:
                            if "hostname" in self.arp_table[ip_address]:
                                hostname = self.arp_table[ip_address]["hostname"]
                                data_dict["hostname"] = hostname

                        listing.append(data_dict)
                else:
                    # MAC address has no related IP
                    data_dict = {}
                    data_dict["mac_address"] = mac_address
                    data_dict["manufacturer"] = manufacturer
                    data_dict["ip_address"] = ""
                    data_dict["hostname"] = ""
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
        manufacturer = ""

        # Process data
        mac_oui = mac_address[0:6]
        if mac_oui in self.oui:
            manufacturer = self.oui[mac_oui]

        # Return
        return manufacturer
