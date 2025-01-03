"""Module for LLDP-MIB."""

from collections import defaultdict
import binascii

# Import project libraries
from switchmap.poller.snmp.base_query import Query
from switchmap.poller.snmp import BridgeQuery
from switchmap.core import general
from . import mib_if


def get_query():
    """Return this module's Query class."""
    return LldpQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return LldpQuery(snmp_object)


class LldpQuery(Query):
    """Class interacts with LLDP-MIB.

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
        self._snmp_object = snmp_object
        self._use_ifindex = False

        # Get one OID entry in MIB (lldpRemSysName)
        test_oid = ".1.0.8802.1.1.2.1.4.1.1.9"

        super().__init__(snmp_object, test_oid, tags=["layer1"])

        # Load the ifindex baseport map if this mib is supported
        bridge_mib = BridgeQuery(self._snmp_object)

        if self.supported() and bridge_mib.supported():
            self._baseportifindex = bridge_mib.dot1dbaseport_2_ifindex()
            self._use_ifindex = self._use_ifindex_check()
        else:
            self._baseportifindex = None

    def layer1(self):
        """Get layer 1 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface lldpRemSysName data
        values = self.lldpremsysname()
        for key, value in values.items():
            final[key]["lldpRemSysName"] = value

        # Get interface lldpRemSysDesc data
        values = self.lldpremsysdesc()
        for key, value in values.items():
            final[key]["lldpRemSysDesc"] = value

        # Get interface lldpRemPortDesc data
        values = self.lldpremportdesc()
        if values is not None:
            for key, value in values.items():
                final[key]["lldpRemPortDesc"] = value

        # Get interface lldpRemSysCapEnabled data
        values = self.lldpremsyscapenabled()
        if values is not None:
            for key, value in values.items():
                final[key]["lldpRemSysCapEnabled"] = value

        # Return
        return final

    def lldpremsysname(self, oidonly=False):
        """Return dict of LLDP-MIB lldpRemSysName for each port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of lldpRemSysName using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.0.8802.1.1.2.1.4.1.1.9"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self._snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Check if this OID is indexed using iFindex or dot1dBasePort
            ifindex = self._ifindex(key)

            # We have seen issues where self._baseportifindex doesn't always
            # return a complete dict of values that include all ifindexes
            if bool(ifindex) is True:
                data_dict[ifindex] = str(bytes(value), encoding="utf-8")

        # Return the interface descriptions
        return data_dict

    def lldpremsyscapenabled(self, oidonly=False):
        """Return dict of LLDP-MIB lldpRemSysCapEnabled for each port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of lldpRemSysCapEnabled using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)
        length_in_bits = 16
        base = 16

        # Descriptions
        oid = ".1.0.8802.1.1.2.1.4.1.1.12"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self._snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Check if this OID is indexed using iFindex or dot1dBasePort
            ifindex = self._ifindex(key)

            # We have seen issues where self._baseportifindex doesn't always
            # return a complete dict of values that include all ifindexes
            if bool(ifindex) is False:
                continue

            # Convert binary data to hex value
            hex_value = binascii.hexlify(value).decode("utf-8")

            # Convert hex value to right justified 16 character binary string
            binary_string = bin(int(hex_value, base))[2:].zfill(length_in_bits)
            data_dict[ifindex] = binary_string

        # Return the interface descriptions
        return data_dict

    def lldpremsysdesc(self, oidonly=False):
        """Return dict of LLDP-MIB lldpRemSysDesc for each port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of lldpRemSysDesc using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.0.8802.1.1.2.1.4.1.1.10"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self._snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Check if this OID is indexed using iFindex or dot1dBasePort
            ifindex = self._ifindex(key)

            # We have seen issues where self._baseportifindex doesn't always
            # return a complete dict of values that include all ifindexes
            if bool(ifindex) is True:
                data_dict[ifindex] = general.cleanstring(
                    str(bytes(value), encoding="utf-8")
                )

        # Return the interface descriptions
        return data_dict

    def lldpremportdesc(self, oidonly=False):
        """Return dict of LLDP-MIB lldpRemPortDesc for each port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of lldpRemPortDesc using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.0.8802.1.1.2.1.4.1.1.8"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self._snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Check if this OID is indexed using iFindex or dot1dBasePort
            ifindex = self._ifindex(key)

            # We have seen issues where self._baseportifindex doesn't always
            # return a complete dict of values that include all ifindexes
            if bool(ifindex) is True:
                data_dict[ifindex] = general.cleanstring(
                    str(bytes(value), encoding="utf-8")
                )

        # Return the interface descriptions
        return data_dict

    def lldplocportdesc(self, oidonly=False):
        """Return dict of LLDP-MIB lldpLocPortDesc for each port.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of lldpLocPortDesc using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.0.8802.1.1.2.1.3.7.1.4"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = self._snmp_object.swalk(oid, normalized=False)
        for key, value in results.items():
            # Check if this OID is indexed using iFindex or dot1dBasePort
            key_index = int(key.split(".")[-1])

            # Check if this OID is indexed using iFindex or dot1dBasePort
            if bool(self._baseportifindex) is True:
                if self._use_ifindex is True:
                    ifindex = key_index
                else:
                    ifindex = self._baseportifindex[key_index]
            else:
                ifindex = key_index

            # We have seen issues where self._baseportifindex doesn't always
            # return a complete dict of values that include all ifindexes
            if bool(ifindex) is True:
                data_dict[ifindex] = general.cleanstring(
                    str(bytes(value), encoding="utf-8")
                )

        # Return the interface descriptions
        return data_dict

    def _use_ifindex_check(self):
        """Return if LLDP OIDs are keyed by ifIndex or dot1dBasePortIfIndex.

        Args:
            None

        Returns:
            use_ifindex: True if ifIndex is used

        """
        # Initialize key variables
        use_ifindex = False
        ifdescr = mib_if.IfQuery(self._snmp_object).ifdescr()

        # Use the well known lldplocportdesc OID that must be supported
        oid = ".1.0.8802.1.1.2.1.3.7.1.4"

        # Process results
        lldpdescr = self._snmp_object.swalk(oid, normalized=False)
        for oid_key in sorted(lldpdescr.keys()):
            # Check if this OID is indexed using iFindex or dot1dBasePort
            lldp_key = int(oid_key.split(".")[-1])

            if lldp_key in ifdescr:
                interface = lldpdescr[oid_key].decode("utf-8")
                if interface.lower() == ifdescr[lldp_key].lower():
                    use_ifindex = True
                    break

        # Return
        return use_ifindex

    def _ifindex(self, key):
        """Return ifindex of port.

        Args:
            key: Key from SNMP walk

        Returns:
            ifindex: The ifindex of the port

        """
        # Initialize key variables
        ifindex = None

        # Check if this OID is indexed using iFindex or dot1dBasePort
        if bool(self._baseportifindex) is True:
            if self._use_ifindex is True:
                ifindex = _penultimate_node(key)
            else:
                bridgeport = _penultimate_node(key)
                ifindex = self._baseportifindex[bridgeport]
        else:
            ifindex = _penultimate_node(key)

        # Return
        return ifindex


def _penultimate_node(oid):
    """Return the penultimate node from an OID.

    Args:
        oid: OID

    Returns:
        value: Value of the penultimate node

    """
    # Initialize key variables
    nodes = oid.split(".")
    value = int(nodes[-2])

    # Return
    return value
