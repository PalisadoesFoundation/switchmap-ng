#!/usr/bin/env python3
"""Class interacts with CISCO-IETF-IP-MIB."""


from collections import defaultdict

from switchmap.snmp.base_query import Query
from switchmap.utils import general


def get_query():
    """Return this module's Query class."""
    return CiscoIetfIpQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return CiscoIetfIpQuery(snmp_object)


class CiscoIetfIpQuery(Query):
    """Class interacts with CISCO-IETF-IP-MIB.

    Args:
        None

    Returns:
        None

    Key Methods:

        supported: Queries the device to determine whether the MIB is
            supported using a known OID defined in the MIB. Returns True
            if the device returns a response to the OID, False if not.

        layer3: Returns all needed layer 3 MIB information from the device.
            Keyed by OID's MIB name (primary key), IP address (secondary key).

    """

    def __init__(self, snmp_object):
        """Function for intializing the class.

        Args:
            snmp_object: SNMP Interact class object from snmp_manager.py

        Returns:
            None

        """
        # Define query object
        self.snmp_object = snmp_object

        # Get one OID entry in MIB (cInetNetToMediaPhysAddress)
        test_oid = '.1.3.6.1.4.1.9.10.86.1.1.3.1.3'

        super().__init__(snmp_object, test_oid, tags=['layer3'])

    def layer3(self):
        """Get layer 3 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface cInetNetToMediaPhysAddress data
        values = self.cinetnettomediaphysaddress()
        for key, mac_value in values.items():
            final['cInetNetToMediaPhysAddress'][key] = mac_value[:12]

        # Return
        return final

    def cinetnettomediaphysaddress(self):
        """Return dict of the device's ARP table.

        Args:
            None

        Returns:
            data_dict: Dict of MAC addresses keyed by IPv6 Address

        """
        # Initialize key variables
        data_dict = defaultdict(dict)
        oid = '.1.3.6.1.4.1.9.10.86.1.1.3.1.3'

        # Get results
        results = self.snmp_object.swalk(oid, normalized=False)
        for key, mac_value in results.items():
            # Get MAC address
            macaddress = general.octetstr_2_string(mac_value)

            # Convert IP address from decimal to hex
            nodes = key.split('.')
            ipv6decimal = nodes[-16:]
            ipv6hex = []
            for value in ipv6decimal:
                # Convert deximal value to hex,
                # then zero fill to ensure hex is two characters long
                hexbyte = '{}'.format(hex(int(value)))[2:]
                ipv6hex.append(hexbyte.zfill(2))

            # Create IPv6 string
            ipv6 = ':'.join(ipv6hex)

            # Create ARP entry
            data_dict[ipv6] = macaddress

        # Return data
        return data_dict
