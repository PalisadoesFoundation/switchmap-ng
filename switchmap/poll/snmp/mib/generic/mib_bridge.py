#!/usr/bin/env python3
"""Class interacts with devices supporting BRIDGE-MIB."""

from collections import defaultdict

from switchmap.poll.snmp.base_query import Query
from switchmap.core import general
from . import mib_if


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
        self._snmp_object = snmp_object

        # Get one OID entry in MIB (dot1dBasePortIfIndex)
        test_oid = ".1.3.6.1.2.1.17.4.3.1.2"

        # Determine whether LLDP is keyed on ifIndex or BasePortIndex
        # If the ifindex method is being used, all the lldpLocPortIds
        # will match the ifindex values
        self._ifindex = mib_if.IfQuery(snmp_object).ifindex()

        super().__init__(snmp_object, test_oid, tags=["layer1"])

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
        oid_vtpvlanstate = ".1.3.6.1.4.1.9.9.46.1.3.1.1.2"
        oid_exists = self._snmp_object.oid_exists(oid_vtpvlanstate)
        if bool(oid_exists) is True:
            final = self._macaddresstable_cisco()
            done = True

        # Check if Juniper VLANS are supported
        if done is False:
            oid_dot1qvlanstaticname = ".1.3.6.1.2.1.17.7.1.4.3.1.1"
            oid_exists = self._snmp_object.oid_exists(oid_dot1qvlanstaticname)
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
        context_names = [""]
        context_style = 0

        # Check if Cisco VLANS are supported
        oid_vtpvlanstate = ".1.3.6.1.4.1.9.9.46.1.3.1.1.2"
        oid_exists = self._snmp_object.oid_exists(oid_vtpvlanstate)
        if bool(oid_exists) is True:
            # Get the vlantype
            oid_vtpvlantype = ".1.3.6.1.4.1.9.9.46.1.3.1.1.3"
            vtpvlantype = self._snmp_object.swalk(
                oid_vtpvlantype, normalized=True
            )

            # Get VLANs and their states
            vtpvlanstate = self._snmp_object.swalk(
                oid_vtpvlanstate, normalized=True
            )

            # Get the style of context name to be used for this type of device
            for vlan, state in vtpvlanstate.items():
                if int(state) == 1 and int(vtpvlantype[vlan]) == 1:
                    context_style = self._cisco_context_style(vlan)
                    break

            # Append additional vlan context names to query.
            # Only if Ethernet VLANs (pysnmp dies silently otherwise)
            for vlan, state in vtpvlanstate.items():
                if int(state) == 1 and int(vtpvlantype[vlan]) == 1:
                    cisco_context = _cisco_vlan_context(vlan, context_style)
                    context_names.append(cisco_context)

        # Get key information
        macs = self._dot1dtpfdbaddress(context_names=context_names)
        dot1dtpfdbport = self._dot1dtpfdbport(context_names=context_names)
        baseportifindex = self.dot1dbaseport_2_ifindex()

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
            final[ifindex]["l1_macs"] = []
            for next_mac in hex_macaddresses:
                final[ifindex]["l1_macs"].append(next_mac)

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

        # Check if Juniper VLANS are supported
        oid_dot1qvlanstaticname = ".1.3.6.1.2.1.17.7.1.4.3.1.1"
        oid_exists = self._snmp_object.oid_exists(oid_dot1qvlanstaticname)
        if bool(oid_exists) is True:
            # Create a dict of MAC addresses found
            mac_dict = self._dot1qtpfdbport()
            for decimal_macaddress, dot1dbaseport in mac_dict.items():
                # Convert decimal mac to hex
                # (Only use the last 6 digits in the decimal_macaddress, first
                # digit is the vlan number)
                hex_macaddress = ""
                mac_bytes = decimal_macaddress.split(".")[-6:]
                for mac_byte in mac_bytes:
                    hex_macaddress = "{}{}".format(
                        hex_macaddress, hex(int(mac_byte))[2:].zfill(2)
                    )

                # Assign MAC to baseport index
                if dot1dbaseport in dot1dbaseport_macs:
                    dot1dbaseport_macs[dot1dbaseport].append(hex_macaddress)
                else:
                    dot1dbaseport_macs[dot1dbaseport] = [hex_macaddress]

            # Assign MACs to ifindex
            baseportifindex = self.dot1dbaseport_2_ifindex()
            for dot1dbaseport, ifindex in baseportifindex.items():
                if dot1dbaseport in dot1dbaseport_macs:
                    final[ifindex]["l1_macs"] = dot1dbaseport_macs[
                        dot1dbaseport
                    ]

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
            context_names = [""]
        data_dict = defaultdict(dict)

        # Process values
        oid = ".1.3.6.1.2.1.17.4.3.1.2"
        for context_name in context_names:
            results = self._snmp_object.swalk(
                oid, normalized=False, context_name=context_name
            )
            for key, value in results.items():
                new_key = key[len(oid) :]
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
        oid_dot1qvlanstaticname = ".1.3.6.1.2.1.17.7.1.4.3.1.1"
        oid_exists = self._snmp_object.oid_exists(oid_dot1qvlanstaticname)
        if bool(oid_exists) is True:
            results = self._snmp_object.walk(
                oid_dot1qvlanstaticname, normalized=True
            )
            for key, value in results.items():
                vlan_dict[key] = value
            for key, _ in vlan_dict.items():
                vlans.append(key)

            # Process values
            oid = ".1.3.6.1.2.1.17.7.1.2.2.1.2"
            for vlan in vlans:
                new_oid = "{}.{}".format(oid, vlan)
                results = self._snmp_object.swalk(new_oid, normalized=False)
                for key, value in results.items():
                    new_key = key[len(oid) :]
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
            context_names = [""]
        data_dict = defaultdict(dict)

        # Process values
        oid = ".1.3.6.1.2.1.17.4.3.1.1"
        for context_name in context_names:
            results = self._snmp_object.swalk(
                oid, normalized=False, context_name=context_name
            )
            for key, mac_value in results.items():
                # Assign the mac address to the dictionary
                new_key = key[len(oid) :]
                data_dict[new_key] = general.octetstr_2_string(mac_value)

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
        offset = 0
        if context_names is None:
            context_names = [""]
        data_dict = defaultdict(dict)

        # Get the difference between ifIndex and dot1dBasePortIfIndex
        oid = ".1.3.6.1.2.1.17.1.4.1.2"
        results = self._snmp_object.swalk(oid, normalized=True)
        for _bridge_index, ifindex in results.items():
            bridge_index = int(_bridge_index)
            offset = int(ifindex) - bridge_index
            break

        # Populate the dictionary keyed by dot1dBasePortIfIndex
        for ifindex, _ in sorted(self._ifindex.items()):
            bridge_index = ifindex - offset
            data_dict[bridge_index] = ifindex

        # Return data
        return data_dict

    def _cisco_context_style(self, vlan):
        """Return style value to use to query VLAN data on a cisco switch.

        Args:
            vlan: Number of vlan

        Returns:
            cisco_style: Style of context for formatting VLAN SNMP contexts

        """
        # Initialize key variables
        cisco_style = 0
        styles = [0, 1]

        # Try all available styles
        for style in styles:
            context_names = [_cisco_vlan_context(vlan, style)]
            result = self._dot1dtpfdbaddress(context_names=context_names)
            if bool(result) is True:
                cisco_style = style
                break

        # Return
        return cisco_style


def _cisco_vlan_context(vlan, context_style):
    """Return dict of BRIDGE-MIB dot1dBasePortIfIndex data.

    Args:
        vlan: Number of vlan
        context_style: Value of the context style to use

    Returns:
        cisco_context: SNMP context string

    """
    # Create context string
    if context_style == 0:
        # Create context for older Cisco systems
        cisco_context = "{}".format(vlan)
    else:
        # Create context for newer Cisco systems
        cisco_context = "vlan-{}".format(vlan)

    # Return
    return cisco_context


def _snmp_octetstr_2_string(binary_value):
    """Convert SNMP OCTETSTR to string.

    Args:
        binary_value: Binary value to convert

    Returns:
        result: String equivalent of binary_value

    """
    # Convert and return
    result = "".join(["%0.2x" % ord(_) for _ in binary_value.decode("utf-8")])
    return result.lower()
