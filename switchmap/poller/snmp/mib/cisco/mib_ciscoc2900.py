"""Module for CISCO-C2900-MIB."""

from collections import defaultdict

from switchmap.poller.snmp.base_query import Query


def get_query():
    """Return this module's Query class."""
    return CiscoC2900Query


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return CiscoC2900Query(snmp_object)


class CiscoC2900Query(Query):
    """Class interacts with CISCO-C2900-MIB.

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
        """Instantiate the class.

        Args:
            snmp_object: SNMP Interact class object from snmp_manager.py

        Returns:
            None

        """
        # Define query object
        self.snmp_object = snmp_object

        # Get one OID entry in MIB (c2900PortLinkbeatStatus)
        test_oid = ".1.3.6.1.4.1.9.9.87.1.4.1.1.18"

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

        # Get interface c2900PortDuplexStatus data
        values = self.c2900portduplexstatus()
        for key, value in values.items():
            final[key]["c2900PortDuplexStatus"] = value

        # Get interface c2900PortLinkbeatStatus data
        values = self.c2900portlinkbeatstatus()
        for key, value in values.items():
            final[key]["c2900PortLinkbeatStatus"] = value

        # Return
        return final

    def c2900portlinkbeatstatus(self, oidonly=False):
        """Return dict of CISCO-C2900-MIB c2900PortLinkbeatStatus per port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of c2900PortLinkbeatStatus using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.4.1.9.9.87.1.4.1.1.18"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def c2900portduplexstatus(self, oidonly=False):
        """Return dict of CISCO-C2900-MIB c2900PortDuplexStatus for each port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of c2900PortDuplexStatus using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.4.1.9.9.87.1.4.1.1.32"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict
