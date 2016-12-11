#!/usr/bin/env python3
"""Class interacts with devices supporting IfMIB. (64 bit counters)."""


from collections import defaultdict

from switchmap.snmp.base_query import Query


def get_query():
    """Return this module's Query class."""
    return Sentry3Query


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return Sentry3Query(snmp_object)


class Sentry3Query(Query):
    """Class interacts with devices supporting IfMIB.

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
        # Initialize key variables
        self.empty_dict = {}

        # Define query object
        self.snmp_object = snmp_object

        # Get one OID entry in MIB (infeedID)
        test_oid = '.1.3.6.1.4.1.1718.3.2.2.1.2'

        super().__init__(snmp_object, test_oid, tags=['system', 'layer1'])

    def system(self):
        """Get system data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = self.empty_dict

        # Return
        return final

    def layer1(self):
        """Get layer 1 data from device using Layer 1 OIDs.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = self.empty_dict

        # Return
        return final

    def infeedcapacity(self, safe=False):
        """Return dict of Sentry3 MIB infeedCapacity for each ifIndex for device.

        Args:
            safe: Do a failsafe walk if True

        Returns:
            data_dict: Dict of infeedCapacity. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.4.1.1718.3.2.2.1.10'
        if safe is False:
            results = self.snmp_object.walk(oid, normalized=False)
        else:
            results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Process OID
            data_dict[key] = value

        # Return
        return data_dict

    def infeedpower(self, safe=False):
        """Return dict of Sentry3 MIB infeedPower for each ifIndex for device.

        Args:
            safe: Do a failsafe walk if True

        Returns:
            data_dict: Dict of infeedPower. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.4.1.1718.3.2.2.1.12'
        if safe is False:
            results = self.snmp_object.walk(oid, normalized=False)
        else:
            results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Process OID
            data_dict[key] = value

        # Return
        return data_dict

    def infeedloadvalue(self, safe=False):
        """Return dict of Sentry3 MIB infeedLoadValue for each ifIndex for device.

        Args:
            safe: Do a failsafe walk if True

        Returns:
            data_dict: Dict of infeedLoadValue. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.4.1.1718.3.2.2.1.7'
        if safe is False:
            results = self.snmp_object.walk(oid, normalized=False)
        else:
            results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Process OID
            data_dict[key] = value / 100

        # Return
        return data_dict

    def infeedid(self, safe=False):
        """Return dict of Sentry3 MIB infeedID for each ifIndex for device.

        Args:
            safe: Do a failsafe walk if True

        Returns:
            data_dict: Dict of infeedID. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.4.1.1718.3.2.2.1.2'
        if safe is False:
            results = self.snmp_object.walk(oid, normalized=False)
        else:
            results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Process OID
            data_dict[key] = str(bytes(value), encoding='utf-8')

        # Return
        return data_dict

    def infeedname(self, safe=False):
        """Return dict of Sentry3 MIB infeedName for each ifIndex for device.

        Args:
            safe: Do a failsafe walk if True

        Returns:
            data_dict: Dict of infeedName. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.4.1.1718.3.2.2.1.3'
        if safe is False:
            results = self.snmp_object.walk(oid, normalized=False)
        else:
            results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Process OID
            data_dict[key] = str(bytes(value), encoding='utf-8')

        # Return
        return data_dict


def _get_data(title, func, dest):
    """Populate dest with data from the given function.

    Args:
        title: The name of the data
        func: The function which will return the data
        dest: a dict which will store the data

    Returns:
        dest: The modified destination dict

    """
    # Process data
    values = func()
    for key, value in values.items():
        dest[key][title] = value

    return dest
