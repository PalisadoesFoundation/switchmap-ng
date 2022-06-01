"""Module for JUNIPER-VLAN-MIB."""


from collections import defaultdict

# Import project libraries
from switchmap.poll.snmp.base_query import Query
from switchmap.poll.snmp.mib_bridge import BridgeQuery


def get_query():
    """Return this module's Query class."""
    return JuniperVlanQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return JuniperVlanQuery(snmp_object)


class JuniperVlanQuery(Query):
    """Class interacts with JUNIPER-VLAN-MIB.

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
        # Define query object
        self.snmp_object = snmp_object

        # Get one OID entry in MIB (jnxExVlanTag)
        test_oid = '.1.3.6.1.4.1.2636.3.40.1.5.1.7.1.3'

        super().__init__(snmp_object, test_oid, tags=['layer1', 'layer2'])

        # Get mapping of the VLAN's dot1dbaseport ID value to its jnxExVlanTag
        # Do this only once instead of every time we invoke a method
        if self.supported() is True:
            self.vlan_map = self._vlanid2tag()
        else:
            self.vlan_map = None

        # Get a mapping of dot1dbaseport values to the corresponding ifindex
        bridge_mib = BridgeQuery(self.snmp_object)

        self.baseportifindex = bridge_mib.dot1dbaseport_2_ifindex()

    def layer1(self):
        """Get layer 1 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface jnxExVlanTag data
        values = self.jnxexvlantag()
        for key, value in values.items():
            final[key]['jnxExVlanTag'] = value

        # Get interface jnxExVlanPortAccessMode data
        values = self.jnxexvlanportaccessmode()
        for key, value in values.items():
            final[key]['jnxExVlanPortAccessMode'] = value

        # Return
        return final

    def layer2(self):
        """Get layer 2 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface jnxExVlanName data
        values = self.jnxexvlanname()
        for key, value in values.items():
            final[key]['jnxExVlanName'] = value

        # Return
        return final

    def jnxexvlanportaccessmode(self):
        """Return dict of JUNIPER-VLAN-MIB jnxExVlanPortAccessMode per port.

        Args:
            None

        Returns:
            data_dict: Dict of jnxExVlanPortAccessMode using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.4.1.2636.3.40.1.5.1.7.1.5'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            ifindex = self.baseportifindex[int(key)]
            data_dict[ifindex] = value

        # Return
        return data_dict

    def jnxexvlantag(self):
        """Return dict of JUNIPER-VLAN-MIB jnxExVlanTag per port.

        Args:
            None

        Returns:
            data_dict: Dict of jnxExVlanTag using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid = '.1.3.6.1.4.1.2636.3.40.1.5.1.7.1.3'
        results = self.snmp_object.walk(oid, normalized=False)
        for key in sorted(results.keys()):
            # The key is the full OID. Split this into its component nodes
            nodes = key.split('.')

            # Get the VLAN ID and corresponding VLAN tag
            vlan_id = nodes[-2]
            vlan_tag = self.vlan_map[int(vlan_id)]

            # Get dot1dbaseport value and it's corresponding ifindex
            baseport_value = nodes[-1]
            ifindex = self.baseportifindex[int(baseport_value)]
            if ifindex in data_dict:
                data_dict[ifindex].append(vlan_tag)
            else:
                data_dict[ifindex] = [vlan_tag]

        # Return the interface descriptions
        return data_dict

    def jnxexvlanname(self):
        """Return dict of JUNIPER-VLAN-MIB jnxExVlanName for each VLAN tag.

        Args:
            None

        Returns:
            data_dict: Dict of jnxExVlanName using the VLAN tag as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.2636.3.40.1.5.1.5.1.2'
        results = self.snmp_object.walk(oid, normalized=True)
        for vlan_id, value in results.items():
            # Get VLAN tag
            vlan_tag = self.vlan_map[int(vlan_id)]

            # Assign value (Convert to string)
            data_dict[vlan_tag] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def _vlanid2tag(self):
        """Return dict of JUNIPER-VLAN-MIB jnxExVlanTag w/ dot1dbaseport key.

        Args:
            None:

        Returns:
            data_dict: Dict of mapping

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Get a mapping of dot1dbaseport values to the corresponding ifindex
        oid = '.1.3.6.1.4.1.2636.3.40.1.5.1.5.1.5'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = int(value)

        # Return the interface descriptions
        return data_dict
