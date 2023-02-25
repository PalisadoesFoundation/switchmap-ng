"""Module for CISCO-VLAN-IFTABLE-RELATIONSHIP-MIB."""

from collections import defaultdict

from switchmap.poller.snmp.base_query import Query


def get_query():
    """Return this module's Query class."""
    return CiscoVlanIftableRelationshipQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return CiscoVlanIftableRelationshipQuery(snmp_object)


class CiscoVlanIftableRelationshipQuery(Query):
    """Class interacts with CISCO-VLAN-IFTABLE-RELATIONSHIP-MIB.

    Args:
        None

    Returns:
        None

    Key Methods:

        supported: Queries the device to determine whether the MIB is
            supported using a known OID defined in the MIB. Returns True
            if the device returns a response to the OID, False if not.

        layer1: Returns all needed layer 1 MIB information from the device.
            Keyed by OID's MIB name (primary key), ifIndex (secondary key)

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

        # Get one OID entry in MIB (cviRoutedVlanIfIndex)
        test_oid = ".1.3.6.1.4.1.9.9.128.1.1.1.1.3"

        super().__init__(snmp_object, test_oid, tags=["layer1"])

    def layer1(self):
        """Get layer 1 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface cviRoutedVlanIfIndex data
        values = self.cviroutedvlanifindex()
        for key, value in values.items():
            final[key]["cviRoutedVlanIfIndex"] = value

        # Return
        return final

    def cviroutedvlanifindex(self, oidonly=False):
        """Return dict of CISCO-VLAN-IFTABLE-RELATIONSHIP-MIB
            cviRoutedVlanIfIndex for each VLAN.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of cviRoutedVlanIfIndex using the oid's last node
                as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = ".1.3.6.1.4.1.9.9.128.1.1.1.1.3"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process data
        results = self.snmp_object.swalk(oid, normalized=False)
        for oid, ifindex in results.items():
            nodes = oid.split(".")
            vlan = int(nodes[-2])
            data_dict[ifindex] = [vlan]

        # Return the interface descriptions
        return data_dict
