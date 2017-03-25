#!/usr/bin/env python3
"""Class interacts with devices supporting IfMIB. (64 Bit Counters)."""


from collections import defaultdict

from switchmap.snmp.base_query import Query


def get_query():
    """Return this module's Query class."""
    return If64Query


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return If64Query(snmp_object)


class If64Query(Query):
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

        # Get one OID entry in MIB (ifHCInOctets)
        test_oid = '.1.3.6.1.2.1.31.1.1.1.6'

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
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface ifHCOutBroadcastPkts data
        _get_data('ifHCOutBroadcastPkts', self.ifhcoutbroadcastpkts, final)

        # Get interface ifHCOutMulticastPkts data
        _get_data('ifHCOutMulticastPkts', self.ifhcoutmulticastpkts, final)

        # Get interface ifHCOutUcastPkts data
        _get_data('ifHCOutUcastPkts', self.ifhcoutucastpkts, final)

        # Get interface ifHCOutOctets data
        _get_data('ifHCOutOctets', self.ifhcoutoctets, final)

        # Get interface ifHCInBroadcastPkts data
        _get_data('ifHCInBroadcastPkts', self.ifhcinbroadcastpkts, final)

        # Get interface ifHCInMulticastPkts data
        _get_data('ifHCInMulticastPkts', self.ifhcinmulticastpkts, final)

        # Get interface ifHCInUcastPkts data
        _get_data('ifHCInUcastPkts', self.ifhcinucastpkts, final)

        # Get interface ifHCInOctets data
        _get_data('ifHCInOctets', self.ifhcinoctets, final)

        # Get interface ifHighSpeed data
        _get_data('ifHighSpeed', self.ifhighspeed, final)

        # Return
        return final

    def ifhighspeed(self, oidonly=False):
        """Return dict of IFMIB ifHighSpeed for each ifIndex for device.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of ifHighSpeed using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.15'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def ifhcinucastpkts(self, oidonly=False):
        """Return dict of IFMIB ifHCInUcastPkts for each ifIndex for device.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of ifHCInUcastPkts using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.7'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = value

        # Return
        return data_dict

    def ifhcoutucastpkts(self, oidonly=False):
        """Return dict of IFMIB ifHCOutUcastPkts for each ifIndex for device.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of ifHCOutUcastPkts. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.11'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = value

        # Return
        return data_dict

    def ifhcinmulticastpkts(self, oidonly=False):
        """Return dict of IFMIB ifHCInMulticastPkts for each ifIndex for device.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of ifHCInMulticastPkts. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.8'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = value

        # Return
        return data_dict

    def ifhcoutmulticastpkts(self, oidonly=False):
        """Return dict of IFMIB ifHCOutMulticastPkts for each ifIndex for device.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of ifHCOutMulticastPkts. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.12'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = value

        # Return
        return data_dict

    def ifhcinbroadcastpkts(self, oidonly=False):
        """Return dict of IFMIB ifHCInBroadcastPkts for each ifIndex for device.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of ifHCInBroadcastPkts. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.9'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = value

        # Return
        return data_dict

    def ifhcoutbroadcastpkts(self, oidonly=False):
        """Return dict of IFMIB ifHCOutBroadcastPkts for each ifIndex for device.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of ifHCOutBroadcastPkts. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.13'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = value

        # Return
        return data_dict

    def ifhcinoctets(self, safe=False, oidonly=False):
        """Return dict of IFMIB ifHCInOctets for each ifIndex for device.

        Args:
            safe: Do a failsafe walk if True
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of ifHCInOctets. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.6'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        if safe is False:
            results = self.snmp_object.walk(oid, normalized=True)
        else:
            results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = value

        # Return
        return data_dict

    def ifhcoutoctets(self, safe=False, oidonly=False):
        """Return dict of IFMIB ifHCOutOctets for each ifIndex for device.

        Args:
            safe: Do a failsafe walk if True
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of ifHCOutOctets. Key = OID's last node.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.10'

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        if safe is False:
            results = self.snmp_object.walk(oid, normalized=True)
        else:
            results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = value

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
