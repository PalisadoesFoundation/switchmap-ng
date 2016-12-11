#!/usr/bin/env python3
"""Class interacts with devices supporting IfMIB. (64 bit counters)."""


from collections import defaultdict

from switchmap.snmp.base_query import Query


def get_query():
    """Return this module's Query class."""
    return EmersonFPCQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return EmersonFPCQuery(snmp_object)


class EmersonFPCQuery(Query):
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
        test_oid = '.1.3.6.1.4.1.476.1.42.2.4.2.1.2.1'

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

    def branch_amps_a(self, safe=False):
        """Return dict of LIEBERT-GP-FLEXIBLE-MIB branch_amps_a.

        Args:
            safe: Do a failsafe walk if True

        Returns:
            data_dict: Dict of branch_amps_a. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.5219'
        if safe is False:
            results = self.snmp_object.walk(oid, normalized=False)
        else:
            results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Process OID
            data_dict[key] = float(value)

        # Return
        return data_dict

    def branch_amps_b(self, safe=False):
        """Return dict of LIEBERT-GP-FLEXIBLE-MIB branch_amps_b.

        Args:
            safe: Do a failsafe walk if True

        Returns:
            data_dict: Dict of branch_amps_b. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.5220'
        if safe is False:
            results = self.snmp_object.walk(oid, normalized=False)
        else:
            results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Process OID
            data_dict[key] = float(value)

        # Return
        return data_dict

    def branch_amps_c(self, safe=False):
        """Return dict of LIEBERT-GP-FLEXIBLE-MIB branch_amps_c.

        Args:
            safe: Do a failsafe walk if True

        Returns:
            data_dict: Dict of branch_amps_c. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.5221'
        if safe is False:
            results = self.snmp_object.walk(oid, normalized=False)
        else:
            results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Process OID
            data_dict[key] = float(value)

        # Return
        return data_dict

    def branch_watts(self, safe=False):
        """Return dict of LIEBERT-GP-FLEXIBLE-MIB branch_watts.

        Args:
            safe: Do a failsafe walk if True

        Returns:
            data_dict: Dict of branch_watts. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.4.1.476.1.42.3.9.30.1.20.1.2.1.5222'
        if safe is False:
            results = self.snmp_object.walk(oid, normalized=False)
        else:
            results = self.snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Process OID
            data_dict[key] = float(value)

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
