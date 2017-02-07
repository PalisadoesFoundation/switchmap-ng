#!/usr/bin/env python3
"""Class interacts with devices supporting BRIDGE-MIB."""

from collections import defaultdict
import binascii

from switchmap.snmp.base_query import Query

from switchmap.utils import log
from pprint import pprint
import sys


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
        # Assign SNMP object
        self.snmp_object = snmp_object

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
        final = defaultdict(lambda: defaultdict(dict))
        done = False

        # Check if Cisco VLANS are supported
        oid_vtpvlanstate = '.1.3.6.1.4.1.9.9.46.1.3.1.1.2'
        oid_exists = self.snmp_object.oid_exists_walk(oid_vtpvlanstate)
        if bool(oid_exists) is True:
            final = self._macaddresstable_cisco()
            done = True

        # Check if Juniper VLANS are supported
        if done is False:
            oid_dot1qvlanstaticname = '.1.3.6.1.2.1.17.7.1.4.3.1.1'
            oid_exists = self.snmp_object.oid_exists_walk(
                oid_dot1qvlanstaticname)
            if bool(oid_exists) is True:
                final = self._macaddresstable_juniper()

        # Return
        return final

    def _macaddresstable_cisco(self):
        """Return dict of the Cisco device's MAC address table.

        Args:
            None

        Returns:
            final: Dict of MAC addresses keyed by ifIndex

        """
        # Initialize key variables
        data_dict = defaultdict(lambda: defaultdict(dict))
        final = defaultdict(lambda: defaultdict(dict))
        context_names = ['']

        # Check if Cisco VLANS are supported
        oid_vtpvlanstate = '.1.3.6.1.4.1.9.9.46.1.3.1.1.2'
        oid_exists = self.snmp_object.oid_exists_walk(oid_vtpvlanstate)
        if bool(oid_exists) is True:
            # Get the vlantype
            oid_vtpvlantype = '.1.3.6.1.4.1.9.9.46.1.3.1.1.3'
            vtpvlantype = self.snmp_object.swalk(
                oid_vtpvlantype, normalized=True)

            # Append additonal vlan context names to query.
            # Only if Ethernet VLANs (pysnmp dies silently otherwise)
            vtpvlanstate = self.snmp_object.swalk(
                oid_vtpvlanstate, normalized=True)
            for vlan, state in vtpvlanstate.items():
                if int(state) == 1 and int(vtpvlantype[vlan]) == 1:
                    # Create context for older Cisco systems
                    cisco_context = '{}'.format(vlan)
                    context_names.append(cisco_context)

                    # Create context for newer Cisco systems
                    cisco_context = 'vlan-{}'.format(vlan)
                    context_names.append(cisco_context)

        # Get key information
        macs = self._dot1dtpfdbaddress(context_names=context_names)
        dot1dtpfdbport = self._dot1dtpfdbport(context_names=context_names)
        baseportifindex = self.dot1dbaseport_2_ifindex(
            context_names=context_names)

        # Create a dict keyed by ifIndex
        for decimal_macaddress, hex_macaddress in macs.items():
            # Sometimes an overloaded system running this script may have
            # timeouts retrieving data that should normally be there.
            # This prevents the script from crashing when this occurs
            if bool(dot1dtpfdbport[decimal_macaddress]) is False:
                continue

            # Get ifIndex from dot1dBasePort
            dot1dbaseport = int(dot1dtpfdbport[decimal_macaddress])
            ifindex = baseportifindex[dot1dbaseport]

            # With multi-threading sometimes baseportifindex has empty values.
            if bool(ifindex) is False:
                continue

            # Assign MAC addresses to ifIndex
            if ifindex not in data_dict:
                data_dict[ifindex] = [hex_macaddress]
            else:
                data_dict[ifindex].append(hex_macaddress)

        # Assign MACs to secondary key for final result
        for ifindex, hex_macaddresses in data_dict.items():
            final[ifindex]['jm_macs'] = []
            for next_mac in hex_macaddresses:
                final[ifindex]['jm_macs'].append(next_mac)

        # Return
        return final

    def _macaddresstable_juniper(self):
        """Return dict of the Juniper device's MAC address table.

        Args:
            None

        Returns:
            final: Dict of MAC addresses keyed by ifIndex

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))
        dot1dbaseport_macs = {}

        # Check if Jnuiper VLANS are supported
        oid_dot1qvlanstaticname = '.1.3.6.1.2.1.17.7.1.4.3.1.1'
        oid_exists = self.snmp_object.oid_exists_walk(oid_dot1qvlanstaticname)
        if bool(oid_exists) is True:
            # Create a dict of MAC addresses found
            mac_dict = self._dot1qtpfdbport()
            for decimal_macaddress, dot1dbaseport in mac_dict.items():
                # Convert decimal mac to hex
                # (Only use the last 6 digits in the decimal_macaddress, first
                # digit is the vlan number)
                hex_macaddress = ''
                mac_bytes = decimal_macaddress.split('.')[-6:]
                for mac_byte in mac_bytes:
                    hex_macaddress = (
                        '{}{}'.format(
                            hex_macaddress, hex(int(mac_byte))[2:].zfill(2)))

                # Assign MAC to baseport index
                if dot1dbaseport in dot1dbaseport_macs:
                    dot1dbaseport_macs[dot1dbaseport].append(hex_macaddress)
                else:
                    dot1dbaseport_macs[dot1dbaseport] = [hex_macaddress]

            # Assign MACs to ifindex
            baseportifindex = self.dot1dbaseport_2_ifindex()
            for dot1dbaseport, ifindex in baseportifindex.items():
                if dot1dbaseport in dot1dbaseport_macs:
                    final[ifindex][
                        'jm_macs'] = dot1dbaseport_macs[dot1dbaseport]

        # Return
        return final

    def _dot1dtpfdbport(self, context_names=None):
        """Return dict of BRIDGE-MIB dot1dTpFdbPort data.

        Args:
            None

        Returns:
            data_dict: Dict of dot1dTpFdbPort using the OID nodes
                excluding the OID root as key

        """
        # Initialize key variables
        if context_names is None:
            context_names = ['']
        data_dict = defaultdict(dict)

        # Process values
        oid = '.1.3.6.1.2.1.17.4.3.1.2'
        for context_name in context_names:
            results = self.snmp_object.swalk(
                oid, normalized=False, context_name=context_name)
            for key, value in results.items():
                new_key = key[len(oid):]
                data_dict[new_key] = value

        # Return data
        return data_dict

    def _dot1qtpfdbport(self):
        """Return dict of BRIDGE-MIB dot1qTpFdbPort data.

        Args:
            None

        Returns:
            data_dict: Dict of dot1qTpFdbPort using the OID nodes
                excluding the OID root as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)
        vlan_dict = defaultdict(dict)
        vlans = []

        # Process dot1qvlanstaticname OID
        oid_dot1qvlanstaticname = '.1.3.6.1.2.1.17.7.1.4.3.1.1'
        oid_exists = self.snmp_object.oid_exists_walk(oid_dot1qvlanstaticname)
        if bool(oid_exists) is True:
            results = self.snmp_object.walk(
                oid_dot1qvlanstaticname, normalized=True)
            for key, value in results.items():
                vlan_dict[key] = value
            for key, _ in vlan_dict.items():
                vlans.append(key)

            # Process values
            oid = '.1.3.6.1.2.1.17.7.1.2.2.1.2'
            for vlan in vlans:
                new_oid = '{}.{}'.format(oid, vlan)
                results = self.snmp_object.swalk(new_oid, normalized=False)
                for key, value in results.items():
                    new_key = key[len(oid):]
                    data_dict[new_key] = value

        # Return data
        return data_dict

    def _dot1dtpfdbaddress(self, context_names=None):
        """Return dict of BRIDGE-MIB dot1dTpFdbAddress data.

        Args:
            None

        Returns:
            data_dict: Dict of dot1dTpFdbAddress using the OID nodes
                excluding the OID root as key

        """
        # Initialize key variables
        if context_names is None:
            context_names = ['']
        data_dict = defaultdict(dict)

        # Process values
        oid = '.1.3.6.1.2.1.17.4.3.1.1'
        for context_name in context_names:
            results = self.snmp_object.swalk(
                oid, normalized=False, context_name=context_name)
            for key, value in results.items():
                new_key = key[len(oid):]
                macaddress = binascii.hexlify(value).decode('utf-8')
                data_dict[new_key] = macaddress.lower()

        # Return data
        return data_dict

    def dot1dbaseport_2_ifindex(self, context_names=None):
        """Return dict of BRIDGE-MIB dot1dBasePortIfIndex data.

        Args:
            None

        Returns:
            data_dict: Dict of dot1dBasePortIfIndex with dot1dBasePort as key.

        """
        # Initialize key variables
        if context_names is None:
            context_names = ['']
        data_dict = defaultdict(dict)

        # Process values
        oid = '.1.3.6.1.2.1.17.1.4.1.2'
        for context_name in context_names:
            results = self.snmp_object.swalk(
                oid, normalized=True, context_name=context_name)
            for key, value in results.items():
                data_dict[int(key)] = value

        # Return data
        return data_dict
