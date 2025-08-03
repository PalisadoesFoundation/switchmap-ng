"""Module for ETHERLIKE-MIB."""

from collections import defaultdict

from switchmap.poller.snmp.base_query import Query


def get_query():
    """Return this module's Query class.

    Args:
        None

    Returns:
        EtherlikeQuery: Query class object
    """
    return EtherlikeQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class.

    Args:
        snmp_object: SNMP Interact class object from snmp_manager.py

    Returns:
        EtherlikeQuery: Query class object
    """
    return EtherlikeQuery(snmp_object)


class EtherlikeQuery(Query):
    """Class interacts with ETHERLIKE-MIB.

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

        # Get one OID entry in MIB (dot3StatsDuplexStatus)
        test_oid = ".1.3.6.1.2.1.10.7.2.1.19"

        super().__init__(snmp_object, test_oid, tags=["layer1"])

    async def layer1(self):
        """Get layer 1 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface dot3StatsDuplexStatus data
        values =await self.dot3statsduplexstatus()
        for key, value in values.items():
            final[key]["dot3StatsDuplexStatus"] = value

        # Return
        return final

    async def dot3statsduplexstatus(self, oidonly=False):
        """Return dict of ETHERLIKE-MIB dot3StatsDuplexStatus for each port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of dot3StatsDuplexStatus using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # OID to process
        oid = ".1.3.6.1.2.1.10.7.2.1.19"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict
