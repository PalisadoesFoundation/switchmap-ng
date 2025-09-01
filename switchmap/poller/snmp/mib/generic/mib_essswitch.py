"""Module for MIB-ESSWITCH."""

from collections import defaultdict

from switchmap.poller.snmp.base_query import Query


def get_query():
    """Return this module's Query class.

    Args:
        None

    Returns:
        EssSwitchQuery: Query class object
    """
    return EssSwitchQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class.

    Args:
        snmp_object: SNMP Interact class object from snmp_manager.py

    Returns:
        EssSwitchQuery: Query class object
    """
    return EssSwitchQuery(snmp_object)


class EssSwitchQuery(Query):
    """Class interacts with MIB-ESSWITCH.

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

        # Get one OID entry in MIB (swPortDuplexStatus)
        test_oid = ".1.3.6.1.4.1.437.1.1.3.3.1.1.30"

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

        # Get interface swPortDuplexStatus data
        values = await self.swportduplexstatus()
        for key, value in values.items():
            final[key]["swPortDuplexStatus"] = value

        # Return
        return final

    async def swportduplexstatus(self, oidonly=False):
        """Return dict of MIB-ESSWITCH swPortDuplexStatus for each port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of swPortDuplexStatus using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # OID to process
        oid = ".1.3.6.1.4.1.437.1.1.3.3.1.1.30"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict
