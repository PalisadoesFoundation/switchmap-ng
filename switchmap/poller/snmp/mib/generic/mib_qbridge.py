"""Module for Q-BRIDGE-MIB."""

from collections import defaultdict

# Import project libraries
from switchmap.poller.snmp.base_query import Query
from switchmap.poller.snmp import BridgeQuery


def get_query():
    """Return this module's Query class.

    Args:
        None

    Returns:
        QbridgeQuery: Query class object
    """
    return QbridgeQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class.

    Args:
        snmp_object: SNMP Interact class object from snmp_manager.py

    Returns:
        QbridgeQuery: Query class object
    """
    return QbridgeQuery(snmp_object)


class QbridgeQuery(Query):
    """Class interacts with Q-BRIDGE-MIB.

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

        # Get one OID entry in MIB (dot1qPvid)
        test_oid = ".1.3.6.1.2.1.17.7.1.4.5.1.1"

        super().__init__(snmp_object, test_oid, tags=["layer1"])

        # Get a mapping of dot1dbaseport values to the corresponding ifindex
        self.baseportifindex = None

    async def _get_bridge_data(self):
        """Load bridge data only when needed."""
        if self.baseportifindex is None:
            self.bridge_mib = BridgeQuery(self.snmp_object)

            if await self.supported() and await self.bridge_mib.supported():
                self.baseportifindex = (
                    await self.bridge_mib.dot1dbaseport_2_ifindex()
                )
            else:
                self.baseportifindex = {}

    async def layer1(self):
        """Get layer 1 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        await self._get_bridge_data()

        # Get interface dot1qPvid data
        values = await self.dot1qpvid()
        for key, value in values.items():
            final[key]["dot1qPvid"] = value

        # Return
        return final

    async def layer2(self):
        """Get layer 2 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface dot1qVlanStaticName data
        values = await self.dot1qvlanstaticname()
        for key, value in values.items():
            final[key]["dot1qVlanStaticName"] = value

        # Return
        return final

    async def dot1qpvid(self, oidonly=False):
        """Return dict of Q-BRIDGE-MIB dot1qPvid per port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of dot1qPvid using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = ".1.3.6.1.2.1.17.7.1.4.5.1.1"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            ifindex = self.baseportifindex.get(int(key))
            if ifindex is not None:
                data_dict[ifindex] = value

        # Return
        return data_dict

    async def dot1qvlanstaticname(self, oidonly=False):
        """Return dict of Q-BRIDGE-MIB dot1qVlanStaticName per port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of dot1qVlanStaticName using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = ".1.3.6.1.2.1.17.7.1.4.3.1.1"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[key] = str(bytes(value), encoding="utf-8")

        # Return
        return data_dict
