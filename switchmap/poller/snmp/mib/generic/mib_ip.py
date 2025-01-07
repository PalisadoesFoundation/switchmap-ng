"""Class interacts with devices supporting IP-MIB."""

from collections import defaultdict

from switchmap.poller.snmp.base_query import Query
from switchmap.core import general


def get_query():
    """
    Return this module's Query class.
    
    Args:
        None

    Returns:
        IpQuery: Query class object
    """
    return IpQuery


def init_query(snmp_object):
    """
    Return initialize and return this module's Query class.
    
    Args:
        snmp_object: SNMP Interact class object from snmp_manager.py

    Returns:
        IpQuery: Query class object
    """
    return IpQuery(snmp_object)


class IpQuery(Query):
    """Class interacts with devices supporting IP-MIB.

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
        """Instantiate the class.

        Args:
            snmp_object: SNMP Interact class object from snmp_manager.py

        Returns:
            None

        """
        # Define query object
        self.snmp_object = snmp_object

        super().__init__(snmp_object, "", tags=["layer3"])

    def supported(self):
        """Return device's support for the MIB.

        Args:
            None

        Returns:
            validity: True if supported

        """
        # Support OID
        validity = True

        # Return
        return validity

    def layer3(self):
        """Get layer 3 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface ipNetToMediaTable data
        values = self.ipnettomediatable()
        for key, value in values.items():
            final["ipNetToMediaTable"][key] = value

        # Get interface ipNetToPhysicalPhysAddress data
        values = self.ipnettophysicalphysaddress()
        for key, value in values.items():
            final["ipNetToPhysicalPhysAddress"][key] = value

        # Return
        return final

    def ipnettomediatable(self, oidonly=False):
        """Return dict of ipNetToMediaTable, the device's ARP table.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of MAC addresses keyed by IPv4 address

        """
        # Initialize key variables
        data_dict = {}

        # Process
        oid = ".1.3.6.1.2.1.4.22.1.2"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Determine IP address
            nodes = key.split(".")
            octets = nodes[-4:]
            ipaddress = ".".join(octets)

            # Determine MAC address
            macaddress = general.octetstr_2_string(value)

            # Create ARP table entry
            data_dict[ipaddress] = macaddress

        # Return data
        return data_dict

    def ipnettophysicalphysaddress(self, oidonly=False):
        """Return dict of the device's ipNetToPhysicalPhysAddress ARP table.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of MAC addresses keyed by IPv6 Address

        """
        # Initialize key variables
        data_dict = {}
        oid = ".1.3.6.1.2.1.4.35.1.4"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.swalk(oid, normalized=False)
        for key, mac_value in results.items():
            # Get IP address, first 12 characters
            macaddress = general.octetstr_2_string(mac_value)

            # Convert IP address from decimal to hex
            nodes = key.split(".")

            # We want to remove IPv4 addresses from results
            if len(nodes) < 16 + len(oid.split(".")):
                continue

            # Process IPv6
            nodes_decimal = nodes[-16:]
            nodes_hex = []
            nodes_final = []
            for value in nodes_decimal:
                # Convert deximal value to hex,
                # then zero fill to ensure hex is two characters long
                hexbyte = "{}".format(hex(int(value)))[2:]
                nodes_hex.append(hexbyte.zfill(2))

            # Convert to list of four byte hex numbers
            for pointer in range(0, len(nodes_hex) - 1, 2):
                fixed_value = "{}{}".format(
                    nodes_hex[pointer], nodes_hex[pointer + 1]
                )
                nodes_final.append(fixed_value)

            # Create IPv6 string
            ipv6 = ":".join(nodes_final)

            # Create ARP entry
            data_dict[ipv6] = macaddress

        # Return data
        return data_dict
