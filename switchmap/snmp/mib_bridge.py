#!/usr/bin/env python3
"""Class interacts with devices supporting BRIDGE-MIB."""


from collections import defaultdict
import binascii

from switchmap.snmp.base_query import Query


def get_query():
    """Return this module's Query class."""
    return BridgeQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return BridgeQuery(snmp_object)


class BridgeQuery(Query):
    """Class interacts with devices supporting BRIDGE-MIB.

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
        # Get one OID entry in MIB (dot1dBasePortIfIndex)
        test_oid = '.1.3.6.1.2.1.17.4.3.1.2'

        super().__init__(snmp_object, test_oid, tags=['layer1'])

    def layer1(self):
        """Get layer 1 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Return
        return self._macaddresstable()

    def _macaddresstable(self):
        """Return dict of the devices MAC address table.

        Args:
            None

        Returns:
            final: Dict of MAC addresses keyed by ifIndex

        """
        # Initialize key variables
        data_dict = defaultdict(lambda: defaultdict(dict))
        final = defaultdict(lambda: defaultdict(dict))
        baseport = self._dot1dtpfdbport()
        macs = self._dot1dtpfdbaddress()
        baseportifindex = self.dot1dbaseport_2_ifindex()

        # Create a dict keyed by ifIndex
        for key, value in macs.items():
            # Get ifIndex from dot1dBasePort
            ifindex = baseportifindex[int(baseport[key])]

            # With multi-threading sometimes baseportifindex has empty values.
            if bool(ifindex) is False:
                continue

            # Assign MAC addresses to ifIndex
            if ifindex not in data_dict:
                data_dict[ifindex] = [value]
            else:
                data_dict[ifindex].append(value)

        # Assign MACs to secondary key for final result
        for key, value in data_dict.items():
            final[key]['jm_macs'] = []
            for next_mac in value:
                final[key]['jm_macs'].append(next_mac)

        # Return
        return final

    def _dot1dtpfdbport(self):
        """Return dict of BRIDGE-MIB dot1dtpfdbport data.

        Args:
            None

        Returns:
            data_dict: Dict of dot1dtpfdbport using the OID nodes
                excluding the OID root as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process values
        oid = '.1.3.6.1.2.1.17.4.3.1.2'
        results = self.snmp_object.walk(oid, normalized=False)
        for key, value in results.items():
            new_key = key[len(oid):]
            data_dict[new_key] = value

        # Return data
        return data_dict

    def _dot1dtpfdbaddress(self):
        """Return dict of BRIDGE-MIB dot1dTpFdbAddress data.

        Args:
            None

        Returns:
            data_dict: Dict of dot1dTpFdbAddress using the OID nodes
                excluding the OID root as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process values
        oid = '.1.3.6.1.2.1.17.4.3.1.1'
        results = self.snmp_object.walk(oid, normalized=False)
        for key, value in results.items():
            new_key = key[len(oid):]
            macaddress = binascii.hexlify(value).decode('utf-8')
            data_dict[new_key] = macaddress.lower()

        # Return data
        return data_dict

    def dot1dbaseport_2_ifindex(self):
        """Return dict of BRIDGE-MIB dot1dBasePortIfIndex data.

        Args:
            None

        Returns:
            data_dict: Dict of dot1dBasePortIfIndex with dot1dBasePort as key.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process values
        oid = '.1.3.6.1.2.1.17.1.4.1.2'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = value

        # Return data
        return data_dict
